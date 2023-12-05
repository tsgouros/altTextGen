import pandas as pd
import re
import matplotlib.pyplot as plt
from scipy.stats import f_oneway 
#three files with vector results from differnt prompts
file_paths = [
    "evaluation_scores.txt",
    "evaluation_scores2.txt",
    "evaluation_scores3.txt"
]

file_contents = []
for file_path in file_paths:
    with open(file_path, 'r') as file:
        file_contents.append(file.read())

file_contents_preview = [content.split('\n')[:5] for content in file_contents]
file_contents_preview

def parse_data_dynamic(contents):
    data = []
    for line in contents:
        if line.strip():
            # Extracting the pair number, text type (Good/Bad), and scores
            match = re.match(r'Scores for pair_(\d+) - (Good|Bad) Text: \[([0-9., ]+)\]', line)
            if match:
                pair_num = int(match.group(1))
                text_type = match.group(2)
                scores = [float(score) for score in match.group(3).split(', ')]
                data.append((pair_num, text_type, scores))
    return data

# parsing data from each file
data_list_dynamic = []
for i, content in enumerate(file_contents):
    parsed_data = parse_data_dynamic(content.split('\n'))
    for pair_num, text_type, scores in parsed_data:
        data_list_dynamic.append([i+1, pair_num, text_type] + scores)

for index, row in enumerate(data_list_dynamic):
    if len(row) != 17:
        print(f"Row {index} has incorrect number of elements: {len(row)} elements")
        print(row)  # Optionally print the row to inspect it

assert all(len(row) - 3 == 14 for row in data_list_dynamic), "Not all rows have 14 score dimensions"

max_dims = 14 #max(len(row) - 3 for row in data_list_dynamic)  # -3 for Prompt, Pair, Text_Type

columns_dynamic = ['Prompt', 'Pair', 'Text_Type'] + [f'Dim_{i+1}' for i in range(max_dims)]
df_dynamic = pd.DataFrame(data_list_dynamic, columns=columns_dynamic)

df_dynamic.head()
#print(df_dynamic.head())

df_filled = df_dynamic.fillna(0)

#one for good texts and one for bad texts
df_good = df_filled[df_filled['Text_Type'] == 'Good']
df_bad = df_filled[df_filled['Text_Type'] == 'Bad']

#align
df_good = df_good.sort_values(by=['Prompt', 'Pair'])
df_bad = df_bad.sort_values(by=['Prompt', 'Pair'])

#  the diff in scores for good and bad texts for each dimension
df_diff = df_good.copy()
for col in df_good.columns[3:]:
    df_diff[col] = df_good[col] - df_bad[col]

#  unnecessary column
df_diff = df_diff.drop(columns=['Text_Type'])



# merge good and bad df on 'Prompt' and 'Pair' columns
df_merged = pd.merge(df_good, df_bad, on=['Prompt', 'Pair'], suffixes=('_good', '_bad'))

#  differences in scores between good and bad texts for each dimension
for dim in range(1, max_dims + 1):
    dim_col = f'Dim_{dim}'
    df_merged[f'{dim_col}_diff'] = df_merged[f'{dim_col}_good'] - df_merged[f'{dim_col}_bad']

# Kkeeping only the difference columns,  with 'Prompt' and 'Pair'
diff_columns = [f'Dim_{i}_diff' for i in range(1, max_dims + 1)]
df_diff_corrected = df_merged[['Prompt', 'Pair'] + diff_columns]

print(df_diff_corrected.head())

# aggregate qnalysis: calculating mean, median, and standard deviation for each dimension and prompt
aggregate_stats = df_diff_corrected.groupby('Prompt')[diff_columns].agg(['mean', 'median', 'std'])

# statistical analysis: ANOVA for each dimension across prompts
anova_results = {}
for dim in diff_columns:
    anova_data = [df_diff_corrected[df_diff_corrected['Prompt'] == i][dim] for i in df_diff_corrected['Prompt'].unique()]
    anova_results[dim] = f_oneway(*anova_data)

# sawtooth plot
plt.figure(figsize=(15, 6))
for prompt in df_diff_corrected['Prompt'].unique():
    subset = df_diff_corrected[df_diff_corrected['Prompt'] == prompt].mean()[1:]  # Excluding 'Pair' from means
    plt.plot(subset, label=f'Prompt {prompt}', marker='o')

# plt.xticks(range(len(diff_columns)), diff_columns, rotation=45)
# plt.xlabel('Dimensions')
# plt.ylabel('Average Difference Score')
# plt.title('Sawtooth Plot of Average Score Differences Across Dimensions for Each Prompt')
# plt.legend()
# plt.grid(True)
# plt.show()

# Displaying aggregate statistics and ANOVA test results
print(anova_results)
print(aggregate_stats)

# from sklearn.cluster import KMeans
# import pandas as pd

# X = df_diff_corrected.iloc[:, 2:]  # Excluding 'Prompt' and 'Pair' columns

# # normalize the features if necessary
# # from sklearn.preprocessing import StandardScaler
# # scaler = StandardScaler()
# # X_scaled = scaler.fit_transform(X)

# k = 3  #  'good', 'moderate', 'bad'

# # Running K-means clustering
# kmeans = KMeans(n_clusters=k, random_state=0).fit(X)

# # The cluster assignments for each alt text are stored in kmeans.labels_
# df_diff_corrected['Cluster'] = kmeans.labels_

# # Analyzing the centroids to understand the 'profile' of each cluster
# centroids = kmeans.cluster_centers_

# # print the mean values of the dimensions for each cluster
# for i in range(k):
#     print(f"Cluster {i} centroid:", centroids[i])

# # You can also explore how many alt texts are in each cluster
# print(df_diff_corrected['Cluster'].value_counts())
