#! /usr/bin/python  
import math

class DBSCAN:  
#Density-Based Spatial Clustering of Application with Noise -> http://en.wikipedia.org/wiki/DBSCAN  
	def __init__(self):  
		self.name = 'DBSCAN'  
		self.DB = [] #Database  
		self.esp = 500 #neighborhood distance for search  
		self.MinPts = 5 #minimum number of points required to form a cluster  
		self.cluster_inx = -1
		self.cluster = []
      
	def DBSCAN(self):
		noise = 0
		# print len(self.DB)
		for i in range(len(self.DB)):  
			p_tmp = self.DB[i]  
			if (not p_tmp.visited):  
				#for each unvisited point P in dataset  
				p_tmp.visited = True  
				NeighborPts = self.regionQuery(p_tmp)  
				if(len(NeighborPts) < self.MinPts):  
					#that point is a noise  
					p_tmp.isnoise = True
					noise += 1
				else:
					self.cluster.append([])
					self.cluster_inx = self.cluster_inx + 1
					self.expandCluster(p_tmp, NeighborPts)

		retCluster = []
		# print "Noise points", noise
		# print "Clusters found", len(self.cluster)
		for i in range(len(self.cluster)):
			cluster = self.cluster[i]
			x = 0
			y = 0
			for p in cluster:
				x += p.x
				y += p.y
			x = x/len(cluster)
			y = y/len(cluster)
			c = Cluster(x, y, len(cluster))
			clus = c.dictize()
			retCluster.append(clus)
  
		return retCluster
      
	def expandCluster(self, P, neighbor_points):
		self.cluster[self.cluster_inx].append(P)  
		iterator = iter(neighbor_points)  
		while True:  
			try:   
				npoint_tmp = iterator.next()  
			except StopIteration:  
			# StopIteration exception is raised after last element  
				break  
			if (not npoint_tmp.visited): 
        #for each point P' in NeighborPts   
				npoint_tmp.visited = True  
				NeighborPts_ = self.regionQuery(npoint_tmp)  
				if (len(NeighborPts_) >= self.MinPts):  
					for j in range(len(NeighborPts_)):  
						neighbor_points.append(NeighborPts_[j])  
			if (not self.checkMembership(npoint_tmp)):  
			#if P' is not yet member of any cluster  
				self.cluster[self.cluster_inx].append(npoint_tmp)
  
	def checkMembership(self, P):
		#will return True if point is belonged to some cluster  
		ismember = False
		for i in range(len(self.cluster)):  
			for j in range(len(self.cluster[i])):  
				if (P.x == self.cluster[i][j].x and P.y == self.cluster[i][j].y):  
					ismember = True  
		return ismember 
      
	def regionQuery(self, P):  
	#return all points within P's eps-neighborhood, except itself
		pointInRegion = []
		for i in range(len(self.DB)):
			p_tmp = self.DB[i]
			if (self.dist(P, p_tmp) < self.esp and P.x != p_tmp.x and P.y != p_tmp.y):
				pointInRegion.append(p_tmp)
		return pointInRegion

	def dist(self, p1, p2):
		#return distance between two point  
		degrees_to_radians = math.pi/180.0
		if(p1.x == p2.x and p1.y == p2.y):
			return 0
		else:
		# phi = 90 - latitude
			phi1 = (90.0 - p1.x)*degrees_to_radians
			phi2 = (90.0 - p2.x)*degrees_to_radians
			# theta = longitude
			theta1 = p2.y*degrees_to_radians
			theta2 = p2.y*degrees_to_radians

	# Compute spherical distance from spherical coordinates.
	# For two locations in spherical coordinates 
	# (1, theta, phi) and (1, theta, phi)
	# cosine( arc length ) = 
	#    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
	# distance = rho * arc length
			cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
			arc = math.acos( cos )

	# Remember to multiply arc by the radius of the earth 
	# in your favorite set of units to get length.
			return arc*6371

class Point:  
	def __init__(self, x = 0, y = 0, visited = False, isnoise = False):  
		self.x = x
		self.y = y
		self.visited = False
		self.isnoise = False

	def show(self):
		return self.x, self.y
      
if __name__=='__main__':  
	#this is a mocking data just for test  
	pointSet = []
  
	#Create object  
	dbScan = DBSCAN()
	#Load data into object
	dbScan.DB = vecPoint;
	#Do clustering
	dbScan.DBSCAN()
  #Show result cluster
	# for i in range(len(dbScan.cluster)):
	# 	 print 'Cluster: ', i
	# for j in range(len(dbScan.cluster[i])):
	# 	print dbScan.cluster[i][j].show()
	  
class Cluster:
	def __init__(self, lat = 0, long = 0, size = 0):
		self.centroid = [lat, long]
		self.size = size
	def dictize(self):
		cluster = {}
		cluster['centroid'] = [self.centroid[0], self.centroid[1]]
		cluster['size'] = self.size
		return cluster