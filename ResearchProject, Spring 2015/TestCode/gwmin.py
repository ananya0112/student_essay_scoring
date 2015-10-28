"""
Example/Dummy input:
Graph = {
'A' : [1, 5],
'B' : [2, 4],
'C' : [2, 3],
'D' : [3],
'E' : [1, 4, 5]
}
"""
import sys

# scu_dict = {1:5, 2:5, 3:4, 4:4, 5:3} # Dummy scu_dict #
from data_analytics import getSCU
scu_dict = getSCU("12_10_09_MATTER.pyr", "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/scu_YINGHUI/scu")

# Adding max. values to scu-dictionary for sentence id's
for i in xrange(-18, 0):
	scu_dict[i] = 5



""" Algo_type = 1 : greedy algo 1 using den = degree + 1 | Algo_type = 2 : greedy algo 2 using den = weight(neighborhood) 
Default is algo_type = 2"""
algo_type = 0 # 1 / 2

class Vertex(object):
	def __init__(self, name, elements):
		self.name = name
		self.scu_ids = elements
		self.weight = self.__get_weight() # -- #


	def __get_weight(self):
		""" Given the list of unique scu_id's of the form '134: 1', return the sum of their scores """
		sum_scu = 0
		for scu_id in self.scu_ids:
			sum_scu += scu_dict[scu_id]
		return sum_scu


	def get_info(self):
		print "Name : "+str(self.name)
		print "Elements : "
		for scu_id in self.scu_ids:
			print scu_id
		print "Total Weight : "+str(self.weight)
		print '\n'



class Edge(object):
	def __init__(self,v1, v2):
		""" Edge e between vertices v1 -- e -- v2 | value = intersection of scu_id's between the sets """
		self.v1 = v1
		self.v2 = v2
		self.value = list(set(v1.scu_ids).intersection(set(v2.scu_ids)))


	def get_info(self):
		print "Edge v1 : "+str(self.v1.name)
		print "Edge v2 : "+str(self.v2.name)
		print "Total Value : "+str(self.value)
		print '\n'



class Graph(object):
	def __init__(self, scu_sets):
		self.vertices = []
		self.edges = []
		self.adj_list = {} # Adjacency list #
		self.__generate_initial_graph(scu_sets) # This sets the initial graph


	def __generate_initial_graph(self, scu_sets):
		""" Used to generate graph in the Initial state using input scu_sets  """
		print "----- Generating vertices -------" # First create list of vertices and their elements:
		for name, elements in scu_sets.iteritems():
			v = Vertex(name, elements)
			self.vertices.append(v)
			v.get_info()

		print "----- Generating edges -------" # Then, create list of edges:
		self.edges = [Edge(self.vertices[i], self.vertices[j]) for i in xrange(len(scu_sets)) for j in xrange(i+1, len(scu_sets)) if self.__is_edge(self.vertices[i], self.vertices[j])]
		for e in self.edges:
			print e.get_info()

		# Finished generating V,E | Components of Graph | Now generate graph by creating an adjacency list representation
		self.__generate_adjacency_list()
		return self.adj_list


	def __get_vertex_by_name(self, name):
		for v in self.vertices:
			if v.name == name:
				return v
		return None


	def get_graph(self):
		""" Will return graph at any stage """
		self.__generate_adjacency_list()
		self.get_info()
		return self.adj_list


	def __is_edge(self,v1, v2):
		""" Pass input of type Vertex | Returns true if two vertices have an element in common; hence edge in common | Else, false """
		return bool(set(v1.scu_ids) & set(v2.scu_ids))


	def __add_to_adjlist(self,k, v):
		""" k : key | v : value """
		if k in self.adj_list:
			self.adj_list[k].append(v)
		else:
			self.adj_list[k] = [v]


	def __generate_adjacency_list(self):
		""" Take self.edges list, for edge, make v1 a key, append/add v2 as a value & vice-versa -> Since undirected graph |
		Returns neighborhood for each vertex """
		self.adj_list = {} # Since we are re-generating it now # 
		for edge in self.edges:
			# Since undirected;
			self.__add_to_adjlist(edge.v1, edge.v2)
			self.__add_to_adjlist(edge.v2, edge.v1)


	def __get_edges_by_vertex(self, vertex):
		""" Return all edges where one end is the vertex """
		ver_edges = [edge for edge in self.edges if edge.v1 == vertex or edge.v2 == vertex]
		return ver_edges


	def __remove_vertex(self, vertex, gen_adjl = True):
		""" Removes vertex from self.vertices and each edge in self.edges that contains the vertex; thereby eliminating vertex from adj_list i.e Graph henceforth |
		the gen_adjl flag will re-generate graph by default as soon as a vertex is removed | However, if we want to call this function to remove 
		a neighborhood, it serves to be more efficient if the graph is regenerated in the end, after each vertex has been pruned out, 
		in which case, set 'gen_adjl = False' """
		ver_edges = self.__get_edges_by_vertex(vertex)
		for e in ver_edges:
			# print "Removing edge between : "+ e.v1.name + " & "+e.v2.name, len(ver_edges)
			self.edges.remove(e)

		self.vertices.remove(vertex)
		if gen_adjl:
			self.__generate_adjacency_list()


	def __remove_vertex_neighborhood(self, vertex):
		""" Removes the neighborhood of the vertex & the vertex itself from the graph.
		1. If all neighbors edges removed, all of it's own edges are removed too! So no need to do same operation for vertex itself. 
		2. Remove vertex from this.vertices """
		all_neighbors = self.adj_list[vertex]
		for neighbor in all_neighbors:
			self.__remove_vertex(neighbor, False)
		self.vertices.remove(vertex)
		print '-----REMOVED NEIGHBORS! Regenerate adj list : -----'
		self.__generate_adjacency_list()
		self.get_info()
		print '----------'

	
	def __gwdegree(self, vertex):
		""" PLUGIN : Greedy algo (1) cost function/weight specified in GWMIN paper """
		return float(vertex.weight)/float(len(self.adj_list[vertex]) + 1)


	def __gwmin(self, vertex):
		""" PLUGIN : Greedy algo (2) cost function/weight specified in GWMIN paper """
		n_weight = sum([neighbor.weight for neighbor in self.adj_list[vertex]]) # sum of weights of each vertex in neighborhood
		return float(vertex.weight)/float(n_weight)


	def __get_gwm_wt(self, vertex):
		""" Algo_type = 1 : greedy algo 1 using den = degree + 1 | Algo_type = 2 : greedy algo 2 using den = weight(neighborhood) 
		Default is algo_type = 2"""
		global algo_type
		if algo_type == 1:
			return self.__gwdegree(vertex)
		else:
			return self.__gwmin(vertex)


	def __get_optimal_vertex(self):
		""" For graph, returns vertex s.t max v [W(vertex)/W(neighborhood)]"""
		opt_vertex = None
		max_gwm = -1
		for vertex in self.vertices:
			print '- vertex : '+str(vertex.name)+" | Wt : "
			# gwm_wt = self.__gwdegree(vertex) # (1)
			# gwm_wt = self.__gwmin(vertex) # (2)
			gwm_wt = self.__get_gwm_wt(vertex)
			print gwm_wt
			if gwm_wt > max_gwm:
				max_gwm = gwm_wt
				opt_vertex = vertex
		print "---OPT ----", opt_vertex.name
		return opt_vertex


	def get_maximal_independent_set(self):
		"""Returns the maximal independent set for the graph by choosing max. gwmin vertex at eaxh iteration 
		1. While graph:
			a. Choose optimal vertex
			b. Insert optimal vertex into solution
			c. * Remove neighborhood of the opt-vertex from the graph * [ Remove opt-vertex from graph  ]
			d. _REPEAT_
		"""
		max_indep_set = []
		while len(self.edges) > 0:
			optimal_vertex = self.__get_optimal_vertex()
			max_indep_set.append(optimal_vertex)
			self.__remove_vertex_neighborhood(optimal_vertex) # remove neighbors + vertex itself
		return max_indep_set


	def get_info(self):
		for k,v in self.adj_list.iteritems():
			print 'Key :', str(k.name)
			for e in v:
				print 'Value :', str(e.name)
			print '\n'


s = {1 : [103, -1],
2 :[100, -1],
3 :[105, -2],
4 :[110, -2],
5 :[100, 110, -2],
6 :[105, -3],
7 :[100, 105, -3],
8 :[121, 105, -3],
9 :[138, -4],
10 :[137, -4],
11 :[136, -7],
12 :[136, 119, -7],
13 :[119, -7],
14 :[100, -8],
15 :[100, 136, -8],
16 :[100, 119, -8],
17 :[100, -9],
18 :[136, 100, -9]
}


def main(a_type):
	global algo_type
	algo_type = int(a_type) # Setting the algorithm type!
	# SCU_SETS toy value #
	# s = {
	# 'A' : [1, 5],
	# 'B' : [2, 4],
	# 'C' : [2, 3],
	# 'D' : [3],
	# 'E' : [1, 4, 5]
	# }
	g = Graph(s)
	g.get_info() # Here, returning graph in the initial state # 
	max_set = g.get_maximal_independent_set()
	print 'MAXIMAL SET : (Set names and elements) :-'
	for e in max_set:
		print e.name, e.scu_ids



def usage():
    sys.stderr.write("""
    Usage: Generate Maximal Independent set.
    Execute this file by writing 'python gwmin.py <int algorithm type value>' 
    where int value = 1 => Algo 1 OR value = 2 => Algo 2 | Algo 2 performs better! \n""")



if __name__ == "__main__": 
	if ((len(sys.argv) != 2) or (not sys.argv[1].isdigit())):
		usage()
		sys.exit(1)	
	main(sys.argv[1])


"""
Debugging statements:
# print "----- OLD EDGES -------" 
# for e in self.edges:
# 	print e.get_info()
# 	print self.adj_list[vertex]
# print "----- OLD EDGES end -------" 

# print "----- NEW EDGES after removing neighbor's edges of vertex -------" 
# for e in self.edges:
# 	print e.get_info()
# print "----- NEW VERTICES -------" 
# for v in self.vertices:
# 	print v.name

# def __gwdegree(self, vertex):
# print "vertex weight : ", float(vertex.weight)
# print "den : ", float(len(self.adj_list[vertex]) + 1)
"""
