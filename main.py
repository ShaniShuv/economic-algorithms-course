# This is a sample Python script.
import math
import copy
import networkx
import networkx as nx

def q4a(g):
    new_graph = copy.deepcopy(g)
    cycle = negative_cycle(new_graph)
    # TODO:
    # add a new graph so I could send only it's copy
    if cycle!=[]: return True
    else: return False

def negative_cycle(graph):
    new_graph = copy.deepcopy(graph)
    update_weights(new_graph)
    cycleFound=False
    cycle = []
    # print(graph.edges.data())
    for node in graph.nodes:
        if cycleFound:
            break
        try:
            cycle = nx.find_negative_cycle(graph, node)
            cycleFound = True

        except:
            pass

    print("Does G contains any negative cycle?", cycleFound)
    if cycleFound:
        print(cycle)
    return cycle


def update_weights(graph):
    for e in graph.edges:
        weight = graph[e[0]][e[1]]["weight"]
        if weight > 0:
            graph[e[0]][e[1]]["weight"] = math.log(weight, 2)
    return graph



def q5(cycle=[], allocation=[0][0], valuations=[0][0]):
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
    gv=networkx.DiGraph
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
    graph_consumes=networkx.DiGraph
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
    q=5

    if q=="4a":
        q4a(g)

    elif q==5:
        q5(g)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
