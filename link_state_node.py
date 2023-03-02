from simulator.node import Node
import json

class Link_State_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.graph = Weighted_Graph()

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        if latency == -1 and neighbor in self.neighbors:
            self.neighbors.remove(neighbor)
        else:
            self.neighbors.append(neighbor)

        # new node
        if neighbor not in self.graph.nodes:
            for source in self.graph.nodes:
                for dest, old_latency, seq in self.graph.adj_list[source]:
                    
                    message = json.dumps([source, dest, old_latency, seq])
                    self.send_to_neighbor(neighbor, "0" + message)

        # old node
        new_seq = self.graph.update_edge(self.id, neighbor, latency)
        message = json.dumps([self.id, neighbor, latency, new_seq])
        self.send_to_neighbors("1" + message)

        return

    # Fill in this function
    def process_incoming_routing_message(self, m):
        if m[0] == "0":
            source, dest, latency, seq = json.loads(m[1:])
            self.graph.incoming_edge(source, dest, latency, seq)
            return

        elif m[0] == "1":
            source, dest, latency, seq = json.loads(m[1:])
            updated = self.graph.incoming_edge(source, dest, latency, seq)
            if updated:
                self.send_to_neighbors(m)
    
    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        dist = {}
        prev = {}

        for v in self.graph.nodes:
            dist[v] = float("inf")
            prev[v] = None
        dist[self.id] = 0
        Q = list(self.graph.nodes.copy())

        while len(Q) > 0:
            Q.sort(key=lambda x: dist[x])
            u = Q[0]
            Q.remove(u)
            for v in self.graph.nodes:
                weight = self.graph.get_edge_weight(u,v)
                if weight < 0:
                    continue
                alt = dist[u] + self.graph.get_edge_weight(u,v)
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

        if dist.get(destination, float("inf")) == float("inf"):
            return -1
        next_hop = destination
        while prev[next_hop] != self.id:
            next_hop = prev[next_hop]
        return next_hop

class Weighted_Graph():
    def __init__(self):
        self.nodes = set()
        self.adj_list = {}

    def update_edge(self, source, dest, latency):
        self.nodes.add(source)
        # self.nodes.add(dest)
            
        if self.adj_list.get(source) == None:
            self.adj_list[source] = [[dest,latency,0]]
        else:
            for edge in self.adj_list[source]:
                if edge[0] == dest:
                    edge[1] = latency
                    edge[2] += 1   
                    return edge[2]
            self.adj_list[source].append([dest,latency,0])     
        return 0
    
    def incoming_edge(self, source, dest, latency, sequence):
        self.nodes.add(source)
        # self.nodes.add(dest)
        
        if self.adj_list.get(source) == None:
            self.adj_list[source] = [[dest,latency,0]]
        else:
            for edge in self.adj_list[source]:
                if edge[0] == dest:
                    if sequence > edge[2]:
                        edge[1] = latency
                        edge[2] = sequence
                        return True
                    return False
            self.adj_list[source].append([dest,latency,0])
        
        return True
    
    def get_edge_weight(self, source, dest):
        if source not in self.nodes:
            return -1
        for edge in self.adj_list[source]:
            if edge[0] == dest:
                return edge[1]
        return -1
