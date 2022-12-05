# This is a sample Python script.
import math
import copy
import networkx as nx

def q4a(g):
    """
    this function checks if there's a cycle that can present an exchange in the allocation which lead to a parreto improvment
    :param g: a graph
    :return: True iff there is a  parreto improvment
    """
    new_graph = copy.deepcopy(g)
    cycle = negative_cycle(new_graph)
    if cycle!=[]:
        return True
    else:
        return False

def negative_cycle(graph):
    new_graph = copy.deepcopy(graph)
    update_weights_as_log(new_graph)
    cycleFound=False
    cycle = []

    for node in new_graph.nodes:
        if cycleFound:
            break
        try:
            # if it doesn't find a negative cycle it throws an exception
            cycle = nx.find_negative_cycle(new_graph, node)
            cycleFound = True
        except:
            pass

    return cycle


def update_weights_as_log(graph):
    """
    I failed to use the doctest
    :returns the graph with edges as their logarithmic value
    >>> graph_with_negative_cycle = nx.DiGraph().add_node(range(3)).add_edge(1, 2, weight=4).add_edge(2, 3, weight=0.5).add_edge(3, 1, weight=0.25)
    this graph_with_negative_cycle is the triangle 1 --4--> 2 --0.5--> 3 --0.25--> 1
    >>> graph_with_negative_cycle_updated = nx.DiGraph().add_node(range(3)).add_edge(1, 2, weight=2).add_edge(2, 3, weight=-1).add_edge(3, 1, weight=-1)
    >>>[update_weights_as_log(graph=graph_with_negative_cycle)]
    >>> graph_with_negative_cycle_updated
    :param graph:
    :return:
    """
    for e in graph.edges:
        weight = graph[ e[0] ][ e[1] ]["weight"]
        # print("weight before", weight)
        if weight > 0:
            graph[e[0]][e[1]]["weight"] = math.log(weight, 2)
            # print("weight after",graph.get_edge_data(e[0] ,e[1]))

    return graph



def overall(cycle=[], allocation=[0][0], valuations=[0][0]):
    graph_consumes = create_graph_consumes(allocation)
    graph_exchanges = create_graph_exchanges(allocation, valuations)

    negative_consume_cycle=cycle
    if negative_consume_cycle == []:
        negative_consume_cycle=negative_cycle(graph_consumes)
        if negative_consume_cycle == []:
            return allocation

    negative_exchange_cycle = negative_cycle(graph_exchanges)

    if negative_exchange_cycle == []:
        negative_exchange_cycle = find_zero_weighted_cycle()
    return update_allocation(allocation, negative_consume_cycle)


def find_zero_weighted_cycle():
    #TODO: only if I find a time for it
    pass

def update_allocation(exchange_cycle, allocation, valuations):
    new_allocation = allocation

    exchange_table = [len(allocation)][2]
    # if_a_player = True
    counter=0
    for node in exchange_cycle:
        if node > 0:
            exchange_table[counter][0] = node

        else:
            exchange_table[counter][1] = node
            counter += 1

    epsilon = allocation[[exchange_table][1], [exchange_table][1][0]]
    fraction = 1
    for i in range(len(exchange_table)-1):
        curr_epsilon = fraction * allocation[[exchange_table][i][0], [exchange_table][i][1]]
        fraction *= valuations[[exchange_table][i][0], [exchange_table][i][1]]/valuations[[exchange_table][i+1][0], [exchange_table][i][1]]
        if curr_epsilon >=0:
            epsilon = min(epsilon, curr_epsilon)
            #TODO: prve that it cannot be neg or even 0

    # fraction_in_process = 1
    for i in range(len(exchange_table)-1):
        if i == 0:
            curr_player = [exchange_table][i][0]
            curr_object = [exchange_table][i][1]
            next_player = [exchange_table][i+1][0]
            # next_object = [exchange_table][i+1][1]

            allocation[curr_player, curr_object] -= epsilon
            allocation[next_player, curr_object] += epsilon

        return allocation



def create_graph_exchanges(allocation=[0][0], valuations=[0][0]):
    gv=nx.DiGraph()
    gv.add_nodes_from(range(10))
    res=[[[0 for i in range (len(allocation))] for i in range (len(valuations))]  for i in range (len(valuations))]

    for i in len(allocation):
        for j in len(allocation):
            if i!=j:
                res[i][j]= [a / b for a, b in zip(valuations[i], valuations[j])]
            for k in range(len(res)):
                    if allocation[i][k] == 0:
                        allocation[i][k] = 100 # math.inf
            gv.add_edge(i, j, weight=min(res[i][j]))

def create_graph_consumes(allocation=[0][0]):
    graph_consumes=nx.DiGraph
    graph_consumes.add_nodes_from(range(len(allocation)))
    graph_consumes.add_nodes_from(range(-len(allocation[1]), 0))

    for i in len(allocation):
        for k in len(allocation[1]):
            if allocation[i][k] != 0:
                graph_consumes.add_edge(i, -k, weight=-1)
    return graph_consumes




if __name__ == '__main__':
    g = nx.DiGraph()
    g.add_nodes_from(range(10))
    g.add_edge(1, 2, weight=0.5)
    g.add_edge(2, 3, weight=0.5)
    g.add_edge(3, 1, weight=0.5)

    q="4a"
    # q=5

    # if q=="4a":
    #     q4a(g)

    graph_with_negative_cycle = nx.DiGraph()
    graph_with_negative_cycle.add_node(range(3))
    graph_with_negative_cycle.add_edge(1, 2, weight=4)
    graph_with_negative_cycle.add_edge(2, 3,weight=0.5)
    graph_with_negative_cycle.add_edge(3, 1, weight=0.25)
    # graph_with_negative_cycle is the triangle  1 --4--> 2 --0.5--> 3 --0.25--> 1

    graph_with_negative_cycle_updated = nx.DiGraph()
    graph_with_negative_cycle_updated.add_node(range(3))
    graph_with_negative_cycle_updated.add_edge(1, 2, weight=2.0)
    graph_with_negative_cycle_updated.add_edge(2, 3,weight=-1.0)
    graph_with_negative_cycle_updated.add_edge( 3, 1, weight=-1.0)
    # graph_with_negative_cycle_updated is the following triangle  1 --2--> 2 --(-1)--> 3 --(-2)--> 1

    cycle = negative_cycle(graph_with_negative_cycle)
    print(cycle)

    graph_without_negative_cycle = nx.DiGraph()
    graph_without_negative_cycle.add_node(range(3))
    graph_without_negative_cycle.add_edge(1, 2, weight=4)
    graph_without_negative_cycle.add_edge(2, 3, weight=8)
    graph_without_negative_cycle.add_edge(3, 1, weight=16)

    graph_with_negative_cycle_updated = nx.DiGraph()
    graph_with_negative_cycle_updated.add_node(range(3))
    graph_with_negative_cycle_updated.add_edge(1, 2, weight=2.0)
    graph_with_negative_cycle_updated.add_edge(2, 3, weight=3.0)
    graph_with_negative_cycle_updated.add_edge(3, 1, weight=4.0)

    cycle = negative_cycle(graph_with_negative_cycle_updated)
    print(cycle)

    # flag = update_weights_as_log(graph=graph_with_negative_cycle) == graph_with_negative_cycle_updated
    # print(flag)
    # elif q==5:
    #     overall(g)

    # import doctest
    # doctest.testmod()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
