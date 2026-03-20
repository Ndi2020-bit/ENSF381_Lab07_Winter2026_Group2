import re 
import requests
from bs4 import BeautifulSoup 
from collections import Counter
import matplotlib.pyplot as plt 
url = "https://en.wikipedia.org/wiki/University_of_Calgary" 
headers = { 
"User-Agent": "lab07-web-analyzer" 
} 
try: 
    response = requests.get(url, headers=headers) #Added headers=headers
    response.raise_for_status()  # Ensures the request was successful 
    soup = BeautifulSoup(response.text, 'html.parser') 
    print(f"Successfully fetched content from {url}") 
    print(soup.prettify()) 
    # Count headings (h1 to h6)
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    headings_count = len(headings)
    print("Number of headings:", headings_count)
    
    # Count links
    links = soup.find_all('a')
    links_count = len(links)
    print("Number of links:", links_count)
    
    # Count paragraphs
    paragraphs = soup.find_all('p')
    paragraphs_count = len(paragraphs)
    print("Number of paragraphs:", paragraphs_count)

    # Extract all text from the page
    text = soup.get_text()

    # Convert to lowercase
    text = text.lower()

    # Extract words using regex
    words = re.findall(r'\b\w+\b', text)

    # Count word frequencies
    word_freq = Counter(words)
    print("Most common words:")
    for word, freq in word_freq.most_common(5):
        print(f"  {word}: {freq}")
    
    # Ask user for a keyword
    keyword = input("\nEnter a keyword to search: ").lower()

    # Extract all text and convert to lowercase
    text = soup.get_text().lower()

    # Count occurrences
    count = text.count(keyword)

    # Display result
    print(f"\nThe keyword '{keyword}' appears {count} times in the webpage.")

    # Find all paragraph tags
    paragraphs = soup.find_all('p')

    longest_para = ""
    max_words = 0

    for p in paragraphs:
        text = p.get_text().strip()
        
        # Split into words
        words = text.split()
        
        # Ignore empty or short paragraphs (< 5 words)
        if len(words) < 5:
            continue
        
        # Check if this is the longest so far
        if len(words) > max_words:
            max_words = len(words)
            longest_para = text

    # Display result
    print("\nLongest paragraph:")
    print(longest_para)
    print(f"\nWord count: {max_words}")

    labels = ['Headings', 'Links', 'Paragraphs'] 
    values = [headings_count, links_count, paragraphs_count] 
    plt.bar(labels, values) 
    plt.title('Group 2') 
    plt.xlabel('Element Type')
    plt.ylabel('Count') 
    plt.savefig('web_analysis_results.png')  # Save the figure as an image file 
    plt.show() 

except Exception as e: 
    print(f"Error fetching content: {e}")
