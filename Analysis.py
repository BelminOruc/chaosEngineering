import BacktrackKiller
import BruteKiller
import DynamicKiller
import RandomKiller
import GreedyKiller
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



def run_tests(G, min_flow, max_cost, run):
    '''
    logging.info("--------------------------------------------------------------")
    logging.info("Workingkiller: ")
    edge_numbers = []
    iterations = []
    survivors = []
    for i, graph in enumerate(G):
        logging.info(f'File Nr.'+ str(i))
        #G, demands = parser.read_sndlib_topology(file)
        logging.info("Number of Edges: " + str(G[i].number_of_edges()))
        edge_numbers.append(G[i].number_of_edges())
        iteration, survivor = WorkingKiller.working_killer(G[i], max_cost[i], min_flow[i])
        iterations.append(iteration)
        survivors.append(survivor)

        logging.info("")
        print("Finished")
    logging.info("Iterations: " + str(sum(iterations) / len(iterations)))
    logging.info("Survivers:  " + str(sum(survivors) / len(survivors)) + "%")
    helpers.generate_tikz_graph("Workingkiller, " + run, edge_numbers, iterations, survivors)
    helpers.plot_result_graph("Workingkiller, " + run, edge_numbers, iterations, survivors)
    '''
    logging.info("--------------------------------------------------------------------------------------")
    logging.info("DynamicKiller: ")
    edge_numbers = []
    iterations = []
    survivors = []
    for i, graph in enumerate(G):
        logging.info(f'Processing file: {i}')
        logging.info("Number of Edges: " + str(G[i].number_of_edges()))
        edge_numbers.append(G[i].number_of_edges())
        iteration, survivor = DynamicKiller.dynamic_killer(G[i], max_cost[i], min_flow[i])
        iterations.append(iteration)
        survivors.append(survivor)
        logging.info("")
        print("Finished")
    logging.info("Iterations: "+ str(sum(iterations) / len(iterations)))
    logging.info("Survivers:  "+str(sum(survivors) / len(survivors))+"%")
    helpers.generate_tikz_graph("DynamicKiller, "+ run, edge_numbers, iterations, survivors)
    helpers.plot_result_graph("DynamicKiller, "+ run, edge_numbers, iterations, survivors)
    '''
    logging.info("--------------------------------------------------------------------------------------")
    logging.info("Greedykiller: ")
    edge_numbers = []
    iterations = []
    survivors = []
    for i, graph in enumerate(G):
        logging.info(f'Processing file: '+ str(i))
        logging.info("Number of Edges: " + str(G[i].number_of_edges()))
        edge_numbers.append(G[i].number_of_edges())
        iteration, survivor = GreedyKiller.compute_link_failures(G[i])
        iterations.append(iteration)
        survivors.append(survivor)
        logging.info("")
        print("Finished")
    logging.info(sum(survivors)/len(survivors))
    logging.info(sum(iterations) / len(iterations))
    helpers.generate_tikz_graph("Greedykiller, "+ run, edge_numbers, iterations, survivors)
    helpers.plot_result_graph("Greedykiller, "+ run, edge_numbers, iterations, survivors)
    logging.info("--------------------------------------------------------------------------------------")

    logging.info("Random: ")
    edge_numbers = []
    iterations = []
    survivors = []
    for i, graph in enumerate(G):
        logging.info(f'Processing file: {i}')
        logging.info("Number of Edges: " + str(G[i].number_of_edges()))
        edge_numbers.append(G[i].number_of_edges())
        iteration, survivor = RandomKiller.random_killer(G[i], max_cost[i], min_flow[i])
        iterations.append(iteration)
        survivors.append(survivor)
        logging.info("")
        print("Finished")
    helpers.generate_tikz_graph("Random, "+ run, edge_numbers, iterations, survivors)
    helpers.plot_result_graph("Random, "+ run, edge_numbers, iterations, survivors)
    logging.info("--------------------------------------------------------------------------------------")

    logging.info("BruteKiller: ")
    edge_numbers = []
    iterations = []
    survivors = []
    for i, graph in enumerate(G):
        logging.info(f'Processing file: {i}')
        logging.info("Number of Edges: " + str(G[i].number_of_edges()))
        edge_numbers.append(G[i].number_of_edges())
        iteration, survivor = BruteKiller.brute_killer(G[i], max_cost[i], min_flow[i])
        iterations.append(iteration)
        survivors.append(survivor)
        logging.info("")
        print("Finished")
    helpers.generate_tikz_graph("BruteKiller, "+ run, edge_numbers, iterations, survivors)
    helpers.plot_result_graph("BruteKiller, "+ run, edge_numbers, iterations, survivors)
    logging.info("--------------------------------------------------------------------------------------")
    logging.info("--------------------------------------------------------------------------------------")
    logging.info("BacktrackKiller: ")
    edge_numbers = []
    iterations = []
    survivors = []
    for i, file in enumerate(xml_files):
        logging.info(f'Processing file: {i}')
        logging.info("Number of Edges: " + str(G[i].number_of_edges()))
        edge_numbers.append(G[i].number_of_edges())
        iteration, survivor = BacktrackKiller.backtrack_killer(G[i], max_cost[i], min_flow[i])

        iterations.append(iteration)
        survivors.append(survivor)
        logging.info("")
        print("Finished")
    logging.info("Iterations: " + str(sum(iterations) / len(iterations)))
    logging.info("Survivers:  " + str(sum(survivors) / len(survivors)) + "%")
    helpers.generate_tikz_graph("BacktrackKiller"+ run, edge_numbers, iterations, survivors)
    helpers.plot_result_graph("BacktrackKiller"+ run, edge_numbers, iterations, survivors)
    '''