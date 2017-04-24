Constructing the graph Data:
  We have a dataset of daily percipitation across 357 locations across India for 110 years (1900-2010).
  We create similarity graph from this data by considering an interval of 11-day; A graph is constructed for a given 11 -day    interval where the edges are present if the correlation value between them is greater than 0.95.
  The file 'calGraph095.py' creates these threshold values for choosing an edge. 
  These threshold values are used in 'createSparse.py' to create sparse matrix out of these values.
