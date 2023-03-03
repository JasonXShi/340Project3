import json
import copy
from simulator.node import Node


class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.weights = {}
        self.distance_vector = {}  # {dest: (total_weight, [path])}
        self.neighbor_dvs = {}  # {neighbor node: (dv, time)}

    # Return a string
    def __str__(self):
        return json.dumps([self.get_time(), self.id, self.distance_vector])

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        # latency = -1 if delete a link
        if latency == -1:
            self.neighbors.remove(neighbor)
            self.weights.pop(neighbor)
        else:
            self.neighbors.append(neighbor)
            self.weights[neighbor] = latency

        if self.recalculate_dv():
            self.broadcast()

    def update_dv(self, time, neighbor_id, neighbor_dv):
        if neighbor_id not in self.neighbor_dvs or time > self.neighbor_dvs[neighbor_id][1]:
            self.neighbor_dvs[neighbor_id] = (neighbor_dv, time)

    def recalculate_dv(self):
        dist = {}
        path = {}

        dist[self.id] = 0
        path[self.id] = [self.id]

        for neighbor in self.neighbors:
            dist[neighbor] = self.weights[neighbor]
            path[neighbor] = [self.id, neighbor]

        # update our dv with neighbor dvs
        for i in range(len(self.distance_vector.keys())):
            for neighbor in self.neighbors:
                if neighbor not in self.neighbor_dvs:
                    continue
                neighbor_dv = self.neighbor_dvs[neighbor][0]

                for node in neighbor_dv.keys():
                    alt = self.weights[neighbor] + neighbor_dv[node][0]
                    c = copy.deepcopy(neighbor_dv[node][1])
                    if self.id in c:  # skip if it loops
                        continue
                    curr_path = [self.id] + c
                    if node not in dist:
                        dist[node] = alt
                        path[node] = curr_path
                        continue
                    if dist[node] > alt:
                        dist[node] = alt
                        path[node] = curr_path

        # construct new dv from dist and path
        local_dv = {}
        for d in dist.keys():
            local_dv[d] = [dist[d], path[d]]

        for d in local_dv.keys():
            if d not in self.distance_vector or \
              self.distance_vector[d][0] != local_dv[d][0] or \
              self.distance_vector[d][1] != local_dv[d][1]:
                self.distance_vector = local_dv
                return True

        return False

    def broadcast(self):
        self.send_to_neighbors(str(self))

    # Fill in this function
    def process_incoming_routing_message(self, m):
        # update dv in self.neighbor_dvs if it is newer
        time, sender, dv = json.loads(m)
        new_dv = {}
        for key in dv.keys():
            new_dv[int(key)] = dv[key]
        self.update_dv(time, sender, new_dv)

        # update own dv
        if self.recalculate_dv():
            self.broadcast()

        pass

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        return self.distance_vector[destination][1][1]

