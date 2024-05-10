import os
import fitz  # Import PyMuPDF correctly
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import csv

directory_path = 'isiXhosa Stories'
word_count = {}
letter_count = {}

for filename in os.listdir(directory_path):
    if filename.endswith('.pdf'):
        file_path = os.path.join(directory_path, filename)
        try:
            document = fitz.open(file_path)
            for page in document:
                text = page.get_text()
                if text:
                    words = text.split()
                    for word in words:
                        cleaned_word = word.lower().replace('/', '').replace('-', '')
                        if len(cleaned_word) > 1:
                            word_count[cleaned_word] = word_count.get(cleaned_word, 0) + 1
                        for letter in cleaned_word:
                            if letter.isalpha():
                                letter_count[letter] = letter_count.get(letter, 0) + 1
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

print(f'{len(word_count)} words were analyzed. \n')
wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(word_count)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('isiXhosa_wordcloud.png', format='png')
# plt.show()

# Export the most common words to a CSV file
sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
with open('most_common_isixhosa_words.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Word', 'Count'])
    writer.writerows(sorted_words[:50])  # Adjust the slice as needed for more words

# Export the most common letters to a CSV file
sorted_letters = sorted(letter_count.items(), key=lambda x: x[1], reverse=True)
with open('most_common_isixhosa_letters.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Letter', 'Count'])
    writer.writerows(sorted_letters)  # Export all letter counts

print("Most common words:", sorted_words[:50])  # Print the top 50 words for quick viewing
print("Most common letters:", sorted_letters)  # Print all letter counts for quick viewing
