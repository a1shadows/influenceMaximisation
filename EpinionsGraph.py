import networkx as nx
import matplotlib.pyplot as plt

def makeEpinionsGraph():
    eData = nx.Graph()
    f = open("soc-Epinions1.txt", 'r')
    for i in f.readlines():
        if i[0] != "#":
            x, y = i.split()
            eData.add_node(x) if x not in eData.nodes() else 0
            eData.add_node(y) if y not in eData.nodes() else 0
            eData.add_edge(x, y)
    f.close()
    return eData

if __name__ == "__main__":
    G = nx.davis_southern_women_graph()
    nx.draw(G)
    plt.show()