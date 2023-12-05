import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'alt_data.csv'
df = pd.read_csv(csv_file)

#   calculate word count in a text
def word_count(text):
    words = text.split()
    return len(words)

#  word count for each row
word_counts = [word_count(text) for text in df['Alt Text']]

plt.figure(figsize=(10, 6))
plt.plot(range(1, len(word_counts) + 1), word_counts, marker='o', linestyle='-', color='b')
plt.title('Word Count per Row')
plt.xlabel('Row Number')
plt.ylabel('Word Count')
plt.grid(True)

# Show the graph
plt.tight_layout()
plt.show()
