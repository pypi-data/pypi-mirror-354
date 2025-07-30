import astropy
import joblib
import numpy as np


def run_DfL_ML(
    input_data_path,
    output_data_path,
    seed: int,
    data_type="fits",
    cosmology=(70, 0.3),
    model="HYBRID",
    mu=0.6,
    verbose="True",  # PAK: bools
    testing="False",
    tol=0.05,
    run_lim=10,
    zrange=None,
    N_MC=100,
    err_type=None,
):
    ## JMP: separate data loading function
    # ACCESS INPUT DATA:
    rng = np.random.default_rng(seed)
    path = input_data_path

    if data_type == "ascii":
        with ascii.read(path) as cat:
            GAL_ID = np.asarray(cat["GAL_ID"])  # INT ID
            Z_SPEC = np.asarray(cat["Z_SPEC"])  # UNITLESS
            RA = np.asarray(cat["RA"])  # Deg
            DEC = np.asarray(cat["DEC"])  # Deg
            STELLAR_MASS = np.asarray(cat["STELLAR_MASS"])  # LOG(Msun)

            if err_type == "Point":
                SMerr = np.asarray(
                    cat["STELLAR_MASS_ERROR"]
                )  # Can be point value or PDF 2D array [LOG(Msun)]
                # If 2D -- arr[0,:] = M* values; arr[1,:] = prob
            if testing == "True":
                # NOT REQUIRED (FOR TESTING ONLY):
                HALO_MASS = np.asarray(cat["HALO_MASS"])  # LOG(Msun)
                csflag = np.asarray(cat["csflag"])  # INT FLAG

    if data_type == "fits":
        with astropy.io.fits.open(path) as cat_hdu:
            cat = cat_hdu[1].data

            GAL_ID = cat.field("GAL_ID")  # INT
            Z_SPEC = cat.field("Z_SPEC")  # UNITLESS
            RA = cat.field("RA")  # Deg
            DEC = cat.field("DEC")  # Deg
            STELLAR_MASS = cat.field("STELLAR_MASS")  # LOG(Msun)

            if err_type == "Point":
                SMerr = cat.field(
                    "STELLAR_MASS_ERROR"
                )  # Can be point value or PDF array [LOG(Msun)]
                # If 2D -- arr[0,:] = M* values; arr[1,:] = prob
            if err_type == "PDF":
                SME_val = cat.field("STELLAR_MASS_VALUES")
                SME_prob = cat.field("STELLAR_MASS_PROBABILITY")

            if testing == "True":
                # NOT REQUIRED (FOR TESTING ONLY):
                HALO_MASS = cat.field("HALO_MASS")  # LOG(Msun)
                csflag = cat.field("csflag")  # INT FLAG`

    # Apply redshift cut:

    if zrange is not None:
        zl = zrange[0]
        zh = zrange[1]
        mask = (Z_SPEC >= zl) & (Z_SPEC <= zh)

        GAL_ID = GAL_ID[mask]
        Z_SPEC = Z_SPEC[mask]
        RA = RA[mask]
        DEC = DEC[mask]
        STELLAR_MASS = STELLAR_MASS[mask]

        if err_type == "Point":
            SMerr = SMerr[mask]

        if err_type == "PDF":
            SME_val = SME_val[mask]
            SME_prob = SME_prob[mask]

        if testing == "True":
            HALO_MASS = HALO_MASS[mask]
            csflag = csflag[mask]

    # DEFINE COSMOLOGY & CONSTANTS:
    ## JMP: replace with astropy.constants
    ## H0 as separate variable
    ## Om0 as separate variable

    bigG = 6.6743e-11  # log Nm^2/Kg^2
    speed_of_light = 2.998e5  # km/s
    mass_of_sun = 1.99e30  # kg
    mu_g = 0.6  # unitless
    mp = 1.673e-27  # kg
    KB = 1.380649e-23  # J/K

    H0 = cosmology[0]  # km/s / Mpc
    Om0 = cosmology[1]
    Ol0 = 1 - Om0

    # Define Hubble Parameter H(z):
    ## JMP: first off, there already exist functions in astropy to calculate H(z)
    ## JMP: second, one can use astropy units to convert between km/s/Mpc and s^-1
    H_z = H0 * np.sqrt(Om0 * (1 + Z_SPEC) ** 3 + Ol0)  # km/s/Mpc
    H_z = H_z / 3.086e19  # s^(-1)

    # Determine D_A(z), D_L(z) & D_c(z):
    ## JMP: again, astropy has functions to calculate D_A(z), D_L(z) and D_c(z)
    ## JMP: and it's also a bit confusing why Asa chooses to use already existing
    ## JMP: functionality at random. Especially when he didn't test for performance
    ## JMP: differences between the astropy functions and his own implementation
    cosmo = cosmology.FlatLambdaCDM(H0=H0, Om0=Om0)
    DA = np.asarray(cosmo.angular_diameter_distance(Z_SPEC))  # Mpc/rad
    DA = DA * 17.4533  # kpc/deg
    DL = np.asarray(cosmo.luminosity_distance(Z_SPEC))  # Mpc
    DC = np.asarray(cosmo.comoving_distance(Z_SPEC))  # Mpc

    # SELECT SIMULATION:
    ## JMP: Asa uses joblib to save and load his pretrained models

    if (model == "EAGLE") | (model == "TNG"):
        my_sim = model
        My_Central_Regression_Model = (
            "MODELS/RF_reg_model-cen-zall" + "-" + my_sim + "-adv.joblib"
        )
        My_Group_Regression_Model = (
            "MODELS/RF_reg_model-all-zall" + "-" + my_sim + "-adv.joblib"
        )

    elif model == "HYBRID":
        My_Central_Regression_Model_TNG = (
            "MODELS/RF_reg_model-cen-zall" + "-" + "TNG-adv.joblib"
        )
        My_Central_Regression_Model_EAGLE = (
            "MODELS/RF_reg_model-cen-zall" + "-" + "EAGLE-adv.joblib"
        )
        My_Group_Regression_Model_TNG = (
            "MODELS/RF_reg_model-all-zall" + "-" + "TNG-adv.joblib"
        )
        My_Group_Regression_Model_EAGLE = (
            "MODELS/RF_reg_model-all-zall" + "-" + "EAGLE-adv.joblib"
        )

    # Define output params from while loops:
    sentinel = -999
    size = GAL_ID.size

    GID_pred = np.full(size, sentinel)
    N_gal_pred = np.full(size, sentinel)
    Mh_pred = np.full(size, sentinel)
    Mh_pred_cenonly = np.full(size, sentinel)
    GTM_pred = np.full(size, sentinel)
    csflag_pred = np.full(size, sentinel)
    R_vir_pred = np.full(size, sentinel)
    V_vir_pred = np.full(size, sentinel)
    T_vir_pred = np.full(size, sentinel)
    Dc_pred = np.full(size, sentinel)
    flag_cen = np.full(size, sentinel)
    Nrun = np.full(size, sentinel)
    Mh_errp = np.full(size, sentinel)
    Mh_errn = np.full(size, sentinel)
    Mh_errpp = np.full(size, sentinel)
    Mh_errnn = np.full(size, sentinel)

    Mh_PDF_prob = np.full((size, 80), sentinel)
    Mh_PDF_bin_centers = np.full((size, 80), sentinel)

    # Initialize Group Info:

    groupID = 0
    Ngal_to_fit = len(GAL_ID)

    PDF_binsize = (15 - 11) / 0.05
    convergence_limit = tol
    run_limit = run_lim  ## JMP: why?
    N_MC = N_MC  ## JMP: why?

    ##################################
    #                                #
    # BEGIN GROUP FINDING ALGORITHM: #
    #                                #
    ##################################

    # While there are galaxies not sorted into groups...

    while Ngal_to_fit > 0:
        groupID = groupID + 1  ## JMP: this is a bit odd, why start group ID at 1?

        if verbose == "True":
            print("Running Group: ", groupID)

        # Remove known groups from loop:

        mask_to_fit = (
            GID_pred == -999
        )  ## JMP: that a good typing practice? Read confusing at first

        gGAL_ID = GAL_ID[mask_to_fit]
        gRA = RA[mask_to_fit]
        gDEC = DEC[mask_to_fit]
        gZ_SPEC = Z_SPEC[mask_to_fit]
        gSTELLAR_MASS = STELLAR_MASS[mask_to_fit]
        gDA = DA[mask_to_fit]

        ## JMP: we have to do something about those extra if statements. Unnecessary
        if err_type == "Point":
            gSMerr = SMerr[mask_to_fit]

        if err_type == "PDF":
            gSME_val = SME_val[mask_to_fit]
            gSME_prob = SME_prob[mask_to_fit]

        if testing == "True":
            gHALO_MASS = HALO_MASS[mask_to_fit]

        if verbose == "True":
            print("Number of Galaxies Remaining to Assign: ", len(gGAL_ID))

        # Identify Most Mass Galaxy (MMG) remaining in sample:

        ## JMP: NO. That's a ~9GB array for a 1e9 galaxy dataset.
        ## JMP: argmax instead
        ids = gSTELLAR_MASS.argsort()
        MMG_ID = gGAL_ID[ids[::-1]][0]

        # Extract Properties of MMG:
        MMG_GAL_ID = gGAL_ID[gGAL_ID == MMG_ID][
            0
        ]  ## JMP: why the double indexing? PAK: unsafe reshape
        MMG_RA = gRA[gGAL_ID == MMG_ID][0]
        MMG_DEC = gDEC[gGAL_ID == MMG_ID][0]
        MMG_Z_SPEC = gZ_SPEC[gGAL_ID == MMG_ID][0]
        MMG_STELLAR_MASS = gSTELLAR_MASS[gGAL_ID == MMG_ID][0]
        MMG_DA = gDA[gGAL_ID == MMG_ID][0]

        if err_type == "Point":
            MMG_SMerr = gSMerr[gGAL_ID == MMG_ID][0]

        if err_type == "PDF":
            MMG_SME_val = gSME_val[gGAL_ID == MMG_ID][0, :]
            MMG_SME_prob = gSME_prob[gGAL_ID == MMG_ID][0, :]

        if testing == "True":
            MMG_HALO_MASS = gHALO_MASS[gGAL_ID == MMG_ID][0]

        ##################################
        #                                #
        #        FIRST STAGE:            #
        #                                #
        ##################################

        # Estimate Mhalo(M*|cen)

        cen_input1 = np.zeros((1, 2))
        cen_input1[0, 0] = MMG_STELLAR_MASS
        cen_input1[0, 1] = MMG_Z_SPEC

        if (model == "TNG") | (model == "EAGLE"):
            # Load RF Regression Model for Centrals:
            cen_reg = joblib.load(My_Central_Regression_Model)

            # Predict Central Halo Mass:
            Mh_est = cen_reg.predict(cen_input1)[0]

        elif model == "HYBRID":
            # Load RF Regression Models for Centrals:
            cen_reg_a = joblib.load(My_Central_Regression_Model_TNG)
            cen_reg_b = joblib.load(My_Central_Regression_Model_EAGLE)

            # Predict Central Halo Mass:
            Mh_est_a = cen_reg_a.predict(cen_input1)[0]
            Mh_est_b = cen_reg_b.predict(cen_input1)[0]
            Mh_est = (Mh_est_a + Mh_est_b) / 2  # Average of TNG & EAGLE estimates

        if (verbose == "True") & (testing == "True"):
            print("Actual Halo Mass: ", MMG_HALO_MASS)  # JUST FOR TESTING-MODE
            print("Initial Predicted Halo Mass: ", Mh_est)

        # Store initial halo mass estimate:
        Mh_est_cen = Mh_est.copy()

        ##################################
        #                                #
        #        SECOND STAGE:           #
        #                                #
        ##################################

        # Prep for SECOND STAGE -- Group Regression:
        cen_input2 = np.zeros((N_MC, 4))

        # Initialize parameters for loop:
        Diff_Mh = 1
        run_no = 0
        Mh_est_OLD = Mh_est.copy()
        Mh_est_final = -999
        R_group_final = -999
        GTM_est_final = -999
        V_vir_final = -999

        # While there is lack of convergence in halo mass estimates...

        while (Diff_Mh > convergence_limit) & (run_no < run_limit):
            run_no = run_no + 1

            if verbose == "True":
                print("Iteration No. ", run_no)

            # Compute Virial Radius, Virial Velocity & Virial Temperature:

            my_Hz = np.log10(H_z[GAL_ID == MMG_GAL_ID])  # log(s^-1)
            Mh_kg = Mh_est_OLD + np.log10(mass_of_sun)  # log(Kg)
            R_group_m = (1 / 3) * (
                np.log10(bigG) + Mh_kg - np.log10(100) - 2 * my_Hz
            )  # log(m)
            R_group = 10 ** (R_group_m - 19 - np.log10(3.086))  # kpc

            V_vir = 10 ** (0.5 * (np.log10(bigG) + Mh_kg - R_group_m)) / 1000  # km/s

            T_vir = (
                np.log10(mu_g)
                + np.log10(mp)
                + 2 * np.log10(V_vir * 1000)
                - np.log10(2)
                - np.log10(KB)
            )  # log(K)

            # Extract Group Info:
            ## JMP: shouldn't we just translate angular+redshift sky coordinates
            # into cartesian
            ## JMP: in comoving coordinates and then build a KDTree?
            ## JMP: this way we'll be O(NlogN) instead of O(N^2).
            # Construct angular distance to each galaxy from MMG (Haversine Formula):
            ang_sep = 2 * np.arcsin(
                np.sqrt(
                    (np.sin(np.deg2rad((MMG_DEC - DEC) / 2))) ** 2
                    + np.cos(np.deg2rad(MMG_DEC))
                    * np.cos(np.deg2rad(DEC))
                    * (np.sin(np.deg2rad((MMG_RA - RA) / 2))) ** 2
                )
            )  # RAD

            ang_sep = np.rad2deg(ang_sep)

            # Convert to Physical kpc with DA(z):
            dist2D = ang_sep * MMG_DA  # kpc (phys)

            # Constrct absolute radial velocity difference between
            # each galaxy and the MMG:

            vel_diff = np.abs(
                speed_of_light * (MMG_Z_SPEC - Z_SPEC) / (1 + (MMG_Z_SPEC + Z_SPEC) / 2)
            )  # |km/s|

            # Define group members as those within 1R_200 and 1V_200,
            # not already placed in another group:
            ## JMP: ask Asa if we need separate conditions on RA, DEC and redshift.
            group_mask = (
                (dist2D <= 1 * R_group) & (vel_diff <= 1 * V_vir) & (GID_pred == -999)
            )

            # Define Group Inputs for RF Regressor:
            Ng_est = len(STELLAR_MASS[group_mask])
            GTM_est = np.log10(np.sum(10 ** STELLAR_MASS[group_mask]))

            # MC Analysis of stellar mass -> halo mass errors:

            if err_type is None:
                cTM_input = MMG_STELLAR_MASS
                GTM_input = GTM_est

            elif err_type == "Point":
                # Propegate SMerr to group SMerr:
                ## AFLB: positive error in linear units
                ## AFLB: all good for positive errors. Do the same for negative errors
                group_err_lin_list = (
                    10 ** (STELLAR_MASS[group_mask] + SMerr[group_mask])
                    - 10 ** (STELLAR_MASS[group_mask])
                )

                group_err_lin = np.sqrt(np.sum(group_err_lin_list) ** 2)
                GTM_err_p = np.log10(10**GTM_est + group_err_lin) - np.log10(
                    10**GTM_est
                )
                GTM_err_n = np.log10(10**GTM_est) - np.log10(
                    10**GTM_est - group_err_lin
                )
                GTM_err = (GTM_err_p + GTM_err_n) / 2

                # MC Analysis of stellar mass -> halo mass errors:
                GTM_input = rng.normal(GTM_est, GTM_err, N_MC)
                cTM_input = rng.normal(MMG_STELLAR_MASS, MMG_SMerr, N_MC)

                """
                # Useful Test:
                if(Ng_est > 5):
                    print('TEST 1 : ', GTM_est, np.mean(GTM_input), np.std(GTM_input))
                    print('TEST 2 : ', MMG_STELLAR_MASS, np.mean(cTM_input), 
                                        np.std(cTM_input))
                """

            elif err_type == "PDF":
                val = MMG_SME_val
                prob = MMG_SME_prob

                ## AFLB: checking to make sure that it's interpretable as a PDF
                ## Catch as an error at runtime?
                prob = prob / np.sum(prob)

                ## JMP: replace with inverse sampling
                cTM_input = rng.choice(val, size=N_MC, p=prob)

                GTM_input = np.zeros(N_MC)

                for i in range(len(Z_SPEC[group_mask])):
                    PDF_val = SME_val[group_mask][i, :]
                    PDF_prob = SME_prob[group_mask][i, :]

                    ## JMP: fix logic (not an error, just clarity)
                    ## JMP: all stellar masses summed within draws from their PDFs
                    ## JMP: it's an iterative sum starting with GTM_input=0
                    ## JMP: replace with bulk inverse sampling for
                    GTM_input = np.log10(
                        10**GTM_input + 10 ** rng.choice(PDF_val, size=N_MC, p=PDF_prob)
                    )

            # SET RF INPUT:
            ## JMP: watch out, depending on err_type switch you have different dtype
            ## JMP: TYPSETTING!!@!@!@!
            cen_input2[:, 0] = cTM_input
            cen_input2[:, 1] = GTM_input
            cen_input2[:, 2] = cTM_input * 0 + Ng_est
            cen_input2[:, 3] = cTM_input * 0 + MMG_Z_SPEC

            # RUN Group RF Model:

            if (model == "TNG") | (model == "EAGLE"):
                # Load RF Regression Model for Groups:
                all_reg = joblib.load(My_Group_Regression_Model)

                # Predict New Halo Mass from Goup Parameters:
                Mh_est_new_list = all_reg.predict(cen_input2)

                # Extract predictions from individual trees:
                all_predictions = np.array(
                    [tree.predict(cen_input2) for tree in all_reg.estimators_]
                )
                tree_predictions = (
                    all_predictions.flatten()
                )  # Shape: (num_trees * N_MC,)

                # Define prediction as mean of all tree predictions:
                Mh_est_new = np.mean(tree_predictions)

                # Compute 1 & 2 sig point errors:
                sorted_tree_predictions = np.sort(tree_predictions)
                Ntrees = len(tree_predictions)

                ## JMP: use np.percentile instead of sorting
                Mh_med = sorted_tree_predictions[int(0.5 * Ntrees)]
                Mh_up = sorted_tree_predictions[int(0.84 * Ntrees)]
                Mh_low = sorted_tree_predictions[int(0.16 * Ntrees)]
                Mh_uup = sorted_tree_predictions[int(0.975 * Ntrees)]
                Mh_llow = sorted_tree_predictions[int(0.025 * Ntrees)]

                # Compute PDF:
                ## JMP: from percentiles
                PDF_bins = np.arange(11, 15.01, 0.05)  # 80 bins
                PDF_counts, PDF_bin_edges = np.histogram(
                    tree_predictions, bins=PDF_bins
                )
                PDF_counts = PDF_counts / np.sum(PDF_counts)
                PDF_bin_centers = (PDF_bins + (PDF_bins[1] - PDF_bins[0]) / 2)[:-1]

            elif model == "HYBRID":
                # Load RF Regression Models for Groups:
                all_reg_a = joblib.load(My_Group_Regression_Model_TNG)
                all_reg_b = joblib.load(My_Group_Regression_Model_EAGLE)

                # Predict New Halo Mass from Group Parameters:
                Mh_est_new_list_a = all_reg_a.predict(cen_input2)
                Mh_est_new_list_b = all_reg_b.predict(cen_input2)
                Mh_est_new_list = (
                    Mh_est_new_list_a + Mh_est_new_list_b
                ) / 2  # Average of EAGLE & TNG estimates

                # Extract predictions from individual trees:
                all_predictions_a = np.array(
                    [tree.predict(cen_input2) for tree in all_reg_a.estimators_]
                )
                tree_predictions_a = (
                    all_predictions_a.flatten()
                )  # Shape: (num_trees * N_MC,)
                all_predictions_b = np.array(
                    [tree.predict(cen_input2) for tree in all_reg_b.estimators_]
                )
                tree_predictions_b = (
                    all_predictions_b.flatten()
                )  # Shape: (num_trees * N_MC,)
                tree_predictions = np.concatenate(
                    (tree_predictions_a, tree_predictions_b)
                )

                # Define prediction as mean of all tree predictions:
                Mh_est_new = np.mean(tree_predictions)

                # Compute 1 & 2 sig point errors:
                sorted_tree_predictions = np.sort(tree_predictions)
                Ntrees = len(tree_predictions)
                Mh_med = sorted_tree_predictions[int(0.5 * Ntrees)]
                Mh_up = sorted_tree_predictions[int(0.84 * Ntrees)]
                Mh_low = sorted_tree_predictions[int(0.16 * Ntrees)]
                Mh_uup = sorted_tree_predictions[int(0.975 * Ntrees)]
                Mh_llow = sorted_tree_predictions[int(0.025 * Ntrees)]

                # Compute PDF:
                PDF_bins = np.arange(11, 15.01, 0.05)  # 80 bins
                PDF_counts, PDF_bin_edges = np.histogram(
                    tree_predictions, bins=PDF_bins
                )
                PDF_counts = PDF_counts / np.sum(PDF_counts)
                PDF_bin_centers = (PDF_bins + (PDF_bins[1] - PDF_bins[0]) / 2)[:-1]

            # Define iteration difference:
            Diff_Mh = np.abs(Mh_est_new - Mh_est_OLD)

            # Save best versions:

            if (Diff_Mh < convergence_limit) | (run_no == run_limit):
                Mh_est_final = Mh_est_OLD
                GTM_est_final = GTM_est
                Ng_est_final = Ng_est
                R_group_final = R_group
                V_vir_final = V_vir
                T_vir_final = T_vir
                run_no_final = run_no
                Mh_med_final = Mh_med
                Mh_up_final = Mh_up
                Mh_low_final = Mh_low
                Mh_uup_final = Mh_uup
                Mh_llow_final = Mh_llow
                run_no_final = run_no
                PDF_counts_final = PDF_counts
                PDF_bin_centers_final = PDF_bin_centers

            # Re-set base halo mass estimate to new version:
            Mh_est_OLD = Mh_est_new.copy()

        if verbose == "True":
            print("Final Predicted Halo Mass: ", Mh_est_final)

        # Collate info for centrals & core satellites:

        # Construct angular distance to each galaxy from MMG (Haversine Formula):
        ang_sep = 2 * np.arcsin(
            np.sqrt(
                (np.sin(np.deg2rad((MMG_DEC - DEC) / 2))) ** 2
                + np.cos(np.deg2rad(MMG_DEC))
                * np.cos(np.deg2rad(DEC))
                * (np.sin(np.deg2rad((MMG_RA - RA) / 2))) ** 2
            )
        )  # RAD

        ang_sep = np.rad2deg(ang_sep)

        # Convert to Physical kpc with DA(z):
        dist2D = ang_sep * MMG_DA  # kpc (phys)

        # Constrct absolute radial velocity difference between each galaxy and the MMG:
        vel_diff = np.abs(
            speed_of_light * (MMG_Z_SPEC - Z_SPEC) / (1 + (MMG_Z_SPEC + Z_SPEC) / 2)
        )  # |km/s|

        # Define core group members as D < 1R_200; DV < 1V_200;
        # that are not already set in a group:
        group_mask = (
            (dist2D <= 1 * R_group_final)
            & (vel_diff <= 1 * V_vir_final)
            & (GID_pred == -999)
        )

        GID_pred[group_mask] = groupID
        GTM_pred[group_mask] = GTM_est_final
        Mh_pred[group_mask] = Mh_est_final
        Mh_pred_cenonly[group_mask] = Mh_est_cen
        R_vir_pred[group_mask] = R_group_final
        V_vir_pred[group_mask] = V_vir_final
        T_vir_pred[group_mask] = T_vir_final
        N_gal_pred[group_mask] = Ng_est_final
        csflag_pred[(group_mask) & (STELLAR_MASS == STELLAR_MASS[group_mask].max())] = 1
        csflag_pred[(group_mask) & (STELLAR_MASS < STELLAR_MASS[group_mask].max())] = 0
        Nrun[group_mask] = run_no_final
        Mh_PDF_prob[group_mask, :] = PDF_counts_final
        Mh_PDF_bin_centers[group_mask, :] = PDF_bin_centers_final
        Mh_errp[group_mask] = Mh_up_final - Mh_med_final
        Mh_errn[group_mask] = Mh_med_final - Mh_low_final
        Mh_errpp[group_mask] = Mh_uup_final - Mh_med_final
        Mh_errnn[group_mask] = Mh_med_final - Mh_llow_final

        # Add buffer of potential satellites/ ambiguous region
        # (D < 2R_200; DV < 2V-200):

        ext_group_mask = (
            (dist2D > 1 * R_group_final)
            & (dist2D < 2 * R_group_final)
            & (vel_diff < 2 * V_vir_final)
            & (GID_pred == -999)
        ) | (
            (dist2D <= 1 * R_group_final)
            & (vel_diff > 1 * V_vir_final)
            & (vel_diff < 2 * V_vir_final)
            & (GID_pred == -999)
        )

        GID_pred[ext_group_mask] = groupID
        GTM_pred[ext_group_mask] = GTM_est_final
        Mh_pred[ext_group_mask] = Mh_est_final
        Mh_pred_cenonly[ext_group_mask] = Mh_est_cen
        R_vir_pred[ext_group_mask] = R_group_final
        V_vir_pred[ext_group_mask] = V_vir_final
        T_vir_pred[ext_group_mask] = T_vir_final
        N_gal_pred[ext_group_mask] = Ng_est_final
        csflag_pred[ext_group_mask] = -1
        Nrun[ext_group_mask] = run_no_final
        Mh_PDF_prob[ext_group_mask, :] = PDF_counts_final
        Mh_PDF_bin_centers[ext_group_mask, :] = PDF_bin_centers_final
        Mh_errp[ext_group_mask] = Mh_up_final - Mh_med_final
        Mh_errn[ext_group_mask] = Mh_med_final - Mh_low_final
        Mh_errpp[ext_group_mask] = Mh_uup_final - Mh_med_final
        Mh_errnn[ext_group_mask] = Mh_med_final - Mh_llow_final

        # Update to-fit list:

        Ngal_to_fit = len(gGAL_ID) - len(GAL_ID[GID_pred == groupID])

    # Output Halo Catalog (FITS FORMAT):

    output_path = output_data_path

    if testing == "True":
        delta_Mh = HALO_MASS - Mh_pred
        PDF_format = "80D"

        col0 = astropy.io.fits.Column(name="GAL_ID", format="K", array=GAL_ID)
        col1 = astropy.io.fits.Column(name="Z_SPEC", format="E", array=Z_SPEC)
        col2 = astropy.io.fits.Column(name="RA", format="E", array=RA)
        col3 = astropy.io.fits.Column(name="DEC", format="E", array=DEC)
        col4 = astropy.io.fits.Column(
            name="STELLAR_MASS", format="E", array=STELLAR_MASS
        )
        col5 = astropy.io.fits.Column(name="HALO_MASS", format="E", array=HALO_MASS)
        col6 = astropy.io.fits.Column(name="csflag", format="E", array=csflag)
        col7 = astropy.io.fits.Column(name="GID_pred", format="K", array=GID_pred)
        col8 = astropy.io.fits.Column(name="GTM_pred", format="E", array=GTM_pred)
        col9 = astropy.io.fits.Column(name="N_gal_pred", format="E", array=N_gal_pred)
        col10 = astropy.io.fits.Column(name="Mh_pred", format="E", array=Mh_pred)
        col11 = astropy.io.fits.Column(name="Mh_err_1sig_p", format="E", array=Mh_errp)
        col12 = astropy.io.fits.Column(name="Mh_err_1sig_n", format="E", array=Mh_errn)
        col13 = astropy.io.fits.Column(name="Mh_err_2sig_p", format="E", array=Mh_errpp)
        col14 = astropy.io.fits.Column(name="Mh_err_2sig_n", format="E", array=Mh_errnn)
        col15 = astropy.io.fits.Column(
            name="Mh_PDF_prob", format=PDF_format, array=Mh_PDF_prob
        )
        col16 = astropy.io.fits.Column(
            name="Mh_PDF_bin_centers", format=PDF_format, array=Mh_PDF_bin_centers
        )
        col17 = astropy.io.fits.Column(name="R_vir_pred", format="E", array=R_vir_pred)
        col18 = astropy.io.fits.Column(name="V_vir_pred", format="E", array=V_vir_pred)
        col19 = astropy.io.fits.Column(name="T_vir_pred", format="E", array=T_vir_pred)
        col20 = astropy.io.fits.Column(
            name="csflag_pred", format="E", array=csflag_pred
        )
        col21 = astropy.io.fits.Column(name="delta_Mh", format="E", array=delta_Mh)
        col22 = astropy.io.fits.Column(name="Nrun", format="E", array=Nrun)
        col23 = astropy.io.fits.Column(
            name="Mh_pred_cenonly", format="E", array=Mh_pred_cenonly
        )

        newcols = astropy.io.fits.ColDefs(
            [
                col0,
                col1,
                col2,
                col3,
                col4,
                col5,
                col6,
                col7,
                col8,
                col9,
                col10,
                col11,
                col12,
                col13,
                col14,
                col15,
                col16,
                col17,
                col18,
                col19,
                col20,
                col21,
                col22,
                col23,
            ]
        )

        hdu_file = astropy.io.fits.BinTableHDU.from_columns(newcols)

        hdu_file.writeto(output_path, overwrite=True)

    else:
        PDF_format = "80D"

        col0 = astropy.io.fits.Column(name="GAL_ID", format="K", array=GAL_ID)
        col1 = astropy.io.fits.Column(name="Z_SPEC", format="E", array=Z_SPEC)
        col2 = astropy.io.fits.Column(name="RA", format="E", array=RA)
        col3 = astropy.io.fits.Column(name="DEC", format="E", array=DEC)
        col4 = astropy.io.fits.Column(
            name="STELLAR_MASS", format="E", array=STELLAR_MASS
        )
        col5 = astropy.io.fits.Column(name="GID_pred", format="K", array=GID_pred)
        col6 = astropy.io.fits.Column(name="GTM_pred", format="E", array=GTM_pred)
        col7 = astropy.io.fits.Column(name="N_gal_pred", format="E", array=N_gal_pred)
        col8 = astropy.io.fits.Column(name="Mh_pred", format="E", array=Mh_pred)
        col9 = astropy.io.fits.Column(name="Mh_err_1sig_p", format="E", array=Mh_errp)
        col10 = astropy.io.fits.Column(name="Mh_err_1sig_n", format="E", array=Mh_errn)
        col11 = astropy.io.fits.Column(name="Mh_err_2sig_p", format="E", array=Mh_errpp)
        col12 = astropy.io.fits.Column(name="Mh_err_2sig_n", format="E", array=Mh_errnn)
        col13 = astropy.io.fits.Column(
            name="Mh_PDF_prob", format=PDF_format, array=Mh_PDF_prob
        )
        col14 = astropy.io.fits.Column(
            name="Mh_PDF_bin_centers", format=PDF_format, array=Mh_PDF_bin_centers
        )
        col15 = astropy.io.fits.Column(name="R_vir_pred", format="E", array=R_vir_pred)
        col16 = astropy.io.fits.Column(name="V_vir_pred", format="E", array=V_vir_pred)
        col17 = astropy.io.fits.Column(name="T_vir_pred", format="E", array=T_vir_pred)
        col18 = astropy.io.fits.Column(
            name="csflag_pred", format="E", array=csflag_pred
        )
        col19 = astropy.io.fits.Column(name="Nrun", format="E", array=Nrun)
        col20 = astropy.io.fits.Column(
            name="Mh_pred_cenonly", format="E", array=Mh_pred_cenonly
        )

        newcols = astropy.io.fits.ColDefs(
            [
                col0,
                col1,
                col2,
                col3,
                col4,
                col5,
                col6,
                col7,
                col8,
                col9,
                col10,
                col11,
                col12,
                col13,
                col14,
                col15,
                col16,
                col17,
                col19,
                col20,
            ]
        )

        hdu_file = astropy.io.fits.BinTableHDU.from_columns(newcols)

        hdu_file.writeto(output_path, overwrite=True)
