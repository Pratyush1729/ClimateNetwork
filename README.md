Constructing the graph Data:
  1. We have a dataset of daily percipitation across 357 locations across India for 110 years (1900-2010).
  2. We create similarity graph from this data by considering an interval of 11-day; A graph is constructed for a given 11 -day    interval where the edges are present if the correlation value between them is greater than 0.95.
  3. The file 'calGraph095.py' creates these threshold values for choosing an edge. 
  4. These threshold values are used in 'createSparse.py' to create sparse matrix out of these values.
Subjecting the graph to cluster analysis:
  1. The file 'connectedNodes.py' gives the set of connected nodes in the graph, which are further subjected highly clustered graph analysis. This analysis calls a connected group of nodes as cluster if the graph connectvity is greater than half the number of nodes. 
The analysis of the nodes obtained was done on the basis of graph Connectivity approach presented by Ron Shamir and Erez Hartuv in this paper[1].
  1. A cluster of nodes is highly connected if graph connectivity if greater than half the number of nodes. 
  2. To test if a cluster is highly connected we find its min-cut using two approaches; Karger's algorithm and Karger-Stein algorithm.
Minimum cut Analysis using Karger's algorithm :
  1. The mincut analysis was done on the simulated graph (with known cut-set) for testing its feasiblity in terms of run time. 
  2. The file 'graphGenrator.py' creates the simulated graph.
  3. The file 'test_karger.py' tests the graph for number of iterations required for solving it. 
Minimum cut Analysis using Karger-Stein's algorithm :
  1. The analysis approach used previously was done again.
  2. The file 'test_karger_stein.py' tests the graph for number of iterations for solving it. 
The final optimized algorthim using Karger-Stein approach and parallelized is in stein_hcs.py. 
