import Analysis
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

# Define parameters

max_costs = []
min_flows = []
mean_flows = []
mean_costs = []
min_costs = []
max_flows = []

for i, file in enumerate(xml_files):
    G, demands = parser.read_sndlib_topology(file)
    highest_cost, highest_flow, mean_cost, mean_flow, lowest_cost, lowest_flow = helpers.get_test_values(G)
    max_costs[i] = highest_cost
    min_flows[i] = lowest_flow
    mean_flows[i] = mean_flow
    mean_costs[i] = mean_cost
    min_costs[i] = lowest_cost
    max_flows[i] = highest_flow




# Run the algorithms
#Write here how to run the experiments using Analysis.py+
Analysis.run_tests(max_costs, min_flows)
Analysis.run_tests(mean_costs, mean_flows)
Analysis.run_tests(min_costs, max_flows)