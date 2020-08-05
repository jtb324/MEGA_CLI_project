import logging

from network_creator_class import Network_Img_Maker


def create_networks(segments_file, variant_file, variant_of_interest, output_path):

    logger = logging.getLogger(output_path+'/drawing_networks.log.log')

    network_drawer = Network_Img_Maker(
        segments_file, variant_file, output_path, logger)

    iid_list = network_drawer.isolate_variant_list(variant_of_interest)

    loaded_segments_file = network_drawer.check_file_exist(
        separator=",", header_value=None, skip_rows=5)

    loaded_segments_file = loaded_segments_file.drop(
        [0], axis=1).rename(columns={1: "Pairs"})

    network_drawer_df = network_drawer.isolate_ids(
        loaded_segments_file, iid_list)

    network_drawer.draw_networks(network_drawer_df)
