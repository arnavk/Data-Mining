import sys
import json
import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction import DictVectorizer

if len(sys.argv) == 1:
	hashtag = "@"
else:
	hashtag = sys.argv[1]
	
print(hashtag)

f = open('small.txt', 'r')

all = list()
X = list()
labels_true = list()

count = 0

a = f.readline().rstrip('\n')
while(a != ""):
	x = json.loads(a)
	
	for member in x['hashtags']:
		if member == hashtag or hashtag == "@":
			single = dict()
			single['hashtags'] = member
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

dbscan = DBSCAN(eps=0.3, min_samples=2)
db = dbscan.fit(Y)
core_samples = db.core_sample_indices_
labels = db.labels_
components = db.components_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))
	  
# Plot result
import pylab as pl

# Black removed and is used for noise instead.
unique_labels = set(labels)
# colors = pl.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
# for k, col in zip(unique_labels, colors):
    # if k == -1:
        # # Black used for noise.
        # col = 'k'
        # markersize = 6
    # class_members = [index[0] for index in np.argwhere(labels == k)]
    # cluster_core_samples = [index for index in core_samples if labels[index] == k]
							
    # for index in class_members:
        # x = X[index]
        # if index in core_samples and k != -1:
            # markersize = 14
        # else:
            # markersize = 6
        # pl.plot(x[0], x[1], 'o', markerfacecolor=col,
                # markeredgecolor='k', markersize=markersize)
				
				
# pl.title('Estimated number of clusters: %d' % n_clusters_)
# pl.show()

g = open('clusters.txt', 'w')
for member in unique_labels:
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
		avg_x = total_x / total
		avg_y = total_x / total
		g.write(str(avg_x) + " " + str(avg_y) + "\n")
g.close
