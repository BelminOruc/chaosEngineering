import networkx as nx
from matplotlib import pyplot as plt
import BacktrackKiller
import BruteKiller
import DynamicKiller
import FlowKiller
import RandomKiller
import WorkingKiller
import helpers
import parser
import os
import glob
import logging

# Configure logging
logging.basicConfig(filename='analysis.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Specify the directory containing the XML files
#directory = 'toobigtohandle'
directory = 'sndlibcontent'

# Use glob to find all XML files in the directory
xml_files = glob.glob(os.path.join(directory, '*.xml'))



def run_tests(min_flow, max_cost):
    logging.info("--------------------------------------------------------------")
    edge_numbers = []
    iterations = []
    for i, file in enumerate(xml_files):
        logging.info(f'Processing file: {file}')
        G, demands = parser.read_sndlib_topology(file)
        logging.info("Number of Edges: " + str(G.number_of_edges()))
        edge_numbers.append(G.number_of_edges())
        iterations.append(WorkingKiller.working_killer(G, demands, max_cost[i], min_flow[i]))
        print("Finished")
    helpers.generate_tikz_graph(iterations, edge_numbers)
    helpers.plot_result_graph(iterations, edge_numbers)
    logging.info("--------------------------------------------------------------------------------------")
    edge_numbers = []
    iterations = []
    for i, file in enumerate(xml_files):
        logging.info(f'Processing file: {file}')
        G, demands = parser.read_sndlib_topology(file)
        logging.info("Number of Edges: " + str(G.number_of_edges()))
        edge_numbers.append(G.number_of_edges())
        iterations.append(BacktrackKiller.backtrack_killer(G, demands, max_cost[i], min_flow[i]))
        print("Finished")
    helpers.generate_tikz_graph(iterations, edge_numbers)
    helpers.plot_result_graph(iterations, edge_numbers)
    logging.info("--------------------------------------------------------------------------------------")
    edge_numbers = []
    iterations = []
    for i, file in enumerate(xml_files):
        logging.info(f'Processing file: {file}')
        G, demands = parser.read_sndlib_topology(file)
        logging.info("Number of Edges: " + str(G.number_of_edges()))
        edge_numbers.append(G.number_of_edges())
        iterations.append(DynamicKiller.dynamic_killer(G, demands, max_cost[i], min_flow[i]))
        print("Finished")
    latex_code = helpers.generate_tikz_graph(iterations, edge_numbers)
    helpers.plot_result_graph(iterations, edge_numbers)
    logging.info("--------------------------------------------------------------------------------------")
    edge_numbers = []
    iterations = []
    for i, file in enumerate(xml_files):
        logging.info(f'Processing file: {file}')
        G, demands = parser.read_sndlib_topology(file)
        logging.info("Number of Edges: " + str(G.number_of_edges()))
        edge_numbers.append(G.number_of_edges())
        iterations.append(FlowKiller.greedy_flow_killer(G, demands, max_cost[i], min_flow[i]))
        print("Finished")
    helpers.generate_tikz_graph(iterations, edge_numbers)
    helpers.plot_result_graph(iterations, edge_numbers)
    logging.info("--------------------------------------------------------------------------------------")
    edge_numbers = []
    iterations = []
    for i, file in enumerate(xml_files):
        logging.info(f'Processing file: {file}')
        G, demands = parser.read_sndlib_topology(file)
        logging.info("Number of Edges: " + str(G.number_of_edges()))
        edge_numbers.append(G.number_of_edges())
        iterations.append(RandomKiller.random_killer(G, demands, max_cost[i], min_flow[i]))
        print("Finished")
    helpers.generate_tikz_graph(iterations, edge_numbers)
    helpers.plot_result_graph(iterations, edge_numbers)
    logging.info("--------------------------------------------------------------------------------------")
    edge_numbers = []
    iterations = []
    for i, file in enumerate(xml_files):
        logging.info(f'Processing file: {file}')
        G, demands = parser.read_sndlib_topology(file)
        logging.info("Number of Edges: " + str(G.number_of_edges()))
        edge_numbers.append(G.number_of_edges())
        iterations.append(BruteKiller.brute_killer(G, demands, max_cost[i], min_flow[i]))
        print("Finished")
    helpers.generate_tikz_graph(iterations, edge_numbers)
    helpers.plot_result_graph(iterations, edge_numbers)
    logging.info("--------------------------------------------------------------------------------------")