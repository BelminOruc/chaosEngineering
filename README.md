# chaosEngineering
Bachelor-Thesis Code

## Installation

To run this project, you need to have Python installed. You can install the required dependencies using `pip`. 

```bash
pip install networkx matplotlib
```
## Running the code


```bash
python main.py
```

## Parameters
- 'max_cost' : The maximum flow cost of a graph
- 'min_flow' : The minimum flow of a graph 
- 'biconnected' : If the graph should be biconnected or not

## Varying the parameters
You can vary the parameters:

- max cost and max flow arrays can be specified in the main.py file. 

- alternatively you can change the way it generates the max_cost and max_flow arrays in the helpers.py function
"get_test_values"
- biconnectivity uncommenting the if statement for that in the helpers.py function "check_requirements"


### Info:
Right now only following algorithms are run automatically when running the main.

These include: Working Killer, Iterative killer and the Backtrack Killer.

To change that go to analysis.py and uncomment the algorithms you want to run.

The commented-out algorithms are those that that encounter difficulties when processing specific data sets and therefore cannot be expected to function optimally. 
## Returns
log file "analysis.log" with the results of the experiments

text file "graph.txt" with the graphs that were generated in tikz code.