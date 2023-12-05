import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import numpy as np
data = []
with open('evaluation_scores_full4.txt', 'r') as file:
    for line in file:
        parts = line.strip().split(':')
        if len(parts) == 2:
            scores_str = parts[1].strip().strip('[]')
            scores = [float(score) for score in scores_str.split(',')]
            data.append(scores)


df = pd.DataFrame(data)

# scale data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# 0ptimal Number of Clusters with elbow method, should be 3 
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    sse.append(kmeans.inertia_)

#Plotting the Elbow Method graph
# plt.plot(range(1, 11), sse, marker='o')
# plt.title('Elbow Method')
# plt.xlabel('Number of clusters')
# plt.ylabel('SSE')
# plt.show()



optimal_clusters = 3  #4
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
clusters = kmeans.fit_predict(scaled_data)

#labels to the Original Data
df['Cluster'] = clusters
clus_means = df.groupby('Cluster').mean()
print(clus_means)

# clus_means.to_csv('clustered_evaluation_scores.csv', index=False)

# def assign_label(cluster):
#     if cluster == 0:
#         return ' Very High Quality'
#     elif cluster == 3:
#         return 'High Quality'
#     elif cluster == 1:
#         return 'Moderate Quality'
#     else:
#         return 'Low Quality'
def assign_label(cluster):
    if cluster == 0:
        return 'Low Quality'
    elif cluster == 1:
        return 'High Quality'
    else:
        return 'Moderate Quality'

df['Label'] = df['Cluster'].apply(assign_label)


clus_means1 = df.groupby('Label').mean()


# print(clus_means1)
print(df)
label_counts = df['Label'].value_counts()

# Print the count for each category
print(label_counts)
moderate_quality_rows = df[df['Label'] == 'Moderate Quality']

# Print the moderate quality rows
print(moderate_quality_rows)

from sklearn.preprocessing import MinMaxScaler

# cluster means
high_quality_means = np.array([0.952344, 0.924219, 0.954688, 0.882812, 0.369531, 0.864844, 0.582812, 0.868750, 0.842969, 0.797656, 0.878125, 0.964063, 0.933594, 0.978125])
low_quality_means = np.array([0.159259, 0.062963, 0.338889, 0.072222, 0.092593, 0.066667, 0.011111, 0.037037, 0.012963, 0.051852, 0.540741, 0.275926, 0.466667, 0.312963])
moderate_quality_means = np.array([0.505405, 0.064865, 0.540541, 0.054054, 0.000000, 0.067568, 0.000000, 0.008108, 0.008108, 0.029730, 0.905405, 0.621622, 0.791892, 0.772973]
)

# to account for variability in the difference between high and low means across dimensions:
ranges = np.max([high_quality_means, moderate_quality_means, low_quality_means], axis=0) - np.min([high_quality_means, moderate_quality_means, low_quality_means], axis=0)

def adjusted_euclidean_distance(vec1, vec2, ranges):
    # normalize the difference in each dimension by the range of that dimension across the clusters
    weighted_diff = ((vec1 - vec2) / ranges) ** 2
    return np.sqrt(np.sum(weighted_diff))

# adjusted by dividing the difference in each dimension by the range of that dimension across the clusters, making the distance scale-invariant.
def classify_text(scores):
    scores = np.array(scores)
    distances = {
        'High Quality': adjusted_euclidean_distance(scores, high_quality_means, ranges),
        'Moderate Quality': adjusted_euclidean_distance(scores, moderate_quality_means, ranges),
        'Low Quality': adjusted_euclidean_distance(scores, low_quality_means, ranges)
    }

    return min(distances, key=distances.get)

# chandra
sample_scores = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.8, 1.0, 0.5, 0.8, 0.7, 1.0, 0.8, 1.0]
sample_scores1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sample_scores2 =[1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#jwebb2
sample_scores3 = [0.7, 0.8, 0.9, 0.0, 0.0, 0.6, 0.0, 0.7, 0.5, 0.0, 0.8, 0.9, 0.8, 1.0]
#jwebb1
sample_scores4 = [0.9, 0.9, 0.8, 0.0, 0.0, 0.5, 0.0, 0.5, 0.7, 0.6, 0.9, 0.9, 0.9, 1.0]
classification = classify_text(sample_scores)
classification1 = classify_text(sample_scores1)
classification2 = classify_text(sample_scores2)
classification3 = classify_text(sample_scores3)
classification4 = classify_text(sample_scores4)


print(f"The classification of the text is: {classification}")
print(f"The classification of the text is: {classification1}")
print(f"The classification of the text is: {classification2}")
print(f"The classification of the text is: {classification3}")
print(f"The classification of the text is: {classification4}")





# def plot_sawtooth(cluster_means, label, linestyle):
#    
#     extended_means = np.hstack(([cluster_means[0]], cluster_means, [cluster_means[-1]]))
#     plt.plot(extended_means, label=label, linestyle=linestyle)

# plot_sawtooth(high_quality_means, 'High Quality', '-')
# plot_sawtooth(moderate_quality_means, 'Moderate Quality', '--')
# plot_sawtooth(low_quality_means, 'Low Quality', '-.')

# # Adding titles and labels
# plt.title('Sawtooth Visualization of Cluster Means')
# plt.xlabel('Dimension')
# plt.ylabel('Mean Score')
# plt.legend()
# plt.grid(True)
# plt.show()
#UNCOMMENT FOR SAWTOOTH VISUALIZATION OF CLUSTER MEANS
plt.figure(figsize=(10, 6))

plt.plot(high_quality_means, marker='o', linestyle='-', color='b', label='High Quality')
plt.plot(low_quality_means, marker='o', linestyle='-', color='r', label='Low Quality')
plt.plot(moderate_quality_means, marker='o', linestyle='-', color='g', label='Moderate Quality')

plt.title('Sawtooth Visualization of Means')
plt.xlabel('Dimensions')
plt.ylabel('Mean Value')
plt.grid(True)
plt.legend()  

plt.ylim(0, 1)

plt.show()




# # #use these to now create a classification model
# # #.each alt-text's score vector is a feature set, and the cluster label is the target variable.
# # #for a new alt-text, compute its score vector and pass it through the model to get a classification into good, bad, or moderate.
# # #define thresholds based on cluster avgs,then a scoring system. 
# # #get the means, and the distance information
# # #eg:  if an alt-text scores above a certain threshold in most dimensions,
# # #  classify it as 'good'; if it falls below in most, classify it as 'bad'; otherwise, 'moderate'
# # # normalize (fudge factor) treating all distances as same wont work (refer 11/4)
# # #work on scaling (.4 away from 10-13 more salient than eg6)
# # # visualiseas a sawtooth


#upload github/start presentation
#each evaluation is around 3-4 cents
#nasa spens $6k
