import matplotlib.pyplot as plt
from geopy.distance import great_circle
from shapely.geometry import MultiPoint
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
import folium
import webbrowser




coordenadas = np.array([
[-15.7942, -47.8825],
[-15.7935, -47.8820],
[-15.7932, -47.8818],
[-15.7929, -47.8815]
])



kms_per_radian = 6371.0088
epsilon = 1.5 / kms_per_radian
db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coordenadas))
print(db.labels_)


def add_markers(map, points, label):
    for coord in points:
        folium.Marker(location=[coord[0], coord[1]], popup=label).add_to(map)

map_clusters = folium.Map(location=[np.mean(coordenadas[:,0]), np.mean(coordenadas[:,1])], zoom_start=4)

unique_labels = set(db.labels_)
for cluster_label in unique_labels:
    cluster_points = coordenadas[db.labels_ == cluster_label]
    if cluster_label == -1:
        add_markers(map_clusters, cluster_points, 'Outlier')
    else:
        add_markers(map_clusters, cluster_points, f'Cluster {cluster_label}')
        

map_clusters.save('cluster_map.html')
webbrowser.open('cluster_map.html')
