import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from collections import Counter

def fetch_webpage(url):
    """Fetch and parse the webpage content"""
    headers = {
        "User-Agent": "lab07-web-analyzer"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Successfully fetched content from {url}")
        return soup
    except Exception as e:
        print(f"Error fetching content: {e}")
        return None

def count_headings(soup):
    """Count all heading tags (h1 to h6)"""
    headings_count = 0
    for i in range(1, 7):  
        headings = soup.find_all(f'h{i}')
        headings_count += len(headings)
    return headings_count

def count_links(soup):
    """Count all link tags (a tags)"""
    links = soup.find_all('a')
    return len(links)

def count_paragraphs(soup):
    """Count all paragraph tags (p tags)"""
    paragraphs = soup.find_all('p')
    return len(paragraphs)

def word_frequency_analysis(soup):
    """Analyze word frequency and display top 5 most common words"""
    text = soup.get_text()
    
    text = text.lower()
    
    words = re.findall(r'\b\w+\b', text)
    
    word_counts = Counter(words)
    
    top_5 = word_counts.most_common(5)
    
    print("\n=== Top 5 Most Frequent Words ===")
    for word, count in top_5:
        print(f"{word}: {count}")
    
    return top_5

def keyword_search(soup):
    """Search for a keyword in the webpage content"""
    text = soup.get_text().lower()
    
    keyword = input("\nEnter a keyword to search for: ")
    keyword_lower = keyword.lower()
    
    
    count = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', text))
    
    print(f"\nThe keyword '{keyword}' appears {count} times in the webpage.")
    return count

def find_longest_paragraph(soup):
    """Find and display the longest paragraph with at least 5 words"""
    paragraphs = soup.find_all('p')
    longest_paragraph = None
    max_words = 0
    longest_text = ""
    
    for p in paragraphs:
        text = p.get_text().strip()
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        
        if word_count >= 5 and word_count > max_words:
            max_words = word_count
            longest_text = text
            longest_paragraph = p
    
    print("\n=== Longest Paragraph ===")
    if longest_paragraph:
        print(f"Number of words: {max_words}")
        print(f"Paragraph content: {longest_text[:500]}...")  
    else:
        print("No paragraph with at least 5 words found.")
    
    return max_words, longest_text

def visualize_results(headings_count, links_count, paragraphs_count):
    """Create a bar chart showing counts of headings, links, and paragraphs"""
    labels = ['Headings', 'Links', 'Paragraphs']
    values = [headings_count, links_count, paragraphs_count]
    
    plt.bar(labels, values, color=['skyblue', 'lightgreen', 'lightcoral'])
    plt.title('Group #: 2')
    plt.ylabel('Count')
    plt.xlabel('Element Type')
    
    for i, v in enumerate(values):
        plt.text(i, v + max(values) * 0.02, str(v), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('web_analysis_results.png')  
    plt.show()

def main():
    """Main function to run the web analyzer"""
    print("=== Web Analyzer Tool ===\n")
    
    url = "https://en.wikipedia.org/wiki/University_of_Calgary"
    
    soup = fetch_webpage(url)
    
    if soup:
        print("\n=== Data Analysis ===")
        headings_count = count_headings(soup)
        links_count = count_links(soup)
        paragraphs_count = count_paragraphs(soup)
        
        print(f"Number of headings (h1-h6): {headings_count}")
        print(f"Number of links (a tags): {links_count}")
        print(f"Number of paragraphs (p tags): {paragraphs_count}")
        
        
        word_frequency_analysis(soup)
        
        keyword_search(soup)
        
        find_longest_paragraph(soup)
        
        visualize_results(headings_count, links_count, paragraphs_count)
        
        print("\n=== Analysis Complete ===")
        print("The chart has been saved as 'web_analysis_results.png'")

if __name__ == "__main__":
    main()