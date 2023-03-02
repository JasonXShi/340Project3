class Weighted_Graph():
    def __init__(self):
        self.nodes = set()
        self.adj_list = {}

    def update_edge(self, source, dest, latency):
        self.nodes.add(source)
        self.nodes.add(dest)
        for edge in self.adj_list.get(source, []):
            if edge[0] == dest:
                edge[1] = latency
                edge[2] += 1
                return edge[2]
            
        if self.adj_list.get(source) == None:
            self.adj_list[source] = [[dest,latency,0]]
        else:
            self.adj_list[source].append([dest,latency,0])
        return 0
    
    def add_edge(self, source, dest, latency, sequence):
        self.nodes.add(source)
        self.nodes.add(dest)
        for edge in self.adj_list.get(source, []):
            if edge[0] == dest:
                if sequence > edge[2]:
                    edge[1] = latency
                    edge[2] = sequence
                    return True
                return False
        if self.adj_list.get(source) == None:
            self.adj_list[source] = [[dest,latency,0]]
        else:
            self.adj_list[source].append([dest,latency,0])
        
        return True
    
    def get_edge_weight(self, source, dest):
        if source not in self.nodes:
            return -1
        for edge in self.get_adjacent(source):
            if edge[0] == dest:
                return edge[1]
        return -1

    def get_edge_sequence(self, source, dest):
        if source not in self.nodes:
            return -1
        for edge in self.get_adjacent(source):
            if edge[0] == dest:
                return edge[2]
        return -1

    def get_adjacent(self, source):
        adj = []
        for edge in self.get_adjacent(source):
            if edge[1] >= 0:
                adj.append(edge[0])
        return []


g = Weighted_Graph()
g.add_edge(1,2,3, 0)
g.add_edge(1,3,4, 0)
g.add_edge(1,4,5,0)
g.add_edge(2,3,5,0)
g.add_edge(3,4,6,0)
print(g.adj_list)
