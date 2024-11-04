https://people.idsia.ch/~luca/ij_23-alife99.pdf
rozdzial 3.2.1

The network is modeled by a graph G = (N,A), where
each node i has the same functionalities as a crossbar switch with limited connectivity
(capacity) and links have infinite capacity (that is, they can carry a potentially infinite
number of connections)

Each link (i, j) connecting node i to node j has an
associated vector of pheromone trail values

τijd, d = 1,...,i−1, i+1,...,n. The value τijd
represents a measure of the desirability of choosing link (i, j) when the destination node
is d.

only
pheromone values are used to define the ant-decision table values

 An exploration mechanism is added to the ant’s decision policy: with
some low probability ants can choose the neighbor to move to following a uniformly random scheme over all the current neighbors

 Ants are launched at regular temporal intervals from all the nodes towards destination nodes selected in a uniform random way. Ants
deposit pheromone only online, step-by-step, on the links they visit

An ant k originated in node s and
arriving at time t in node j from node i adds an amount ∆τ k(t) of pheromone to the value
τjis(t) stored on link (j,i)

After the visited entry has been updated, the pheromone value of all the entries relative
to the destination s decays In this case the decay factor is set to 1/(1 + ∆τ k(t))

The value ∆τ k(t) is a function of the ant age. Ants move over a control network isomorphic
to the real one. They grow older after each node hop and they are virtually delayed in
nodes as a function of the node spare capacity. By this simple mechanism, the amount
of pheromone deposited by an ant is made inversely proportional to the length and to
the degree of congestion of the selected path.

Therefore, the overall effect of ants on
pheromone trail values is such that routes which are visited frequently and by “young”
ants will be favored when building paths to route new calls.