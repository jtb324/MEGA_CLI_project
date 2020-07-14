# Determining the allele count in families
import pandas as pd
import numpy as np

################################################
from check_directory import check_dir
from write_path import writePath

################################################


def allele_counts(input_path, output_path):
    '''This function determines the allele counts for specific variants in each family'''

    #Reading in the files ##########################
    raw_file = pd.read_csv(input_path[0], sep=" ")

    pedigree_df = pd.read_csv(input_path[1], sep=",")

    ################################################
    # Getting the names of all the columns to iterate through
    column_list = list(raw_file.columns[6:].values)

    # Creating a dictionary to keep the networks FID, the variant and te number of alleles in each network
    allele_count_dict = dict()

    ###################################################
    # Iterating through all the rows of the pedigree data
    for tuple in pedigree_df.itertuples(index=False):

        # This get the lists of all IID's from the pedigree file
        iid_list = tuple[1].strip("[]").replace(
            "'", "").replace(" ", "").split(",")

        # This gets the variant from the dataframe row
        variant = tuple[0].strip("[]").replace("(", "").replace(
            "'", "").replace(" ", "").split(",")[0]

        # This gets the network FID from the pedigree row
        network = tuple[0].strip("[]").replace(")", "").replace(
            "'", "").replace(" ", "").split(",")[1]

        # This subsets the full raw file for only those value also in the row from the pedigree
        raw_file_subset = raw_file[raw_file["IID"].isin(iid_list)]

        # This iterates through the columns of the dataframe row
        for column in column_list:

            # This starts a counter to determine the number of alleles for each variant
            allele_count = 0

            # This finds the index of any spot with a 1 in the recoding
            index_list_1 = raw_file_subset.index[raw_file_subset[column].isin([
                1])].tolist()

            # This finds the index of any spot with a 2 in the recoding
            index_list_2 = raw_file_subset.index[raw_file_subset[column].isin([
                2])].tolist()

            # This determines the allele count for the variant
            allele_count = len(index_list_1) + len(index_list_2)*2

            # This forms the total index list of each individual with the variant
            index_list = index_list_1 + index_list_2

            # Checks if the index_list is not empty
            if index_list:

                if "IID" and "Network" and "Variant ID" in allele_count_dict:

                    allele_count_dict["Network"].append(network)

                    allele_count_dict["Variant ID"].append(variant)

                    allele_count_dict["Allele Count"].append(allele_count)

                else:

                    allele_count_dict["Network"] = [network]

                    allele_count_dict["Variant ID"] = [variant]

                    allele_count_dict["Allele Count"] = [allele_count]

    allele_count_df = pd.DataFrame(
        allele_count_dict, columns=["Network", "Variant ID", "Allele Count"])

    allele_count_df.drop_duplicates(
        keep="last", inplace=True)

    reformat_directory = check_dir(output_path, "reformated")

    allele_count_df.to_csv(
        writePath(reformat_directory, "allele_count.csv"), index=False)

    # Grouping the resulting output by Allele_count

    count_groups_df = allele_count_df.groupby("Allele Count").count()

    count_groups_df.to_csv(
        writePath(reformat_directory, "grouped_allele_counts.csv"), index=False)