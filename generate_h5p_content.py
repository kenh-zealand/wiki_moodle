import json
import re
from bs4 import BeautifulSoup

def parse_html_to_h5p_content():
    """Parse staff-handbook-moodle.html and convert to H5P content.json format"""
    
    with open('staff-handbook-moodle.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract header info
    title_elem = soup.select_one('.wiki-header h1')
    subtitle_elem = soup.select_one('.wiki-header p')
    search_input = soup.select_one('#searchInput')
    
    title = title_elem.get_text(strip=True).replace('📚 ', '') if title_elem else "Personalhåndbog"
    subtitle = subtitle_elem.get_text(strip=True) if subtitle_elem else "Søgbar videnbase for ansatte"
    search_placeholder = search_input.get('placeholder', 'Søg i personalhåndbogen...') if search_input else 'Søg i personalhåndbogen...'
    
    # Extract alphabet sections
    alphabet_sections = []
    
    for section_div in soup.select('.alphabet-section'):
        letter_elem = section_div.select_one('h2')
        letter = letter_elem.get_text(strip=True) if letter_elem else ''
        
        articles = []
        
        for article_details in section_div.select('.article-details'):
            article_summary = article_details.select_one('summary')
            article_title = article_summary.get_text(strip=True) if article_summary else ''
            
            subsections = []
            
            for subsection_details in article_details.select('.subsection-details'):
                subsection_summary = subsection_details.select_one('summary')
                subsection_title = subsection_summary.get_text(strip=True) if subsection_summary else ''
                
                subsection_content_div = subsection_details.select_one('.subsection-content')
                if subsection_content_div:
                    # Get inner HTML as content
                    subsection_content = ''.join(str(child) for child in subsection_content_div.children)
                    subsection_content = subsection_content.strip()
                else:
                    subsection_content = ''
                
                subsections.append({
                    "title": subsection_title,
                    "content": subsection_content
                })
            
            articles.append({
                "title": article_title,
                "subsections": subsections
            })
        
        if articles:  # Only add section if it has articles
            alphabet_sections.append({
                "letter": letter,
                "articles": articles
            })
    
    # Build H5P content structure
    h5p_content = {
        "handbookData": {
            "title": title,
            "subtitle": subtitle,
            "searchPlaceholder": search_placeholder,
            "alphabetSections": alphabet_sections
        }
    }
    
    # Write to content.json
    with open('content.json', 'w', encoding='utf-8') as f:
        json.dump(h5p_content, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Generated content.json with {len(alphabet_sections)} alphabet sections")
    
    # Count articles and subsections
    total_articles = sum(len(section['articles']) for section in alphabet_sections)
    total_subsections = sum(
        len(article['subsections']) 
        for section in alphabet_sections 
        for article in section['articles']
    )
    
    print(f"  - {total_articles} articles")
    print(f"  - {total_subsections} subsections")

if __name__ == '__main__':
    parse_html_to_h5p_content()
