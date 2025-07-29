import pandas as pd
import os
import numpy as np
import tempfile
import shutil
import re
from itertools import chain


def pet_raft_scriptor(file_path):
    file_path_sheet = file_path
    data_file = pd.read_excel(file_path, sheet_name=None)

    # Step 1: Create temp folder near input file
    root_dir = os.path.dirname(file_path)
    temp_folder = tempfile.mkdtemp(dir=root_dir)

    print(f"📂 Temporary folder created at: {temp_folder}")
    try:
        copolymer = len(data_file) > 1
        if copolymer:
            data = {"Sheet1": data_file[list(data_file.keys())[0]]}
            monomer_df = data_file.get(list(data_file.keys())[1], None)
            user_stocks_df = data_file.get(list(data_file.keys())[2], None)
            unique_monomers = get_unique_monomers(data_file)
        else:
            data = data_file
            monomer_df = None
            user_stocks_df = None

        # 2

        # The row parameter is used to match polymer ID in polymer sheet however if sample from that sheet
        # Then the polymer ID wont be the same as the "row" entry so for now chanfed the "row" to be same value as polymer ID

        def calculate_polymer_volume_updated(df):
            results = []
            for index, row in df.iterrows():
                total_volume = 0
                details = {}
                # Calculate the volume needed for the monomer to achieve the final desired concentration
                monomer_volume = (
                    row["Monomer"] * row["Mf"] / row["Monomer"] * row["Volume"]
                ) / row["[M]"]
                details["Monomer"] = monomer_volume
                total_volume += monomer_volume

                # Check other components based on their feed ratios
                component_to_column = {"CTA": "[CTA]", "photo catalyst": "[PC]"}
                # This wasnt changed so therefore the calculation wouldnt have been affected for final ratios for things made beofre seems (01152025)
                # As monomer_volume = (row['Mf'] * row['Volume']) / row['[M]'] this was equation since stocks were 2M, (1000mM)*200/2000 = 100 so got lucky it would have been same for DP 200 since same as vol
                for component, concentration_column in component_to_column.items():
                    # First find the final concentration of reagent
                    cf = row[component] * row["Mf"] / row["Monomer"]
                    required_volume = (cf * row["Volume"]) / row[concentration_column]
                    total_volume += required_volume
                    details[component] = required_volume

                # Calculate the solvent volume required to reach the final volume if total component volumes are less
                if total_volume < row["Volume"]:
                    solvent_volume = row["Volume"] - total_volume
                    details["Solvent"] = solvent_volume
                    total_volume += solvent_volume
                else:
                    details["Solvent"] = 0

                # Check if the total volume needed is within the desired final volume and all volumes are above 5 µL

                can_be_made = total_volume <= row["Volume"] and all(
                    v >= 5 for v in details.values()
                )
                results.append(
                    {
                        "Row": row["Polymer ID"],
                        "Can be made?": "Yes" if can_be_made else "No",
                        "Total Volume Needed": total_volume,
                        "Details": details,
                    }
                )

            return results

        # Run the updated function with the new data
        updated_calculate_results = calculate_polymer_volume_updated(data["Sheet1"])
        updated_calculate_results
        polymer_sheet_analysis_df = pd.DataFrame(updated_calculate_results)
        polymers_needing_reag_adjust = polymer_sheet_analysis_df[
            polymer_sheet_analysis_df["Can be made?"] == "Yes"
        ].reset_index(drop=True)

        # 3

        # initializing volumes of reagents
        monomer_vol_needed = 0
        cta_vol_needed = 0
        pc_vol_needed = 0
        solvent_vol_needed = 0

        for current in range(len(polymers_needing_reag_adjust["Can be made?"])):
            # adding vol for each row
            monomer_vol_needed = (
                monomer_vol_needed
                + polymers_needing_reag_adjust["Details"][current]["Monomer"]
            )
            cta_vol_needed = (
                cta_vol_needed + polymers_needing_reag_adjust["Details"][current]["CTA"]
            )
            pc_vol_needed = (
                pc_vol_needed
                + polymers_needing_reag_adjust["Details"][current]["photo catalyst"]
            )
            solvent_vol_needed = (
                solvent_vol_needed
                + polymers_needing_reag_adjust["Details"][current]["Solvent"]
            )

        reagent_concentrations = {
            "[CTA]": user_stocks_df["CTA"].dropna().tolist(),
            "[PC]": user_stocks_df["PC"].dropna().tolist(),
        }

        # 4

        # function looking at mult concentrations v3 --issue must be here bc no combination should be chosen if
        # this doesnt meet the criteria overall works but just went through the possible combinations for
        # Issue is that you're dumb and forgot to include the initiator volume

        # If sampling polymer ID wont match row so for now changed that to polymer ID too

        def calculate_polymer_volume_with_detailed_combinations(
            df, reagent_concentrations
        ):
            import numpy as np
            import itertools

            results = []
            # Iterate over each row in the dataframe
            for index, row in df.iterrows():
                # print('Row------')
                possible_cta = []
                possible_pc = []
                valid_combinations = []

                # Generate all combinations of reagents
                metal_options = reagent_concentrations["[CTA]"]
                pc_options = reagent_concentrations["[PC]"]

                all_combinations = list(itertools.product(metal_options, pc_options))

                # Check each combination
                for cta_conc, pc_conc in all_combinations:
                    CTA_volume = (
                        row["Volume"]
                        * (row["CTA"] * (row["Mf"] / row["Monomer"]))
                        / cta_conc
                    )
                    pc_volume = (
                        row["Volume"]
                        * (row["photo catalyst"] * (row["Mf"] / row["Monomer"]))
                        / pc_conc
                    )
                    monomer_volume = (
                        row["Volume"]
                        * (row["Monomer"] * (row["Mf"] / row["Monomer"]))
                        / row["[M]"]
                    )

                    CTA_Volume = (
                        row["Volume"]
                        * (row["CTA"] * (row["Mf"] / row["Monomer"]))
                        / row["[CTA]"]
                    )
                    total_volume = CTA_volume + pc_volume + monomer_volume
                    solvent_volume = 200 - total_volume
                    # Added 01152025 working on proposal as solvent volume wasnt accounted in total vol in this step which would cause the ratios to be wrong
                    if solvent_volume > 0 or solvent_volume == 0:
                        total_volume = total_volume + solvent_volume
                    if solvent_volume < 0:
                        total_volume = 1000
                    # End of addition on 01152025

                    if total_volume <= row["Volume"] and all(
                        v >= 5 for v in [CTA_volume, pc_volume, solvent_volume]
                    ):
                        # print('Solvent accepted')
                        # print(solvent_volume)
                        valid_combinations.append(f"[{cta_conc}, {pc_conc}]")
                        possible_cta.append(cta_conc)
                        possible_pc.append(pc_conc)

                # Append the results for this row to the list
                results.append(
                    {
                        "Row": row[
                            "Polymer ID"
                        ],  # Same thing here turned row into polymer ID as wont match for a sampled polymer sheet
                        "p[CTA]": ", ".join(map(str, set(possible_cta)))
                        if possible_cta
                        else np.nan,
                        "p[PC]": ", ".join(map(str, set(possible_pc)))
                        if possible_pc
                        else np.nan,
                        "Combination Details": "; ".join(valid_combinations),
                    }
                )

            # Create a dataframe from results
            return pd.DataFrame(results)

        # Assuming the reagent_concentrations dictionary and data dataframe have been defined
        # Run the function
        updated_combination_results = (
            calculate_polymer_volume_with_detailed_combinations(
                data["Sheet1"], reagent_concentrations
            )
        )
        updated_combination_results.dropna()  # .reset_index(drop=True)

        # Now need to go through all the combinations and see whcih appear the most, and choose for each polymer
        # the combination that will be used, the combination chosen should be the one that
        # can be used for most, unless this sample only has a combination that works. After that need to find
        # out the volume of each of the concentrations that will be used to know how much of each to make
        # and whether to add this to a SmT or to well plate

        # 5

        from collections import Counter
        # Now need to go through all the combinations and see whcih appear the most, and choose for each polymer
        # the combination that will be used, the combination chosen should be the one that
        # can be used for most, unless this sample only has a combination that works. After that need to find
        # out the volume of each of the concentrations that will be used to know how much of each to make
        # and whether to add this to a SmT or to well plate

        # Splitting the 'Combination Details' into a list of combinations, flattening the list
        unique_combinations = set(
            combination.strip()  # Remove any surrounding whitespace
            for sublist in updated_combination_results["Combination Details"]
            for combination in sublist.split(";")  # Split each entry into combinations
            if combination.strip()  # Ensure the combination is not empty
        )

        # Looking through all combinations and seeing frequency they appear
        # So then can choose the combinations that appear most so can make less stock solutions

        # Flatten all combinations into a single list
        all_combinations = []
        for combinations in updated_combination_results["Combination Details"]:
            all_combinations.extend(combinations.split("; "))

        # Count each unique combination
        combination_counts = Counter(all_combinations)

        # Now going through the dataframe and looking at the possible combinations
        # Here we will make a decision of which to use for a certain polymer
        def select_best_combination(row, combination_counts):
            # Split the combinations in the row
            combinations = row["Combination Details"].split("; ")
            # If only one combination, return it
            if len(combinations) == 1:
                return combinations[0]
            # Find the combination with the highest count
            most_frequent_combination = max(
                combinations, key=lambda x: combination_counts[x]
            )
            return most_frequent_combination

        # Apply the function to each row in the DataFrame
        updated_combination_results["Best Combination"] = (
            updated_combination_results.apply(
                lambda row: select_best_combination(row, combination_counts), axis=1
            )
        )

        # Display the updated DataFrame with the best combination for each polymer

        updated_combination_results_wo_Na = updated_combination_results.dropna()
        updated_combination_results_wo_Na.reset_index(drop=True)

        # 6

        import numpy as np
        # Now making a new polymer sheet where we will update the stock concentration of each
        # reagent that will be used based on the chosen best combination, this will be later used to determine
        # what volume of each reagent at a given concentration is necessary (+ some extra for buffer)

        # Merge the best combinations into the original DataFrame based on 'Polymer ID' ('Row for best combs df)
        df = data["Sheet1"].merge(
            updated_combination_results_wo_Na,
            left_on="Polymer ID",
            right_on="Row",
            how="left",
        )

        # Update the DataFrame with new concentrations or NaN

        def update_concentrations(row):
            # First check if the 'Best Combination' is NaN
            if pd.isna(
                row["p[CTA]"]
            ):  # Cant use best combinations column bc we didnt explicitly add an np.nan
                row["[CTA]"], row["[PC]"] = np.nan, np.nan, np.nan
            else:
                # Split the string and convert to floats only if 'Best Combination' is not NaN
                concentrations = row["Best Combination"].strip("[]").split(",")
                row["[CTA]"] = (
                    float(concentrations[0].strip())
                    if concentrations[0].strip()
                    else np.nan
                )
                row["[PC]"] = (
                    float(concentrations[1].strip())
                    if concentrations[1].strip()
                    else np.nan
                )
            return row

        # Apply the update function to each row
        df = df.apply(update_concentrations, axis=1)

        # Display the updated DataFrame
        df_interest = (
            df[
                [
                    "Polymer ID",
                    "Monomer",
                    "CTA",
                    "photo catalyst",
                    "[M]",
                    "[CTA]",
                    "[PC]",
                    "Mf",
                    "Volume",
                ]
            ]
            .dropna()
            .reset_index(drop=True)
        )
        # 6

        # Now seeing how many unique concentrations there are for each reagent at each concentration
        # and figuring out how much volumen is needed for each,can use first initial fn and store the volume for each reagent on DF

        # First using same initial function to get volumes (didnt change DF name should be fine as wont use the previous one again)
        updated_calculate_results = calculate_polymer_volume_updated(df)
        updated_calculate_results
        polymer_sheet_analysis_df = pd.DataFrame(updated_calculate_results)
        polymers_needing_reag_adjust = polymer_sheet_analysis_df[
            polymer_sheet_analysis_df["Can be made?"] == "Yes"
        ].reset_index(drop=True)
        polymers_needing_reag_adjust = polymers_needing_reag_adjust  # .dropna().reset_index(drop=True) #This here bc if drop NA here messes up the next step

        # 7

        # Here adding the volumes needed for each reagent at the given concentration for each sample in the DF

        from re import I
        # polymers_needing_reag_adjust['Details'][0]['Monomer']

        mon_vol = []
        cta_vol = []
        PC_vol = []
        solvent_vol = []
        for i in range(len(polymers_needing_reag_adjust["Row"])):
            current = i
            # polymers_needing_reag_adjust)
            # polymers_needing_reag_adjust['Details'][current]
            mon_vol.append(polymers_needing_reag_adjust["Details"][current]["Monomer"])
            cta_vol.append(polymers_needing_reag_adjust["Details"][current]["CTA"])
            PC_vol.append(
                polymers_needing_reag_adjust["Details"][current]["photo catalyst"]
            )
            solvent_vol.append(
                polymers_needing_reag_adjust["Details"][current]["Solvent"]
            )

        volumes_df = pd.DataFrame(
            zip(mon_vol, cta_vol, PC_vol, solvent_vol),
            columns=["Monomer Volume", "CTA Volume", "PC Volume", "Solvent Volume"],
        )
        volumes_w_concent_df = (
            pd.concat([df_interest, volumes_df], axis=1)
            .round(
                {
                    "Monomer Volume": 2,
                    "CTA Volume": 2,
                    "PC Volume": 2,
                    "Solvent Volume": 2,
                }
            )
            .dropna()
        )
        volumes_w_concent_df

        # Now getting unique concentrations & storing in a dictionary for some reason some NaNs
        # Show up, I checked but there are non in DF & if check info() on dataframe no values are null
        columns_of_interest = ["[CTA]", "[PC]"]

        # Calculate the number of unique values in each of these columns
        unique_entries = volumes_w_concent_df[columns_of_interest].nunique()

        # Display the number of unique entries for each column
        # print(unique_entries)
        # Get and print unique values for each column of interest
        unique_concent_dict = {}
        for column in columns_of_interest:
            unique_values = df[column].unique()
            unique_concent_dict[column] = unique_values

        volumes_w_concent_df["CTA Cf"] = (
            volumes_w_concent_df["CTA Volume"]
            * volumes_w_concent_df["[CTA]"]
            / volumes_w_concent_df["Volume"]
        )
        volumes_w_concent_df["PC Cf"] = (
            volumes_w_concent_df["PC Volume"]
            * volumes_w_concent_df["[PC]"]
            / volumes_w_concent_df["Volume"]
        )

        # Re-import necessary library

        # Find unique monomers
        unique_monomers = (
            set(monomer_df["Mon 1"].dropna())
            | set(monomer_df["Mon 2"].dropna())
            | set(monomer_df["Mon 3"].dropna())
            | set(monomer_df["Mon 4"].dropna())
        )

        # Initialize an empty DataFrame with Polymer ID and unique monomers as columns
        monomer_percent_df = pd.DataFrame(
            columns=["Polymer ID"] + sorted(unique_monomers)
        )

        # Fill the new DataFrame with Polymer ID and corresponding monomer percentages
        for index, row in monomer_df.iterrows():
            row_data = {"Polymer ID": row["Polymer ID"]}
            for mon_col, perc_col in zip(
                ["Mon 1", "Mon 2", "Mon 3", "Mon 4"],
                ["Mon 1%", "Mon 2%", "Mon 3%", "Mon 4%"],
            ):
                if pd.notna(row[mon_col]):  # Check if monomer exists
                    row_data[row[mon_col]] = (
                        row[perc_col] if pd.notna(row[perc_col]) else 0
                    )

            # Append row to the new DataFrame
            monomer_percent_df = pd.concat(
                [monomer_percent_df, pd.DataFrame([row_data])], ignore_index=True
            )

        # Fill NaN values with 0 for missing monomer percentages
        monomer_percent_df.fillna(0, inplace=True)

        # Display the new DataFrame
        # import ace_tools as tools
        # tools.display_dataframe_to_user(name="Monomer Percentage Data", dataframe=monomer_percent_df)
        # Merge the monomer_percent_df with volumes_w_concent_df to get the monomer volume for each row
        monomer_volume_df = monomer_percent_df.merge(
            volumes_w_concent_df, on="Polymer ID"
        )

        # Multiply the percentages by the corresponding monomer volume to get the final volume for each monomer
        for monomer in monomer_percent_df.columns[1:]:  # Skip Polymer ID column
            monomer_volume_df[f"{monomer} Volume"] = (
                monomer_volume_df[monomer] / 100
            ) * monomer_volume_df["Monomer Volume"]

        # Drop the original percentage columns, keeping only the calculated volumes
        monomer_volume_df = monomer_volume_df.drop(
            columns=monomer_percent_df.columns[1:]
        )

        # Display the final dataframe with monomer volumes
        volumes_w_concent_df = monomer_volume_df

        # 01152025 -- Here adding a summary of reagents that would be needed exactly - should prep extra
        metal_concentrations_needed = volumes_w_concent_df["[CTA]"].unique()
        PC_concentrations_needed = volumes_w_concent_df["[PC]"].unique()

        metal_volumes_needed = []
        ligand_volumes_needed = []
        PC_volumes_needed = []

        for i in range(len(metal_concentrations_needed)):
            metal_volumes_needed.append(
                volumes_w_concent_df.loc[
                    volumes_w_concent_df["[CTA]"] == metal_concentrations_needed[i]
                ]["CTA Volume"].sum()
            )
        for i in range(len(PC_concentrations_needed)):
            PC_volumes_needed.append(
                volumes_w_concent_df.loc[
                    volumes_w_concent_df["[PC]"] == PC_concentrations_needed[i]
                ]["PC Volume"].sum()
            )
        summary_cta = pd.DataFrame(
            zip(metal_concentrations_needed, metal_volumes_needed),
            columns=["[CTA]", "Total CTA Volume"],
        )
        summary_pc = pd.DataFrame(
            zip(PC_concentrations_needed, PC_volumes_needed),
            columns=["[PC]", "Total PC Volume"],
        )

        summary_others = pd.DataFrame(
            zip(
                [volumes_w_concent_df["Monomer Volume"].sum()],
                [volumes_w_concent_df["Solvent Volume"].sum()],
            ),
            columns=["Total Monomer Volume", "Total Solvent Volume"],
        )

        # 8 Debugging Reagent Prep

        # Here now getting rid of those NaNs in the dictionary
        # Then making a new dictionary for each of the reagents of interest (CTA, Ligand & PC) to store volume of each needed

        unique_concent_dict["[CTA]"] = unique_concent_dict["[CTA]"][
            unique_concent_dict["[CTA]"] > 0
        ]
        unique_concent_dict["[PC]"] = unique_concent_dict["[PC]"][
            unique_concent_dict["[PC]"] > 0
        ]

        CTA_dict = {}
        PC_dict = {}

        for i in range(
            len(unique_concent_dict["[CTA]"][unique_concent_dict["[CTA]"] > 0])
        ):
            CTA_dict[unique_concent_dict["[CTA]"][i]] = (
                volumes_w_concent_df[
                    volumes_w_concent_df["[CTA]"]
                    == unique_concent_dict["[CTA]"][unique_concent_dict["[CTA]"] > 0][i]
                ]["CTA Volume"].sum()
                + 200
            )

        for i in range(
            len(unique_concent_dict["[PC]"][unique_concent_dict["[PC]"] > 0])
        ):
            PC_dict[unique_concent_dict["[PC]"][unique_concent_dict["[PC]"] > 0][i]] = (
                volumes_w_concent_df[
                    volumes_w_concent_df["[PC]"]
                    == unique_concent_dict["[PC]"][unique_concent_dict["[PC]"] > 0][i]
                ]["PC Volume"].sum()
                + 200
            )

        # Now will determine how many stocks will be made - Will made a dictionary w Reagents needed
        # For now will assume that the highest concentration reagent will be provided

        max_CTAC = max(list(CTA_dict.keys()))  # The highest concentration in CTA_dict
        max_PCC = max(list(PC_dict.keys()))  # PC

        max_CTAV = CTA_dict[max_CTAC]  # Volume of highest CTA concentration needed
        max_PCV = PC_dict[max_PCC]  # Volume of highest PC concentration needed

        # these will be used to make the reagent preparation dataframe (Concentrations)
        # Lists with the concentrations needed for each reagent
        CTA_concents = list(CTA_dict.keys())
        PC_concents = list(PC_dict.keys())

        # First rounding volumes in the dicts to second decimal - CTA dict has the volumes of each reagent w corresponding concentration needed
        CTA_dict = {key: round(CTA_dict[key], 2) for key in CTA_dict}
        PC_dict = {key: round(PC_dict[key], 2) for key in PC_dict}

        repeats = 1  # int(input('How many times should each polymer be made? '))
        repeats = repeats  # + 0.5
        # These will be used to make reagent preparation DF
        CTA_volumes = list(CTA_dict.values())
        PC_volumes = list(PC_dict.values())

        reagent_preparation_df = pd.DataFrame(
            {
                "[CTA] (mM)": pd.Series(CTA_concents),
                "CTA Volumes (uL)": pd.Series(CTA_volumes),
                "[PC] (mM)": pd.Series(PC_concents),
                "PC Volumes (uL)": pd.Series(PC_volumes),
            }
        )

        reagent_preparation_df["CTA Volumes (uL)"] = (
            reagent_preparation_df["CTA Volumes (uL)"] * repeats
        )
        reagent_preparation_df["PC Volumes (uL)"] = (
            reagent_preparation_df["PC Volumes (uL)"] * repeats
        )

        # Display the final dataframe with monomer volumes
        volumes_w_concent_df = monomer_volume_df

        # 01152025 -- Here adding a summary of reagents that would be needed exactly - should prep extra
        metal_concentrations_needed = volumes_w_concent_df["[CTA]"].unique()
        PC_concentrations_needed = volumes_w_concent_df["[PC]"].unique()

        metal_volumes_needed = []
        ligand_volumes_needed = []
        PC_volumes_needed = []

        for i in range(len(metal_concentrations_needed)):
            metal_volumes_needed.append(
                volumes_w_concent_df.loc[
                    volumes_w_concent_df["[CTA]"] == metal_concentrations_needed[i]
                ]["CTA Volume"].sum()
            )
        for i in range(len(PC_concentrations_needed)):
            PC_volumes_needed.append(
                volumes_w_concent_df.loc[
                    volumes_w_concent_df["[PC]"] == PC_concentrations_needed[i]
                ]["PC Volume"].sum()
            )
        summary_cta = pd.DataFrame(
            zip(metal_concentrations_needed, metal_volumes_needed),
            columns=["[CTA]", "Total CTA Volume"],
        )
        summary_pc = pd.DataFrame(
            zip(PC_concentrations_needed, PC_volumes_needed),
            columns=["[PC]", "Total PC Volume"],
        )

        summary_others = pd.DataFrame(
            zip(
                [volumes_w_concent_df["Monomer Volume"].sum()],
                [volumes_w_concent_df["Solvent Volume"].sum()],
            ),
            columns=["Total Monomer Volume", "Total Solvent Volume"],
        )

        # 8 Debugging Reagent Prep

        # Here now getting rid of those NaNs in the dictionary
        # Then making a new dictionary for each of the reagents of interest (CTA, Ligand & PC) to store volume of each needed

        unique_concent_dict["[CTA]"] = unique_concent_dict["[CTA]"][
            unique_concent_dict["[CTA]"] > 0
        ]
        unique_concent_dict["[PC]"] = unique_concent_dict["[PC]"][
            unique_concent_dict["[PC]"] > 0
        ]

        CTA_dict = {}
        PC_dict = {}

        for i in range(
            len(unique_concent_dict["[CTA]"][unique_concent_dict["[CTA]"] > 0])
        ):
            CTA_dict[unique_concent_dict["[CTA]"][i]] = (
                volumes_w_concent_df[
                    volumes_w_concent_df["[CTA]"]
                    == unique_concent_dict["[CTA]"][unique_concent_dict["[CTA]"] > 0][i]
                ]["CTA Volume"].sum()
                + 200
            )

        for i in range(
            len(unique_concent_dict["[PC]"][unique_concent_dict["[PC]"] > 0])
        ):
            PC_dict[unique_concent_dict["[PC]"][unique_concent_dict["[PC]"] > 0][i]] = (
                volumes_w_concent_df[
                    volumes_w_concent_df["[PC]"]
                    == unique_concent_dict["[PC]"][unique_concent_dict["[PC]"] > 0][i]
                ]["PC Volume"].sum()
                + 200
            )

        # Now will determine how many stocks will be made - Will made a dictionary w Reagents needed
        # For now will assume that the highest concentration reagent will be provided

        max_CTAC = max(list(CTA_dict.keys()))  # The highest concentration in CTA_dict
        max_PCC = max(list(PC_dict.keys()))  # PC

        # these will be used to make the reagent preparation dataframe (Concentrations)
        # Lists with the concentrations needed for each reagent
        CTA_concents = list(CTA_dict.keys())
        PC_concents = list(PC_dict.keys())

        # First rounding volumes in the dicts to second decimal - CTA dict has the volumes of each reagent w corresponding concentration needed
        CTA_dict = {key: round(CTA_dict[key], 2) for key in CTA_dict}
        PC_dict = {key: round(PC_dict[key], 2) for key in PC_dict}

        repeats = 1  # int(input('How many times should each polymer be made? '))
        repeats = repeats  # + 0.5
        # These will be used to make reagent preparation DF
        CTA_volumes = list(CTA_dict.values())
        PC_volumes = list(PC_dict.values())

        reagent_preparation_df = pd.DataFrame(
            {
                "[CTA] (mM)": pd.Series(CTA_concents),
                "CTA Volumes (uL)": pd.Series(CTA_volumes),
                "[PC] (mM)": pd.Series(PC_concents),
                "PC Volumes (uL)": pd.Series(PC_volumes),
            }
        )

        reagent_preparation_df["CTA Volumes (uL)"] = (
            reagent_preparation_df["CTA Volumes (uL)"] * repeats
        )
        reagent_preparation_df["PC Volumes (uL)"] = (
            reagent_preparation_df["PC Volumes (uL)"] * repeats
        )

        # 9 #Debbugin reagent preparation

        # #need second preparation DF for after find out how much of each stock will need to prepare the others
        # #First getting the starting concentration volume required.

        def calculate_volumes(reagent_df, reagent_name):
            # Sort and prepare the dataframe
            prep_df = (
                reagent_df[[f"[{reagent_name}] (mM)", f"{reagent_name} Volumes (uL)"]]
                .sort_values(by=f"[{reagent_name}] (mM)")
                .reset_index(drop=True)
                .dropna()
            )
            # Initialize the list with the volume of the highest concentration
            volumes_to_make = [
                max(prep_df[f"{reagent_name} Volumes (uL)"][0], 100)
            ]  # Ensure the first volume is at least 100 µL
            needed_volume_from_previous_Ar = []
            # Loop through the sorted concentrations from the second item
            for i in range(1, len(prep_df[f"{reagent_name} Volumes (uL)"])):
                current_concentration = prep_df[f"[{reagent_name}] (mM)"][i]
                previous_concentration = prep_df[f"[{reagent_name}] (mM)"][i - 1]
                current_volume = prep_df[f"{reagent_name} Volumes (uL)"][i]
                previous_volume = prep_df[f"{reagent_name} Volumes (uL)"][i - 1]

                # Calculate the ratio of the current concentration to the previous concentration
                concentration_ratio = current_concentration / previous_concentration

                # Determine the volume needed based on the concentration ratio
                if concentration_ratio == 2:  # Standard serial dilution (halving)
                    needed_volume_from_previous = volumes_to_make[-1] / 2

                    needed_volume_from_previous_Ar.append(needed_volume_from_previous)
                    new_vol = current_volume + needed_volume_from_previous
                else:  # Adjusted dilution for skipped concentrations
                    # needed_volume_from_previous = current_volume * concentration_ratio #I think issue here
                    needed_volume_from_previous = (
                        previous_concentration * previous_volume / current_concentration
                    )

                    new_vol = current_volume + needed_volume_from_previous
                    needed_volume_from_previous = (
                        previous_concentration
                        * volumes_to_make[-1]
                        / current_concentration
                    )  # added this after have new volume as for when not serial this gonna be issue
                    needed_volume_from_previous_Ar.append(needed_volume_from_previous)
                    new_vol = current_volume + needed_volume_from_previous
                    # needed_volume_from_previous = previous_concentration*new_vol/current_concentration #added this after have new volume as for when not serial this gonna be issue

                # Check if new volume is less than 100 µL, adjust if necessary
                # new_vol = max(new_vol, 100)  # Ensure that each volume is at least 100 µL

                volumes_to_make.append(new_vol)

            # Update the DataFrame with the calculated volumes
            needed_volume_from_previous_Ar.append(
                0
            )  # This array says how much volume each concent.requires from the one above it.
            # Append 0 at the end bc the highest concentration does not require from another one
            prep_df[f"{reagent_name} Volumes (uL)"] = volumes_to_make
            prep_df[f"{reagent_name} Vol from Next Conc Req (uL)"] = (
                needed_volume_from_previous_Ar
            )
            return prep_df

        # Example usage:
        # Assuming reagent_preparation_df is already defined and loaded with appropriate data
        reagent_names = ["CTA", "PC"]  # List of reagents
        all_reagent_dfs = {}

        for reagent in reagent_names:
            all_reagent_dfs[reagent] = calculate_volumes(
                reagent_preparation_df, reagent
            )

        ##Cleaned up code from above
        # Set initial location for the highest concentration of cta
        highest_cta_loc = 1

        # Generate sequential locations for cta and update DataFrame
        cta_loc = np.arange(
            highest_cta_loc, highest_cta_loc + len(all_reagent_dfs["CTA"])
        )
        # Line below adds the amount of solvent and makes last NaN --Hopefully wont be an issue
        all_reagent_dfs["CTA"]["Solvent"] = round(
            all_reagent_dfs["CTA"]["CTA Volumes (uL)"][:-1]
            - all_reagent_dfs["CTA"]["CTA Vol from Next Conc Req (uL)"][:-1],
            2,
        )
        all_reagent_dfs["CTA"]["SmallTubes1"] = cta_loc[::-1]  # Reversed order

        # Generate sequential locations for PC, starting after the last Ligand location
        highest_pc_loc = cta_loc[-1] + 1
        pc_loc = np.arange(highest_pc_loc, highest_pc_loc + len(all_reagent_dfs["PC"]))
        all_reagent_dfs["PC"]["Solvent"] = round(
            all_reagent_dfs["PC"]["PC Volumes (uL)"][:-1]
            - all_reagent_dfs["PC"]["PC Vol from Next Conc Req (uL)"][:-1],
            2,
        )
        all_reagent_dfs["PC"]["SmallTubes1"] = pc_loc[::-1]  # Reversed order

        print(
            "Only have this many SmallTubes1 available: ",
            32 - all_reagent_dfs["PC"].iloc[0, -1],
        )
        remainig_smt1 = 32 - all_reagent_dfs["PC"].iloc[0, -1]

        # Next is now make the sheet to make the different stocks of each reagent -- Close to the end last part is make the sheet for the final polymer addition
        # Which shouldnt be too bad, cause if after make stocks then can go to the main synthesis sheet and just like did best combination can add an array
        # w the sequence of places to pickup from
        # #When copolymer experiment---- Make function to make steps for adding monomers, first user needs to indicate the locations from each monomer

        # #1st figure out what SmallTubes1 Locations are open by looking at last value in PC SmallTubes1 column

        starting_loc = max(all_reagent_dfs["PC"]["SmallTubes1"]) + 1

        # Same as before but using tupples now to prevent unexpected changes
        def assign_monomer_locations(monomer_volumes_df, starting_loc=4, max_loc=32):
            """
            Interactive function to assign monomer storage locations.

            Parameters:
            monomer_volumes_df (pd.DataFrame): Dataframe containing monomer names and total volume.
            starting_loc (int): The first available location for assignment.
            max_loc (int): The maximum location number available.

            Returns:
            dict: Dictionary mapping monomers to their assigned locations (stored as tuples).
            """
            available_locations = list(range(starting_loc, max_loc + 1))
            monomer_locations = {}

            while True:
                print("\nMonomer Location Assignment Menu:")
                print(
                    "Enter locations separated by commas (e.g., 4,5,6) for each monomer."
                )
                print("Enter '0' to restart.")

                monomer_locations.clear()  # Reset in case of restart

                for monomer in unique_monomers:
                    total_volume = monomer_volumes_df[
                        monomer + " Volume"
                    ].sum()  # Get total volume for this monomer
                    print(
                        f"\nAssign locations for {monomer} (Total Volume: {total_volume} µL)"
                    )

                    while True:
                        print(f"Available locations: {available_locations}")
                        user_input = input(f"Enter locations for {monomer}: ")

                        if user_input.strip() == "0":
                            print("Restarting the assignment process...")
                            return assign_monomer_locations(
                                monomer_volumes_df, starting_loc, max_loc
                            )  # Restart

                        try:
                            assigned_locs = tuple(
                                map(int, user_input.split(","))
                            )  # Convert to **tuple** instead of list

                            if any(
                                loc not in available_locations for loc in assigned_locs
                            ):
                                print(
                                    f"Invalid input. Please choose from available locations: {available_locations}"
                                )
                            else:
                                monomer_locations[monomer] = (
                                    assigned_locs  # ✅ Store as tuple
                                )
                                available_locations = [
                                    loc
                                    for loc in available_locations
                                    if loc not in assigned_locs
                                ]
                                break

                        except ValueError:
                            print(
                                "Invalid input. Please enter numbers separated by commas."
                            )

                print("\nFinal Monomer Locations:")
                for monomer, locations in monomer_locations.items():
                    print(f"{monomer}: {locations}")  # ✅ Will display as tuples

                return monomer_locations  # ✅ Locations are stored as tuples

        # Example of how to call the function
        monomer_locations = assign_monomer_locations(
            monomer_volume_df, starting_loc=starting_loc
        )

        # Used for CR1_30 Robot 2 mult repeats
        # 11  --- but  10 don't need to be run to be able to access this (10 was when making dilutions on the run)

        # For now I will just say where to start for each

        rep1_wells = well_location(len(volumes_w_concent_df["CTA"]), "A1")

        # first making array that have the location of each reagent (PC, Ligand & CTA)
        cta_pickup = []
        pc_pickup = []

        for i in range(len(volumes_w_concent_df["Volume"])):
            # Here getting the concentration needed for each reagent in the current row
            cta_conc = volumes_w_concent_df["[CTA]"][i]
            PC_conc = volumes_w_concent_df["[PC]"][i]

            # Here getting the row index as then will match that to the SmallTubes1 column so know where to pickup from
            cta_ind = all_reagent_dfs["CTA"]["[CTA] (mM)"][
                all_reagent_dfs["CTA"]["[CTA] (mM)"] == cta_conc
            ].index.tolist()[0]
            PC_ind = all_reagent_dfs["PC"]["[PC] (mM)"][
                all_reagent_dfs["PC"]["[PC] (mM)"] == PC_conc
            ].index.tolist()[0]

            # Now getting the SmallTubes1 Location
            cta_loc = all_reagent_dfs["CTA"]["SmallTubes1"][cta_ind]
            PC_loc = all_reagent_dfs["PC"]["SmallTubes1"][PC_ind]

            # Now appending the pickup locations to an list for each reagent
            cta_pickup.append(cta_loc)
            pc_pickup.append(PC_loc)

        solvent_vols = volumes_w_concent_df[
            "Solvent Volume"
        ]  # The volumes in the final DF
        solvent_pickups = adjust_pickup_array(
            [1, 2, 3, 4], len(solvent_vols)
        )  # DMSO in LT 1-8

        # Now making the solvent addition step

        step_creator1(
            solvent_vols,
            solvent_pickups,
            rep1_wells,
            "LargeTubes1",
            "Plate1",
            "DMSO",
            "N",
            0,
            "N",
            temp_folder,
            96,
        )

        # Now adding the Monomer --- Think copolymer method can just be used for all

        make_comonomer_steps(
            volumes_w_concent_df,
            rep1_wells,
            monomer_locations,
            unique_monomers,
            temp_folder,
        )

        # Last steps is now (1) adding first the CTA
        CTA_vols = volumes_w_concent_df["CTA Volume"]
        step_creator1(
            CTA_vols,
            cta_pickup,
            rep1_wells,
            "SmallTubes1",
            "Plate1",
            "DMSO",
            "N",
            0,
            "Y",
            temp_folder,
            96,
        )

        # (2) Adding the ZnTPP
        pc_vols = volumes_w_concent_df["PC Volume"]
        step_creator1(
            pc_vols,
            pc_pickup,
            rep1_wells,
            "SmallTubes1",
            "Plate1",
            "DMSO",
            "N",
            0,
            "Y",
            temp_folder,
            96,
        )

        # Lastly Adding a Mixing Step
        step_creator1(
            np.full_like(solvent_vols.to_numpy(), 80),
            rep1_wells,
            rep1_wells,
            "Plate1",
            "Plate1",
            "DMSO",
            "Y",
            80,
            "Y",
            temp_folder,
            96,
        )

        # -------Adding the excel making part------

        folder_path = temp_folder  #'/content/drive/MyDrive/Experiments/Lipase/CR1_E4/Lip Steps 10182024'
        files = os.listdir(folder_path)
        df = pd.DataFrame({"file name": files})

        step_files = [f for f in files if re.match(r"step_\d+\.xlsx", f)]

        # Make DataFrame and sort
        df = pd.DataFrame({"file name": step_files})
        df_steps = df.iloc[
            [
                i
                for i, _ in sorted(
                    enumerate(df["file name"]),
                    key=lambda x: int(x[1].split("_")[1].split(".")[0]),
                )
            ]
        ].reset_index(drop=True)

        import math

        # Initializing appended_df and the step addition
        appended_df = pd.DataFrame(columns=["Actions", "Parameters"])
        n = 0
        for i in range(len(df_steps["file name"])):
            df1 = pd.read_excel(folder_path + "/" + df_steps["file name"][i])
            # Can get rid of row below once fix this in GUI
            df1 = df1.rename(columns={"column1": "Actions", "column2": "Parameters"})
            if df1["Parameters"][0] == "Transfer" or df1["Parameters"][0] == "Transfer":
                j = math.ceil(df1["Parameters"][2] / 7)
            else:
                j = 1
            strt = 0
            # for next in range(j):
            df1 = pd.read_excel(folder_path + "/" + df_steps["file name"][i])
            # Can get rid of row below once fix this in GUI
            df1 = df1.rename(columns={"column1": "Actions", "column2": "Parameters"})
            data = {"Actions": "Step", "Parameters": n + 1}
            dfm = pd.DataFrame(data, index=[0])
            if df1["Parameters"][0] == "Transfer" or df1["Parameters"][0] == "Transfer":
                df1.drop(columns="Unnamed: 0")
                # Can get rid of row below once fix this in GUI
                df1 = df1.rename(
                    columns={"column1": "Actions", "column2": "Parameters"}
                )
                if df1["Parameters"][8] == 2:
                    df1["Parameters"][8] = "Water"
                # Getting rid of spaces and square brackets at volumes entry
                df1.loc[1, "Parameters"] = (
                    df1["Parameters"][1]
                    .replace(" ", "")
                    .strip("[")
                    .strip("]")
                    .strip("'")
                    .replace("'", "")
                )
                x = df1["Parameters"][1].split(",")
                df1.loc[1, "Parameters"] = ",".join(x[strt : df1["Parameters"][2]])

                # Getting rid of brackets and spaces at pickup positions
                df1.loc[3, "Parameters"] = (
                    df1["Parameters"][3]
                    .replace(" ", "")
                    .strip("[")
                    .strip("]")
                    .strip("'")
                    .replace("'", "")
                )
                x = df1["Parameters"][3].split(",")
                df1.loc[3, "Parameters"] = ",".join(x[strt : df1["Parameters"][2]])
                # Getting rid of brackets and ' ' at dropoff positions
                df1.loc[4, "Parameters"] = (
                    df1["Parameters"][4]
                    .replace(" ", "")
                    .strip("[")
                    .strip("]")
                    .strip("'")
                    .replace("'", "")
                )
                x = df1["Parameters"][4].split(",")
                df1.loc[4, "Parameters"] = ",".join(x[strt : df1["Parameters"][2]])
                df1.loc[2, "Parameters"] = int(len(x[strt : df1["Parameters"][2]]))
                # df1.loc[4,'Parameters'] = df1['Parameters'][4][strt:df1['Parameters'][2]]

                # df1.to_excel("/content/step_try.xlsx")
                # appended_df = pd.DataFrame(columns = ['Actions', 'Parameters'])
                appended_df = pd.concat(
                    [
                        appended_df,
                        dfm,
                        df1.loc[0:11, ["Actions", "Parameters"]],
                        pd.DataFrame([[]]),
                    ],
                    axis=0,
                )
                n = n + 1
            if df1["Parameters"][0] in [
                "Manual Step",
                "Start timer",
                "Pickup",
                "Move",
                "Send message",
            ]:
                appended_df = pd.concat(
                    [
                        appended_df,
                        dfm,
                        df1.loc[0:1, ["Actions", "Parameters"]],
                        pd.DataFrame([[]]),
                    ],
                    axis=0,
                )
                n = n + 1

        appended_df

        # Adding automatic naming

        # Split the path into directory and filename
        dir_path, file_name = os.path.split(file_path_sheet)

        # Modify the filename by adding "Synthesis_" before it
        new_file_name = "Synthesis_" + file_name

        # Reconstruct the full path
        new_final_path = os.path.join(dir_path, new_file_name)

        appended_df.to_excel(new_final_path, index=False)

        # Split the path into directory and filename
        # Here just saving and will put the dataframe in the same folder as the input file

        # Saving done outside now
        dir_path, file_name = os.path.split(file_path_sheet)

        # Modify the filename by adding "Synthesis_" before it
        new_file_name = "Volumes_DF_" + file_name

        # Reconstruct the full path
        new_final_path = os.path.join(dir_path, new_file_name)

        # print(new_final_path)

        volumes_w_concent_df.to_excel(new_final_path)
        new_final_path_prep = os.path.join(dir_path, "Reagent_Prep.xlsx")
        reagent_preparation_df.to_excel(new_final_path_prep)

        # Do all your volume calcs and return a final dataframe

        return volumes_w_concent_df
    finally:
        # Step 2: Clean up temporary folder
        shutil.rmtree(temp_folder)
        print(f"🧹 Temporary folder deleted: {temp_folder}")


def get_unique_monomers(data_file):
    """
    Gets the number of unique monomers when a data file contains a second sheet
    indicating a copolymer experiment.

    input: dataframe
    output: number of unique monomers (list)

    """
    # Extract the second sheet (monomer composition sheet)
    # Identify unique monomers across all columns Mon 1, Mon 2, Mon 3, Mon 4
    monomer_df = data_file[list(data_file.keys())[1]]

    # Identify unique monomers across all columns Mon 1, Mon 2, Mon 3, Mon 4
    monomer_columns = ["Mon 1", "Mon 2", "Mon 3", "Mon 4"]

    # Flatten and get unique values
    unique_monomers = set()
    for col in monomer_columns:
        unique_monomers.update(monomer_df[col].dropna().unique())

    # Output the unique monomers
    unique_monomers
    return unique_monomers


# Run first to initialize functions


def step_creator1(
    vols,
    pickup_pos,
    drop_pos,
    pickup_name,
    drop_name,
    solvent_,
    mix,
    mix_vol,
    replace_tips,
    temp_folder,
    plate_type="",
):
    num_samples = len(np.array(vols))
    if len(pickup_pos) < num_samples:
        for i in range(num_samples - len(pickup_pos)):
            pickup_pos.append(pickup_pos[i])
    step_path = temp_folder + "/step_"
    folder_path = temp_folder
    stp_num = find_next_step_number(folder_path)
    vols, pickup_pos, drop_pos = adjust_volumes_for_pipetting(
        vols, pickup_pos, drop_pos
    )
    indices = np.where(np.array(vols) > 50)[0]
    mask = np.ones_like(np.array(vols), dtype=bool)
    mask[indices] = False

    step_dict_1 = {
        "Action": "Transfer",
        "volume": [float(v) for v in np.array(vols)[mask].tolist()],
        "number samples": int(len(np.array(vols)[mask])),
        # 'pickup positions': str((np.array(pickup_pos)[mask]).tolist()), #Changed this line on 03192025
        # 'pickup positions': ((np.array(pickup_pos)[mask]).tolist()), #Changed this line on 03192025
        "pickup positions": [str(pos) for pos in np.array(pickup_pos)[mask].tolist()],
        "dropoff positions": [str(pos) for pos in np.array(drop_pos)[mask].tolist()],
        "pickup labwareID": pickup_name,
        "dropoff labwareID": drop_name,
        "plate type": plate_type,
        "solvent": solvent_,
        "mixing": mix,
        "mix volume": mix_vol,
        "replace tips": replace_tips,
    }

    df_1 = pd.DataFrame(list(step_dict_1.items()), columns=["Actions", "Parameters"])
    mask[:] = False
    mask[indices] = True
    step_dict_1a = {
        "Action": "Transfer",
        "volume": [float(v) for v in np.array(vols)[mask].tolist()],
        "number samples": int(len(np.array(vols)[mask])),
        "pickup positions": [str(pos) for pos in np.array(pickup_pos)[mask].tolist()],
        "dropoff positions": [str(pos) for pos in np.array(drop_pos)[mask].tolist()],
        "pickup labwareID": pickup_name,
        "dropoff labwareID": drop_name,
        "plate type": plate_type,
        "solvent": solvent_,
        "mixing": mix,
        "mix volume": mix_vol,
        "replace tips": replace_tips,
    }

    df_1a = pd.DataFrame(list(step_dict_1a.items()), columns=["Actions", "Parameters"])
    if (step_dict_1a["number samples"] > 0) and (step_dict_1["number samples"] > 0):
        df_1.to_excel(step_path + str(stp_num) + ".xlsx")
        df_1a.to_excel(step_path + str(int(stp_num) + 1) + ".xlsx")

    if step_dict_1a["number samples"] <= 0 and step_dict_1["number samples"] > 0:
        df_1.to_excel(step_path + str(stp_num) + ".xlsx")
    if step_dict_1a["number samples"] > 0 and step_dict_1["number samples"] <= 0:
        df_1a.to_excel(step_path + str(stp_num) + ".xlsx")


def adjust_volumes_for_pipetting(volumes, pickup_pos, drop_off_pos, max_volume=300):
    # Need to fix this to append the things to the end as of now bc it slows down the robot this way
    """
    Adjusts the volumes array to fit the pipetting limits and updates the corresponding pickup and dropoff arrays.

    Args:
    volumes (list): Array of volumes.
    pickup_pos (list): Corresponding pickup positions.
    drop_off_pos (list): Corresponding drop-off positions.
    max_volume (int): Maximum volume that can be handled per operation.

    Returns:
    tuple: Updated arrays of volumes, pickup positions, and drop-off positions.
    """
    # Initialize the output lists
    adjusted_volumes = []
    adjusted_pickup_pos = []
    adjusted_drop_off_pos = []

    # Iterate over each volume and its corresponding positions
    for volume, pickup, drop_off in zip(volumes, pickup_pos, drop_off_pos):
        while volume > max_volume:
            adjusted_volumes.append(max_volume)
            adjusted_pickup_pos.append(pickup)
            adjusted_drop_off_pos.append(drop_off)
            volume -= max_volume

        # Append the remainder volume if any
        if volume > 0:
            adjusted_volumes.append(volume)
            adjusted_pickup_pos.append(pickup)
            adjusted_drop_off_pos.append(drop_off)

    return adjusted_volumes, adjusted_pickup_pos, adjusted_drop_off_pos


def find_next_step_number(folder_path):
    """
    Determines the next step number for ATRP experiment instruction files stored in a folder.

    Args:
    folder_path (str): Path to the folder containing the instruction Excel files.

    Returns:
    int: The next step number.
    """
    # List all files in the given directory
    files = os.listdir(folder_path)
    # print('files: ', files)

    # Filter and process filenames to extract step numbers
    step_numbers = []
    for file in files:
        if file.startswith("step_") and file.endswith(".xlsx"):
            # Split the filename to extract the step number part
            parts = file.split("_")
            # Attempt to convert the third part (after the second underscore) to an integer
            try:
                step_number = int(
                    parts[1].split(".")[0]
                )  # Split at '.' and convert to int
                step_numbers.append(step_number)
            except ValueError:
                # Handle the case where the conversion fails
                continue

    # Determine the next step number
    if step_numbers:
        return max(step_numbers) + 1
    else:
        # If no valid files found, start at step 1
        return 1


# # Example usage
# folder_path = '/path/to/your/folder'  # Replace with the actual path to your folder
# next_step = find_next_step_number(folder_path)
# print("The next step number should be:", next_step)


def well_location(number_of_wells, starting_well):
    """This function will give the number of wells needed then based on that will assign what wells to use for the polymers by
    creating an array of the length of the dataframe which each index will correspond to the index of the row of the polymer sample
    in the polymers df (volumes_w_concent) -- originally made for Auto ATRP"""

    plate_matrix = [
        ["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1"],
        ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"],
        ["A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3"],
        ["A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4"],
        ["A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5"],
        ["A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6"],
        ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"],
        ["A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8"],
        ["A9", "B9", "C9", "D9", "E9", "F9", "G9", "H9"],
        ["A10", "B10", "C10", "D10", "E10", "F10", "G10", "H10"],
        ["A11", "B11", "C11", "D11", "E11", "F11", "G11", "H11"],
        ["A12", "B12", "C12", "D12", "E12", "F12", "G12", "H12"],
    ]

    plate_wells = list(chain.from_iterable(plate_matrix))
    index_at_start = plate_wells.index(starting_well)
    return plate_wells[index_at_start : index_at_start + int(number_of_wells)]


def adjust_pickup_array(pickup_pos, num_samples):
    """
    Pass the pickup positions for a given reagent then this will iterate over those positions
    to assign a pickup location for each volume. For example if have 96 transfers and will be all DMSO
    which is in LT 1-8, can pass an array [1,2,3,4,5,6,7,8] and the array will be iterated to make one with len 96
    of those positions

    """
    if len(pickup_pos) < num_samples:
        for i in range(num_samples - len(pickup_pos)):
            pickup_pos.append(pickup_pos[i])
    return pickup_pos


def make_comonomer_steps(
    monomer_volume_df, rep1_wells, monomer_locations, unique_monomers, temp_folder
):
    """
    function to make the monomer addition steps for the final sheet.

    """
    monomer_volume_df_well = pd.concat(
        [monomer_volume_df, pd.DataFrame(rep1_wells, columns=["Well"])], axis=1
    )
    for i in range(len(unique_monomers)):
        # mon_vols_array = []
        if i == 0:
            current_monomer = list(unique_monomers)[i]
            mon_well_array = (
                monomer_volume_df_well.loc[
                    monomer_volume_df_well[current_monomer + " Volume"] > 0
                ]["Well"]
                .dropna()
                .to_list()
            )
            mon_vols_array = (
                monomer_volume_df_well.loc[
                    monomer_volume_df_well[current_monomer + " Volume"] > 0
                ][current_monomer + " Volume"]
                .reset_index(drop=True)
                .tolist()
            )
            current_mon_loc = adjust_pickup_array(
                list(monomer_locations[current_monomer]), len(mon_vols_array)
            )  # adjust_pickup_array(np.array(monomer_locations[current_monomer]),len(mon_vols_array))
            monomer_locs_array = current_mon_loc
        if i > 0:
            current_monomer = list(unique_monomers)[i]
            mon_well_array.extend(
                monomer_volume_df_well.loc[
                    monomer_volume_df_well[current_monomer + " Volume"] > 0
                ]["Well"]
                .dropna()
                .to_list()
            )
            # mon_vols_array.append(monomer_volume_df_well.loc[monomer_volume_df_well[current_monomer+' Volume']>0][current_monomer+' Volume'].reset_index(drop=True).tolist())
            mon_vols_array_temp = (
                monomer_volume_df_well.loc[
                    monomer_volume_df_well[current_monomer + " Volume"] > 0
                ][current_monomer + " Volume"]
                .reset_index(drop=True)
                .tolist()
            )
            mon_vols_array.extend(
                monomer_volume_df_well.loc[
                    monomer_volume_df_well[current_monomer + " Volume"] > 0
                ][current_monomer + " Volume"]
                .reset_index(drop=True)
                .tolist()
            )

            current_mon_loc = adjust_pickup_array(
                list(monomer_locations[current_monomer]), len(mon_vols_array_temp)
            )
            monomer_locs_array.extend(current_mon_loc)

    step_creator1(
        mon_vols_array,
        monomer_locs_array,
        mon_well_array,
        "SmallTubes1",
        "Plate1",
        "DMSO",
        "N",
        0,
        "Y",
        temp_folder,
        96,
    )
