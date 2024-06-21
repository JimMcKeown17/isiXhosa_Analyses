import os
import PyPDF2
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import csv

# Path to the directory containing the PDF files
directory_path = 'isiXhosa All Stories'

# List of consonant clusters to track
consonant_clusters = [
    'mb', 'mf', 'mp', 'mv', 'ts', 'ty', 'gc', 'gq', 'gx', 'dy', 'dz', 'nc', 'nd', 'ng', 'nj', 'nk', 'nq', 'nt', 'nx', 'ny', 'nz',
    'dl', 'hl', 'bh', 'ch', 'kh', 'ph', 'qh', 'th', 'xh', 'sh', 'rh', 'gr', 'kr', 'tr', 'cw', 'dw', 'gw', 'kw', 'lw', 'nw', 'qw',
    'sw', 'tw', 'xw', 'zw', 'ndl', 'ngc', 'ngq', 'ngw', 'ngx', 'ntl', 'nts', 'nty', 'tsh', 'ncw', 'ndw', 'nkw', 'nqw', 'ntw',
    'nxw', 'nzw', 'nyh', 'tyh', 'chw', 'khw', 'qhw', 'thw', 'gcw', 'gqw', 'hlw', 'krw', 'tsw', 'tyw', 'shw', 'nkc', 'nkq', 'nkx',
    'ntsh', 'ngcw', 'ndlw', 'ntyw'
]
consonant_count = {}
total_words = 0
# Initialize the consonant count dictionary
for cluster in consonant_clusters:
    consonant_count[cluster] = 0

for filename in os.listdir(directory_path):
    if filename.endswith('.pdf'):
        file_path = os.path.join(directory_path, filename)

        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    words = text.split()
                    total_words += len(words)
                    for word in words:
                        cleaned_word = word.lower().replace('/', '').replace('-', '')
                        for cluster in consonant_clusters:
                            consonant_count[cluster] += cleaned_word.count(cluster)

# Create a word cloud from consonant frequencies
wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(consonant_count)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('isiXhosa_consonant_wordcloud.png', format='png')
plt.show()

# Export the most common consonants to a CSV file
sorted_consonants = sorted(consonant_count.items(), key=lambda x: x[1], reverse=True)
with open('most_common_isixhosa_consonants.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Consonant Cluster', 'Count'])
    writer.writerows(sorted_consonants)

print(f"We evaluated {total_words} words.")
print("Most common consonant clusters:", sorted_consonants)  # Print all consonant counts for quick viewing

# Create a bar chart for the top 20 most common consonant clusters
top_20_consonants = sorted_consonants[:20]
consonant_labels, consonant_counts = zip(*top_20_consonants)

plt.figure(figsize=(12, 8))
plt.barh(consonant_labels, consonant_counts, color='skyblue')
plt.xlabel('Count')
plt.ylabel('Consonant Cluster')
plt.title('Top 20 Most Common Consonant Clusters in isiXhosa Texts')
plt.gca().invert_yaxis()  # Invert y-axis to have the highest count at the top
plt.savefig('isiXhosa_top_20_consonants.png', format='png')
plt.show()
