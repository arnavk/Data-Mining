import sys
import json
import pickle
import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction import DictVectorizer
from operator import itemgetter

f = open('small.txt', 'r')

all = list()
X = list()
labels_true = list()

count = 0

a = f.readline().rstrip('\n')
while(a != ""):
	x = json.loads(a)
	
	single = dict()
	single['x'] = x['coord'][0]
	single['y'] = x['coord'][1]
	all.append(single)
	X.append(x['coord'])
	labels_true.append(count)
	count+=1
	x = None
	a = f.readline().rstrip('\n')
	
f.close()

Y = StandardScaler().fit_transform(X)

dbscan = DBSCAN(eps=0.3, min_samples=1)
db = dbscan.fit(Y)
core_samples = db.core_sample_indices_
labels = db.labels_
components = db.components_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

# Black removed and is used for noise instead.
unique_labels = set(labels)

numLabels = 0

clusterList = list()

g = open('clusters.txt', 'w')
for member in unique_labels:
	# form list of dict
	cluster = dict()
	
	total_x = 0
	total_y = 0
	total = 0
	cluster_core_samples = [index for index in core_samples if labels[index] == member]
	
	for node in cluster_core_samples:
		Node = X[node]
		total+=1
		total_x += Node[0]
		total_y += Node[1]
	
	if(total != 0):
		cluster['label'] = member
		cluster['size'] = total
		cluster['centroid'] = [total_x / total, total_y / total]
		clusterList.append(cluster)

sortedClusterList = sorted(clusterList, key=itemgetter('size'), reverse=True)

for n in range(0,10):
	j = json.dumps(sortedClusterList[n])
	g.write(j + "\n")

g.close
