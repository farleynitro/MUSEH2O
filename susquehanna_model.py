import numpy as np
from tqdm import tqdm
import utils
from rbf import RBF


class susquehanna_model:
    gammaH20 = 1000.0
    GG = 9.81

    def __init__(self, l0, l0_MR, d0, n_years):  #  level0, level_MR0, d0?, n_years
        # initial condition Conowingo
        self.init_level = l0  # feet
        # initial condition in muddy run
        self.init_level_MR = l0_MR  # feet
        # initial start day
        self.day0 = d0  # day int
        # variables from the header file
        self.RBF_setting = []
        self.input_min = []
        self.input_max = []
        self.output_max = []
        self.PolicySim = ""

        self.Nobj = 6  # 8 in flood version
        self.n_days_in_year = 365
        self.n_years = n_years  # historical record #1000 simulation horizon (1996,2001)
        self.time_horizon_H = self.n_days_in_year * self.n_years
        self.dec_step = 4  # 4-hours decisional time step
        self.day_fraction = int(24 / self.dec_step)
        self.n_days_one_year = 1 * 365

    def load_data(self):
        # n_days_one_year = 1*365 moved to init
        # Conowingo characteristics
        self.lsv_rel = utils.loadMatrix(
            "./data1999/lsv_rel_Conowingo.txt", 3, 10
        )  # level (ft) - Surface (acre) - storage (acre-feet) relationships
        self.turbines = utils.loadMatrix(
            "./data1999/turbines_Conowingo2.txt", 3, 13
        )  # Max-min capacity (cfs) - efficiency of Conowingo plant turbines
        self.tailwater = utils.loadMatrix(
            "./data1999/tailwater.txt", 2, 18
        )  # tailwater head (ft) - release flow (cfs)
        self.spillways = utils.loadMatrix(
            "./data1999/spillways_Conowingo.txt", 3, 8
        )  # substitute with newConowingo1      # level (ft) - max release (cfs) - min release (cfs) for level > 108 ft

        # Muddy Run characteristics
        self.lsv_rel_Muddy = utils.loadMatrix(
            "./data1999/lsv_rel_Muddy.txt", 3, 38
        )  # level (ft) - Surface (acre) - storage (acre-feet) relationships
        self.turbines_Muddy = utils.loadVector(
            "./data1999/turbines_Muddy.txt", 4
        )  # Turbine-Pumping capacity (cfs) - efficiency of Muddy Run plant (equal for the 8 units)

        # historical
        # N_samples = self.n_days_one_year * self.n_years
        # self.evap_CO_MC= utils.loadVector("./data_historical/vectors/evapCO_history.txt",N_samples)         # evaporation losses (inches per day)
        # self.inflow_MC = utils.loadVector("./data_historical/vectors/MariettaFlows_history.txt",N_samples)   # inflow, i.e. flows at Marietta (cfs)
        # self.inflowLat_MC = utils.loadVector("./data_historical/vectors/nLat_history.txt",N_samples)         # lateral inflows from Marietta to Conowingo (cfs)
        # self.evap_Muddy_MC = utils.loadVector("./data_historical/vectors/evapMR_history.txt",N_samples)      # evaporation losses (inches per day)
        # self.inflow_Muddy_MC = utils.loadVector("./data_historical/vectors/nMR_history.txt",N_samples)

        # stochastic hydrology
        self.evap_CO_MC = utils.loadMatrix(
            "./dataMC/evapCO_MC.txt", self.n_years, self.n_days_one_year
        )  # evaporation losses (inches per day)
        self.inflow_MC = utils.loadMatrix(
            "./dataMC/MariettaFlows_MC.txt", self.n_years, self.n_days_one_year
        )  # inflow, i.e. flows at Marietta (cfs)
        self.inflowLat_MC = utils.loadMatrix(
            "./dataMC/nLat_MC.txt", self.n_years, self.n_days_one_year
        )  # lateral inflows from Marietta to Conowingo (cfs)
        self.evap_Muddy_MC = utils.loadMatrix(
            "./dataMC/evapMR_MC.txt", self.n_years, self.n_days_one_year
        )  # evaporation losses (inches per day)
        self.inflow_Muddy_MC = utils.loadMatrix(
            "./dataMC/nMR_MC.txt", self.n_years, self.n_days_one_year
        )  # inflow to Muddy Run (cfs)

        # objectives parameters
        self.energy_prices = utils.loadArrangeMatrix(
            "./data1999/Pavg99.txt", 24, self.n_days_one_year
        )  # energy prices ($/MWh)
        self.min_flow = utils.loadVector(
            "./data1999/min_flow_req.txt", self.n_days_one_year
        )  # FERC minimum flow requirements for 1 year (cfs)
        self.h_ref_rec = utils.loadVector(
            "./data1999/h_rec99.txt", self.n_days_one_year
        )  # target level for weekends in touristic season (ft)
        self.w_baltimore = utils.loadVector(
            "./data1999/wBaltimore.txt", self.n_days_one_year
        )  # water demand of Baltimore (cfs)
        self.w_chester = utils.loadVector(
            "./data1999/wChester.txt", self.n_days_one_year
        )  # water demand of Chester (cfs)
        self.w_atomic = utils.loadVector(
            "./data1999/wAtomic.txt", self.n_days_one_year
        )  # water demand for cooling the atomic power plant (cfs)

        # standardization of the input-outpu of the RBF release curve
        self.input_max.append(self.n_days_in_year * self.day_fraction - 1)
        # self.input_max.append(6)
        self.input_max.append(120)
        self.output_max.append(utils.computeMax(self.w_atomic))
        self.output_max.append(utils.computeMax(self.w_baltimore))
        self.output_max.append(utils.computeMax(self.w_chester))
        self.output_max.append(85412)  # max release = tot turbine capacity + spillways @ max storage

    def setPolicySim(self, newPolicySim):
        self.PolicySim = newPolicySim

    def setRBF(self, pn, pm, pK):
        self.RBF_setting.append(pn)
        self.RBF_setting.append(pm)
        self.RBF_setting.append(pK)
        return self.RBF_setting

    def RBFs_policy(self, control_law, input):
        input1 = []
        for i in range(0, self.RBF_setting[1]):
            # RBF_setting[1] is the number of inputs. Input1 is the normalized value of each
            # input1.append((input[i] - self.input_min[i]) / (self.input_max[i] - self.input_min[i]))
            input1.append(input[i] / self.input_max[i])
        # RBF
        u = []
        u = control_law.rbf_control_law(input1)  #  print("first element of u " + str(u[0]))
        # de-normalization, Q: What is denormalization? Why do we do it?
        uu = []
        for i in range(0, self.RBF_setting[2]):  # RBF_setting[2] is the total number of outputs
            uu.append(u[i] * self.output_max[i])
        return uu

    # def evaluate(self, var, opt_met): # needed?
    #     pass

    def evaluateMC(self, var, opt_met=1):
        Jhydropower, Jatomicpowerplant, Jbaltimore, Jchester, Jenvironment, Jrecreation = self.simulate(
            var,
            self.inflow_MC,
            self.inflowLat_MC,
            self.inflow_Muddy_MC,
            self.evap_CO_MC,
            self.evap_Muddy_MC,
            opt_met,
        )
        outcomes = [Jhydropower, Jatomicpowerplant, Jbaltimore, Jchester, Jenvironment, Jrecreation]
        print(outcomes)
        return outcomes

    def storageToLevel(self, s, lake):
        # s : storage
        # lake : which lake it is at
        # gets triggered decision step * time horizon
        s_ = utils.cubicFeetToAcreFeet(s)
        if lake == 0:
            h = utils.interpolate_linear(self.lsv_rel_Muddy[2], self.lsv_rel_Muddy[0], s_)
        else:
            h = utils.interpolate_linear(self.lsv_rel[2], self.lsv_rel[0], s_)
        return h

    def levelToStorage(self, h, lake):
        if lake == 0:
            s = utils.interpolate_linear(self.lsv_rel_Muddy[0], self.lsv_rel_Muddy[2], h)
        else:
            s = utils.interpolate_linear(self.lsv_rel[0], self.lsv_rel[2], h)
        return utils.acreFeetToCubicFeet(s)

    def levelToSurface(self, h, lake):
        if lake == 0:
            S = utils.interpolate_linear(self.lsv_rel_Muddy[0], self.lsv_rel_Muddy[1], h)
        else:
            S = utils.interpolate_linear(self.lsv_rel[0], self.lsv_rel[1], h)
        return utils.acreToSquaredFeet(S)

    def tailwater_level(self, q):
        l = utils.interpolate_linear(self.tailwater[0], self.tailwater[1], q)
        return l

    def muddyRunPumpTurb(self, day, hour, level_Co, level_MR):
        # Determines the pumping and turbine release volumes in a day based on the hour and day of week for muddy run
        QP = 24800  # cfs
        QT = 32000  # cfs
        qM = (
            self.levelToStorage(level_MR, 0) - self.levelToStorage(470.0, 0)
        ) / 3600  # active storage = sMR - deadStorage
        qp = 0.0
        qt = 0.0
        if day == 0:  # sunday
            if hour < 5 or hour >= 22:
                qp = QP
        elif 1 <= day <= 4:  # monday to thursday
            if hour <= 6 or hour >= 21:
                qp = QP
            if (hour >= 7 and hour <= 11) or (hour >= 17 and hour <= 20):
                qt = min(QT, qM)
        elif day == 5:  # friday
            if (hour >= 7 and hour <= 11) or (hour >= 17 and hour <= 20):
                qt = min(QT, qM)
        elif day == 6:  # saturday
            if hour <= 6 or hour >= 22:
                qp = QP
        # water pumping stops to Muddy Run beyond this point.
        # However, according to the conowingo authorities 800 cfs will be released as emergency credits in order to keep the facilities from running
        # Q: The level in Conowingo impacts the pumping in Muddy Run. How?
        if level_Co < 104.7:  # if True cavitation problems in pumping
            qp = 0.0

        if level_MR < 470.0:
            qt = 0.0
        return qp, qt  # pumping, Turbine release

    def actual_release(self, uu, level_Co, day_of_year):
        # Check if it doesn't exceed the spillway capacity
        Tcap = 85412  # total turbine capacity (cfs)
        # maxSpill = 1242857.0 # total spillway combined (cfs)

        # minimum discharge values at APP, Balitomore, Chester and downstream
        qm_A = 0.0
        qm_B = 0.0
        qm_C = 0.0
        qm_D = 0.0

        # maximum discharge values. The max discharge can be as much as the demand in that area
        qM_A = self.w_atomic[day_of_year]
        qM_B = self.w_baltimore[day_of_year]
        qM_C = self.w_chester[day_of_year]
        qM_D = Tcap

        # if level_Co <= self.min_level_app:
        #     qM_A = 0.0
        # else:
        #     qM_A = self.w_atomic[day_of_year]

        # if level_Co <= self.min_level_baltimore:
        #     qM_B = 0.0
        # else:
        #     qM_B = self.w_baltimore[day_of_year]
        # if level_Co <= self.min_level_chester:
        #     qM_C = 0.0
        # else:
        #     qM_C = self.w_chester[day_of_year]

        if level_Co > 110.2:  # spillways activated
            qM_D = (
                utils.interpolate_linear(self.spillways[0], self.spillways[1], level_Co) + Tcap
            )  # Turbine capacity + spillways
            qm_D = (
                utils.interpolate_linear(self.spillways[0], self.spillways[1], level_Co) + Tcap
            )  # change to spillways[2]

        # different from flood model
        if level_Co < 105.5:
            qM_D = 0.0
        elif level_Co < 103.5:
            qM_A = 0.0
        elif level_Co < 100.5:
            qM_C = 0.0
        elif level_Co < 91.5:
            qM_B = 0.0

        # actual release
        rr = []
        rr.append(min(qM_A, max(qm_A, uu[0])))
        rr.append(min(qM_B, max(qm_B, uu[1])))
        rr.append(min(qM_C, max(qm_C, uu[2])))
        rr.append(min(qM_D, max(qm_D, uu[3])))
        return rr

    def g_hydRevCo(self, r, h, day_of_year, hour0):
        Nturb = 13
        g_hyd = []
        g_rev = []
        pp = []
        c_hour = len(r) * hour0
        for i in range(0, len(r)):
            deltaH = h[i] - self.tailwater_level(r[i])
            q_split = r[i]
            for j in range(0, Nturb):
                if q_split < self.turbines[1][j]:
                    qturb = 0.0
                elif q_split > self.turbines[0][j]:
                    qturb = self.turbines[0][j]
                else:
                    qturb = q_split
                q_split = q_split - qturb
                p = (
                    0.79
                    * self.GG
                    * self.gammaH20
                    * utils.cubicFeetToCubicMeters(qturb)
                    * utils.feetToMeters(deltaH)
                    * 3600
                    / (3600 * 1000)
                )  # assuming lower efficiency as in Exelon docs
                pp.append(p)
            g_hyd.append(sum(pp))
            g_rev.append(sum(pp) / 1000 * self.energy_prices[c_hour][day_of_year])
            pp.clear()
            c_hour = c_hour + 1
        Gp = sum(g_hyd)
        Gr = sum(g_rev)
        return Gp, Gr

    def g_hydRevMR(self, qp, qr, hCo, hMR, day_of_year, hour0):
        Nturb = 8
        g_hyd = []
        g_pump = []
        g_rev = []
        g_revP = []
        c_hour = len(qp) * hour0
        pT = 0.0
        pP = 0.0
        for i in range(0, len(qp)):
            # net head
            deltaH = hMR[i] - hCo[i]
            # 8 turbines
            qp_split = qp[i]
            qr_split = qr[i]
            # Vectorize this part?
            for j in range(0, Nturb):
                if qp_split < 0.0:
                    qpump = 0.0
                elif qp_split > self.turbines_Muddy[2]:
                    qpump = self.turbines_Muddy[2]
                else:
                    qpump = qp_split

                p_ = (
                    self.turbines_Muddy[3]
                    * self.GG
                    * self.gammaH20
                    * utils.cubicFeetToCubicMeters(qpump)
                    * utils.feetToMeters(deltaH)
                    * 3600
                    / (3600 * 1000)
                )  # KWh/h
                pP = pP + p_
                qp_split = qp_split - qpump

                if qr_split < 0.0:
                    qturb = 0.0
                elif qr_split > self.turbines_Muddy[0]:
                    qturb = self.turbines_Muddy[0]
                else:
                    qturb = qr_split

                p = (
                    self.turbines_Muddy[1]
                    * self.GG
                    * self.gammaH20
                    * utils.cubicFeetToCubicMeters(qturb)
                    * utils.feetToMeters(deltaH)
                    * 3600
                    / (3600 * 1000)
                )  # kWh/h
                pT = pT + p
                qr_split = qr_split - qturb

            g_pump.append(pP)
            g_revP.append(pP / 1000 * self.energy_prices[c_hour][day_of_year])
            pP = 0.0
            g_hyd.append(pT)
            g_rev.append(pT / 1000 * self.energy_prices[c_hour][day_of_year])
            pT = 0.0
            c_hour = c_hour + 1

        return g_pump, g_hyd, g_revP, g_rev

    def res_transition_h(self, s0, uu, n_sim, n_lat, ev, s0_mr, n_sim_mr, ev_mr, day_of_year, day_of_week, hour0):
        HH = self.dec_step  # 4 hour horizon
        sim_step = 3600  # s/hour
        leak = 800  # cfs

        # Storages and levels of Conowingo and Muddy Run
        storage_Co = [-999.0] * (HH + 1)
        level_Co = [-999.0] * (HH + 1)
        storage_MR = [-999.0] * (HH + 1)
        level_MR = [-999.0] * (HH + 1)
        # Actual releases (Atomic Power plant, Baltimore, Chester, Dowstream)
        release_A = [-999.0] * (HH)
        release_B = [-999.0] * (HH)
        release_C = [-999.0] * (HH)
        release_D = [-999.0] * (HH)
        q_pump = [-999.0] * (HH)
        q_rel = [-999.0] * (HH)
        s_rr = []
        rr = []

        # initial conditions
        storage_Co[0] = s0
        storage_MR[0] = s0_mr
        c_hour = HH * hour0

        for i in range(0, HH):
            # compute level
            level_Co[i] = self.storageToLevel(storage_Co[i], 1)
            level_MR[i] = self.storageToLevel(storage_MR[i], 0)
            # Muddy Run operation
            q_pump[i], q_rel[i] = self.muddyRunPumpTurb(day_of_week, int(c_hour), level_Co[i], level_MR[i])

            # Compute actual release
            rr = self.actual_release(uu, level_Co[i], day_of_year)
            release_A[i] = rr[0]
            release_B[i] = rr[1]
            release_C[i] = rr[2]
            release_D[i] = rr[3]
            WS = release_A[i] + release_B[i] + release_C[i]  # Q: Why is this being added?

            # Compute surface level and evaporation losses
            surface_Co = self.levelToSurface(level_Co[i], 1)
            evaporation_losses_Co = utils.inchesToFeet(ev) * surface_Co / 86400  # cfs
            surface_MR = self.levelToSurface(level_MR[i], 0)
            evaporation_losses_MR = utils.inchesToFeet(ev_mr) * surface_MR / 86400  # cfs

            # System Transition
            storage_MR[i + 1] = storage_MR[i] + sim_step * (q_pump[i] - q_rel[i] + n_sim_mr - evaporation_losses_MR)
            storage_Co[i + 1] = storage_Co[i] + sim_step * (
                n_sim + n_lat - release_D[i] - WS - evaporation_losses_Co - q_pump[i] + q_rel[i] - leak
            )
            c_hour = c_hour + 1

            storage_MR[i + 1] = storage_MR[i] + sim_step * (q_pump[i] - q_rel[i] + n_sim_mr - evaporation_losses_MR)
            storage_Co[i + 1] = storage_Co[i] + sim_step * (
                n_sim + n_lat - release_D[i] - WS - evaporation_losses_Co - q_pump[i] + q_rel[i] - leak
            )

        # s_rr.append(storage_Co[HH])
        # # print(" storage HH " + str(storage_Co[HH]))
        # s_rr.append(storage_MR[HH])
        # s_rr.append(utils.computeMean(release_A))
        # s_rr.append(utils.computeMean(release_B))
        # s_rr.append(utils.computeMean(release_C))
        # s_rr.append(utils.computeMean(release_D))

        s_rr.extend(
            [
                storage_Co[HH],
                storage_MR[HH],
                utils.computeMean(release_A),
                utils.computeMean(release_B),
                utils.computeMean(release_C),
                utils.computeMean(release_D),
            ]
        )

        # 4-hours hydropower production/revenue
        # rDTurb = []
        # Tcap = 85412
        # for i in range(0, len(release_D)):
        #     rDTurb.append(min(release_D[i], Tcap))

        # 4-hours hydropower production/revenue
        hp = self.g_hydRevCo(release_D, level_Co, day_of_year, hour0)
        # hp = self.g_hydRevCo(rDTurb, level_Co, day_of_year, hour0)
        hp_mr = self.g_hydRevMR(q_pump, q_rel, level_Co, level_MR, day_of_year, hour0)

        # Revenue
        s_rr.extend([hp[1], hp_mr[2], hp_mr[3]])
        # Production
        s_rr.extend([hp[0], hp_mr[0], hp_mr[1]])

        return s_rr

    def g_StorageReliability(self, h, hTarget):
        c = 0
        Nw = 0
        for i in range(0, len(h)):  # len(h) -1 in flood model
            tt = i % self.n_days_one_year
            if h[i] < hTarget[tt]:  # h[i] + 1  in flood model
                c = c + 1
            if hTarget[tt] > 0:
                Nw = Nw + 1

        G = 1 - c / Nw
        return G

    def g_ShortageIndex(self, q, qTarget):
        delta = 24 * 3600
        g = []
        for i in range(0, len(q)):
            tt = i % self.n_days_one_year
            gg = max((qTarget[tt] * delta) - (q[i] * delta), 0.0) / (qTarget[tt] * delta)
            g.append(gg * gg)
        G = utils.computeMean(g)
        return G

    def g_VolRel(self, q, qTarget):
        g = []
        delta = 24 * 3600
        for i in range(0, len(q)):
            tt = i % self.n_days_one_year
            g.append((q[i] * delta) / (qTarget[tt] * delta))
        G = utils.computeMean(g)
        return G

    def simulate(
        self,
        input_variable_list_var,
        inflow_MC_n_sim,
        inflowLateral_MC_n_lat,
        inflow_Muddy_MC_n_mr,
        evap_CO_MC_e_co,
        evap_Muddy_MC_e_mr,
        opt_met,
    ):
        # Initializing daily variables
        # storages and levels
        storage_Co = [-999.0] * (self.time_horizon_H + 1)
        level_Co = [-999.0] * (self.time_horizon_H + 1)  # (self.n_days_in_year + 1)
        storage_MR = [-999.0] * (self.time_horizon_H + 1)
        level_MR = [-999.0] * (self.time_horizon_H + 1)
        # Conowingo actual releases
        release_A = [-999.0] * self.time_horizon_H
        release_B = [-999.0] * self.time_horizon_H
        release_C = [-999.0] * self.time_horizon_H
        release_D = [-999.0] * self.time_horizon_H

        # subdaily variables
        storage2_Co = [-999.0] * (self.day_fraction + 1)
        level2_Co = [-999.0] * (self.day_fraction + 1)
        storage2_MR = [-999.0] * (self.day_fraction + 1)
        level2_MR = [-999.0] * (self.day_fraction + 1)
        release2_A = []
        release2_B = []
        release2_C = []
        release2_D = []

        # hydropower production/revenue
        hydropowerProduction_Co = []  # energy production at Conowingo
        hydropowerProduction_MR = []  # energy production at Muddy Run
        hydroPump_MR = []  # energy consumed for pumping at Muddy Run
        hydropowerRevenue_Co = []  # energy revenue at Conowingo
        hydropowerRevenue_MR = []  # energy revenue at Muddy Run
        hydropowerPumpRevenue_MR = []  # energy revenue consumed for pumping at Muddy Run

        # release decision variables ( AtomicPP, Baltimore, Chester ) only Downstream in Baseline
        uu = []
        ss_rr_hp = []
        # RBF.control_law(self.RBF_setting[0], self.RBF_setting[1], self.RBF_setting[2], var)
        control_law = RBF(self.RBF_setting[0], self.RBF_setting[1], self.RBF_setting[2], input_variable_list_var)
        input = []

        # initial condition
        level_Co[0] = self.init_level
        storage_Co[0] = self.levelToStorage(level_Co[0], 1)
        level_MR[0] = self.init_level_MR
        storage_MR[0] = self.levelToStorage(level_MR[0], 0)

        # identification of the periodicity (365 x fdays)
        count = 0
        total_decision_steps_TT = self.n_days_in_year * self.day_fraction
        jj = 0
        day_of_week = 0  # day of the week
        day_of_year = 0  # day of the year
        year = 0

        # run simulation
        for t in tqdm(range(0, self.time_horizon_H)):
            # identification of the day
            day_of_week = (self.day0 + t) % 7
            day_of_year = t % self.n_days_in_year
            if day_of_year % self.n_days_in_year == 0 and t != 0:
                year = year + 1

            # print(f"t: {t}")
            # print(f"day of year: {day_of_year}")
            # print(f"level_Co: {level_Co}")
            # print(f"level2_Co: {level2_Co}")
            # initialization of sub-daily cycle
            level2_Co[0] = level_Co[t]  # level_Co[day_of_year] <<< in flood
            storage2_Co[0] = storage_Co[t]
            level2_MR[0] = level_MR[t]
            storage2_MR[0] = storage_MR[t]

            # subdaily cycle
            for j in range(0, self.day_fraction):
                jj = count % total_decision_steps_TT
                # compute decision
                if opt_met == 0:  # fixed release
                    uu.append(uu[0])
                elif opt_met == 1:  # RBF-PSO
                    input.append(jj)
                    input.append(level2_Co[j])  # reservoir level
                    uu = self.RBFs_policy(control_law, input)
                    input.clear()
                # system transition
                # try:
                # print(f"year is: {year}")
                ss_rr_hp = self.res_transition_h(
                    storage2_Co[j],
                    uu,
                    inflow_MC_n_sim[year][day_of_year],
                    inflowLateral_MC_n_lat[year][day_of_year],
                    evap_CO_MC_e_co[year][day_of_year],
                    storage2_MR[j],
                    inflow_Muddy_MC_n_mr[year][day_of_year],
                    evap_Muddy_MC_e_mr[year][day_of_year],
                    day_of_year,
                    day_of_week,
                    j,
                )
                # ss_rr_hp = self.res_transition_h(
                #     storage2_Co[j],
                #     uu,
                #     inflow_MC_n_sim[t],
                #     inflowLateral_MC_n_lat[t],
                #     evap_CO_MC_e_co[t],
                #     storage2_MR[j],
                #     inflow_Muddy_MC_n_mr[t],
                #     evap_Muddy_MC_e_mr[t],
                #     day_of_year,
                #     day_of_week,
                #     j,
                # )
                # except Exception:
                #     print(t, " day has an error")
                storage2_Co[j + 1] = ss_rr_hp[0]
                storage2_MR[j + 1] = ss_rr_hp[1]
                level2_Co[j + 1] = self.storageToLevel(storage2_Co[j + 1], 1)
                level2_MR[j + 1] = self.storageToLevel(storage2_MR[j + 1], 0)
                release2_A.append(ss_rr_hp[2])
                release2_B.append(ss_rr_hp[3])
                release2_C.append(ss_rr_hp[4])
                release2_D.append(ss_rr_hp[5])

                # Hydropower revenue production
                hydropowerRevenue_Co.append(ss_rr_hp[6])  # 6-hours energy revenue ($/6h)
                hydropowerPumpRevenue_MR.append(ss_rr_hp[7])  # 6-hours energy revenue ($/6h) at MR
                hydropowerRevenue_MR.append(ss_rr_hp[8])  # 6-hours energy revenue ($/6h) at MR
                hydropowerProduction_Co.append(ss_rr_hp[9])  # 6-hours energy production (kWh/6h)
                hydroPump_MR.append(ss_rr_hp[10])  # 6-hours energy production (kWh/6h) at MR
                hydropowerProduction_MR.append(ss_rr_hp[11])  # 6-hours energy production (kWh/6h) at MR
                input = []
                uu = []
                ss_rr_hp = []
                count = count + 1

            # daily values
            level_Co[day_of_year + 1] = level2_Co[self.day_fraction]
            storage_Co[t + 1] = storage2_Co[self.day_fraction]
            release_A[day_of_year] = utils.computeMean(release2_A)
            release_B[day_of_year] = utils.computeMean(release2_B)
            release_C[day_of_year] = utils.computeMean(release2_B)
            release_D[day_of_year] = utils.computeMean(release2_D)
            level_MR[t + 1] = level2_MR[self.day_fraction]
            storage_MR[t + 1] = storage2_MR[self.day_fraction]

            # clear subdaily values
            level2_Co = [-999.0] * (self.day_fraction + 1)  # .clear()
            storage2_Co = [-999.0] * (self.day_fraction + 1)  # .clear()
            level2_MR = [-999.0] * (self.day_fraction + 1)  # .clear()
            storage2_MR = [-999.0] * (self.day_fraction + 1)  # .clear()
            release2_A.clear()
            release2_B.clear()
            release2_C.clear()
            release2_D.clear()
            # level2_Co.clear() Cannot clear!!
            # storage2_Co.clear()
            # level2_MR.clear()
            # storage2_MR.clear()

        # compute objectives >> no numpy array yet
        level_Co.pop(0)
        Jhyd = sum(hydropowerRevenue_Co) / self.n_years / pow(10, 6)  # GWh/year (M$/year)
        Jatom = self.g_VolRel(release_A, self.w_atomic)
        Jbalt = self.g_VolRel(release_B, self.w_baltimore)
        Jches = self.g_VolRel(release_C, self.w_chester)
        Jenv = self.g_ShortageIndex(release_D, self.min_flow)
        Jrec = self.g_StorageReliability(storage_Co, self.h_ref_rec)
        # JJ = []
        # JJ.extend([Jhyd, Jatom, Jbalt, Jches, Jenv, Jrec])
        # utils.logVector(level_Co, "./log/hCO_base99.txt")
        # utils.logVector(release_D, "./log/rCO_base99.txt")
        # return JJ
        return Jhyd, Jatom, Jbalt, Jches, Jenv, Jrec

        # print(sum(release_B), " baltimore release")
        # JJ = []
        # JJ[year]
        # JJ.append(Jhydropower)
        # JJ.append(Jatomicpowerplant)
        # JJ.append(Jbaltimore)
        # JJ.append(Jchester)
        # JJ.append(Jrecreation)
        # JJ.append(Jenvironment)

        # outcomes = [Jhydropower,  Jatomicpowerplant, Jbaltimore, Jchester, Jrecreation, Jenvironment, Jfloodrisk, JFloodDuration]
        # outcome_names = ['Jhydropower',  'Jatomicpowerplant', 'Jbaltimore', 'Jchester', 'Jrecreation', 'Jenvironment', 'Jfloodrisk', 'JFloodDuration']
        # for i in outcome:

        # SS = []
        # SS.append(sum(hydropowerProduction_Co))
        # SS.append()

        # outcomes = [Jhydropower,  Jatomicpowerplant, Jbaltimore, Jchester, Jrecreation, Jenvironment, Jfloodrisk, JFloodDuration]

        # Jhydropower = utils.filterDictionaryPercentile(Jhydropower, 99)
        # Jatomicpowerplant = utils.filterDictionaryPercentile(Jatomicpowerplant, 99)
        # Jbaltimore = utils.filterDictionaryPercentile(Jbaltimore, 99)
        # Jchester = utils.filterDictionaryPercentile(Jchester, 99)
        # Jrecreation = utils.filterDictionaryPercentile(Jrecreation, 99)
        # Jenvironment = utils.filterDictionaryPercentile(Jenvironment, 99)
        # Jfloodrisk = utils.filterDictionaryPercentile(Jfloodrisk, 99)
        # JFloodDuration = utils.filterDictionaryPercentile(JFloodDuration, 99)

        # print("Hydropower Revenue ", Jhydropower)
        # print(JJ[0])

        # print("Atomic Power Plant")
        # print(JJ[1])

        # print("Baltimore")
        # print(JJ[2])

        # print("Chester")
        # print(JJ[3])

        # print("Recreation")
        # print(JJ[4])

        # print("Environment")
        # print(JJ[5])