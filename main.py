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
    print("Processing file: " + file)
    G, demands = parser.read_sndlib_topology(file)
    highest_cost,  mean_cost,  lowest_cost, lowest_flow = helpers.get_test_values(G)
    max_costs.append(highest_cost)
    min_flows.append(lowest_flow)
    mean_costs.append(mean_cost)
    min_costs.append(lowest_cost)



# Run the algorithms
#Write here how to run the experiments using Analysis.py+
helpers.clear_files()
logging.info("#################################All edges can be killed################################################")
Analysis.run_tests(min_flows, max_costs)
#logging.info("##############################About half the edges can be killed########################################")
#Analysis.run_tests(mean_flows, mean_costs)
#logging.info("#####################################No Edges can be killed#############################################")
#Analysis.run_tests(min_flows,max_costs)