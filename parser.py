from itertools import islice
import math
from xml.dom.minidom import parse
import xml.dom.minidom
import networkx as nx
import numpy as np
import logging

#Das Paper "Transparent vs. opaque vs. translucent wavelength-routed optical networks" in der Bachelorarbeit zitieren


def read_sndlib_topology(file):
    graph = nx.Graph()
    demands = {}

    with open(file) as file:
        tree = xml.dom.minidom.parse(file)
        document = tree.documentElement

        graph.graph["coordinatesType"] = document.getElementsByTagName("nodes")[0].getAttribute("coordinatesType")

        nodes = document.getElementsByTagName("node")
        for node in nodes:
            x = node.getElementsByTagName("x")[0]
            y = node.getElementsByTagName("y")[0]
            node_id = node.getAttribute("id")
            graph.add_node(node_id, pos=(float(x.childNodes[0].data), float(y.childNodes[0].data)))

        links = document.getElementsByTagName("link")
        for idx, link in enumerate(links):
            additional_modules = link.getElementsByTagName('addModule')
            try:
                last_module = additional_modules[-1]
            except IndexError:
                preInstalledModules = link.getElementsByTagName('preInstalledModule')
                last_module = preInstalledModules[-1]
            capacity = float(last_module.getElementsByTagName('capacity')[0].firstChild.data)
            cost = float(last_module.getElementsByTagName('cost')[0].firstChild.data)
            source = link.getElementsByTagName("source")[0].childNodes[0].data
            target = link.getElementsByTagName("target")[0].childNodes[0].data

            graph.add_edge(source, target, id=link.getAttribute("id"), capacity=capacity, cost=cost, index=idx)

        demand_elements = document.getElementsByTagName("demand")
        for demand in demand_elements:
            source = demand.getElementsByTagName("source")[0].childNodes[0].data
            demand_value = float(demand.getElementsByTagName("demandValue")[0].childNodes[0].data)
            if source not in demands:
                demands[source] = 0  # Ensure the source node is initialized in demands
            demands[source] += demand_value  # Aggregate demand values for each source node
    graph.graph["node_indices"] = [node for node in graph.nodes()]

    return graph, demands