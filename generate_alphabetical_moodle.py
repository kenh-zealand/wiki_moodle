import re
import json
from collections import defaultdict

# Danish alphabet order
DANISH_ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
                   'Æ', 'Ø', 'Å']

def read_js_knowledge_base(filename):
    """Read the knowledge base from JS file"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the array content
    match = re.search(r'const knowledgeBase = \[(.*?)\];', content, re.DOTALL)
    if not match:
        return []
    
    # Parse each article
    articles = []
    article_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    
    for article_match in re.finditer(article_pattern, match.group(1)):
        article_text = article_match.group(0)
        
        # Extract fields
        title_match = re.search(r'title:\s*"([^"]*)"', article_text)
        content_match = re.search(r'content:\s*`(.*?)`', article_text, re.DOTALL)
        
        if title_match and content_match:
            articles.append({
                'title': title_match.group(1),
                'content': content_match.group(1).strip()
            })
    
    return articles

def get_first_letter(title):
    """Get first letter in Danish alphabet order"""
    first = title[0].upper()
    if first in DANISH_ALPHABET:
        return first
    return 'A'  # Default

def parse_content_to_subsections(content):
    """Parse content into subsections based on H3 and strong tags"""
    subsections = []
    
    # Split by H3 tags
    h3_pattern = r'<h3>(.*?)</h3>(.*?)(?=<h3>|$)'
    h3_matches = re.finditer(h3_pattern, content, re.DOTALL | re.IGNORECASE)
    
    remaining_content = content
    h3_found = False
    
    for match in h3_matches:
        h3_found = True
        h3_title = match.group(1).strip()
        h3_content = match.group(2).strip()
        
        # Skip if this is the main article title
        if not subsections:
            # Check for strong subsections within this h3 section
            strong_subsections = parse_strong_subsections(h3_content)
            if strong_subsections:
                subsections.extend(strong_subsections)
            elif h3_content:
                subsections.append({
                    'title': h3_title,
                    'content': h3_content
                })
        else:
            # Check for strong subsections
            strong_subsections = parse_strong_subsections(h3_content)
            if strong_subsections:
                subsections.extend(strong_subsections)
            elif h3_content:
                subsections.append({
                    'title': h3_title,
                    'content': h3_content
                })
    
    # If no H3 found, look for strong tags
    if not h3_found or not subsections:
        strong_subsections = parse_strong_subsections(content)
        if strong_subsections:
            subsections.extend(strong_subsections)
    
    return subsections

def parse_strong_subsections(content):
    """Parse strong tags as subsections"""
    subsections = []
    
    # Pattern to find <strong>Title</strong> followed by content
    strong_pattern = r'<li><strong>(.*?)</strong>(.*?)(?=<li><strong>|</ul>|$)'
    matches = re.finditer(strong_pattern, content, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        title = match.group(1).strip()
        subcontent = match.group(2).strip()
        
        if subcontent:
            subsections.append({
                'title': title,
                'content': subcontent
            })
    
    return subsections

def group_by_letter(articles):
    """Group articles by first letter"""
    grouped = defaultdict(list)
    
    for article in articles:
        letter = get_first_letter(article['title'])
        grouped[letter].append(article)
    
    # Sort by Danish alphabet order
    sorted_groups = {}
    for letter in DANISH_ALPHABET:
        if letter in grouped:
            # Sort articles within each letter alphabetically
            sorted_groups[letter] = sorted(grouped[letter], key=lambda x: x['title'])
    
    return sorted_groups

def generate_html(grouped_articles):
    """Generate the new HTML structure"""
    
    html = '''<!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personalhåndbog - Moodle Wiki</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        
        .wiki-container {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .wiki-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .wiki-header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .wiki-header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .search-container {
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }
        
        .search-box {
            position: relative;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .search-box input {
            width: 100%;
            padding: 15px 50px 15px 20px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 50px;
            outline: none;
            transition: all 0.3s;
        }
        
        .search-box input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .search-icon {
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: #999;
        }
        
        .main-content {
            padding: 30px;
        }
        
        /* Alphabet Section Styling */
        .alphabet-section {
            margin-bottom: 50px;
        }
        
        .alphabet-section > h2 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            font-weight: 700;
        }
        
        /* Level 2: Article Details */
        .article-details {
            margin: 15px 0;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            background: #fff;
        }
        
        .article-details summary {
            padding: 15px 50px 15px 20px;
            cursor: pointer;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 6px;
            font-weight: 700;
            font-size: 1.3em;
            color: #495057;
            list-style: none;
            position: relative;
            transition: all 0.3s;
        }
        
        .article-details summary::-webkit-details-marker {
            display: none;
        }
        
        .article-details summary::after {
            content: '▼';
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            transition: transform 0.3s;
            font-size: 0.8em;
            color: #667eea;
        }
        
        .article-details[open] summary::after {
            transform: translateY(-50%) rotate(-180deg);
        }
        
        .article-details summary:hover {
            background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
        }
        
        .article-content {
            padding: 20px;
        }
        
        /* Level 3: Subsection Details */
        .subsection-details {
            margin: 12px 0;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            background: #fff;
        }
        
        .subsection-details summary {
            padding: 10px 40px 10px 15px;
            cursor: pointer;
            background: #f8f9fa;
            border-radius: 5px;
            font-weight: 600;
            font-size: 1.05em;
            color: #495057;
            list-style: none;
            position: relative;
            transition: all 0.3s;
        }
        
        .subsection-details summary::-webkit-details-marker {
            display: none;
        }
        
        .subsection-details summary::after {
            content: '▼';
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            transition: transform 0.3s;
            font-size: 0.7em;
            color: #667eea;
        }
        
        .subsection-details[open] summary::after {
            transform: translateY(-50%) rotate(-180deg);
        }
        
        .subsection-details summary:hover {
            background: #e9ecef;
        }
        
        .subsection-content {
            padding: 15px;
        }
        
        /* Content Styling */
        .article-content ul, .subsection-content ul {
            margin-left: 20px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        
        .article-content li, .subsection-content li {
            margin-bottom: 5px;
        }
        
        .article-content p, .subsection-content p {
            margin-bottom: 10px;
        }
        
        .article-content h3, .subsection-content h3 {
            color: #495057;
            margin-top: 15px;
            margin-bottom: 10px;
        }
        
        /* Hidden class for search */
        .hidden {
            display: none !important;
        }
        
        .no-results {
            text-align: center;
            padding: 40px;
            color: #6c757d;
            font-size: 1.2em;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            
            .wiki-header h1 {
                font-size: 1.8em;
            }
            
            .alphabet-section > h2 {
                font-size: 2em;
            }
            
            .article-details summary {
                font-size: 1.1em;
                padding: 12px 40px 12px 15px;
            }
        }
    </style>
</head>
<body>
    <div class="wiki-container">
        <div class="wiki-header">
            <h1>📚 Personalhåndbog</h1>
            <p>Zealand's Medarbejderhåndbog - Alfabetisk Oversigt</p>
        </div>
        
        <div class="search-container">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Søg i håndbogen..." autocomplete="off">
                <span class="search-icon">🔍</span>
            </div>
        </div>
        
        <div class="main-content" id="mainContent">
'''
    
    # Generate alphabet sections
    for letter in DANISH_ALPHABET:
        if letter in grouped_articles:
            html += f'''
            <div class="alphabet-section" data-letter="{letter}">
                <h2>{letter}</h2>
'''
            
            # Generate articles for this letter
            for article in grouped_articles[letter]:
                html += f'''
                <details class="article-details">
                    <summary>{article['title']}</summary>
                    <div class="article-content">
'''
                
                # Parse subsections
                subsections = parse_content_to_subsections(article['content'])
                
                if subsections:
                    # Generate subsection details
                    for subsection in subsections:
                        html += f'''
                        <details class="subsection-details">
                            <summary>{subsection['title']}</summary>
                            <div class="subsection-content">
                                {subsection['content']}
                            </div>
                        </details>
'''
                else:
                    # No subsections, just show content
                    html += f'''
                        <div class="subsection-content">
                            {article['content']}
                        </div>
'''
                
                html += '''
                    </div>
                </details>
'''
            
            html += '''
            </div>
'''
    
    # Add JavaScript for search
    html += '''
        </div>
    </div>
    
    <script>
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const mainContent = document.getElementById('mainContent');
        const alphabetSections = document.querySelectorAll('.alphabet-section');
        
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase().trim();
            
            if (searchTerm === '') {
                // Show all sections
                alphabetSections.forEach(section => {
                    section.classList.remove('hidden');
                    const articles = section.querySelectorAll('.article-details');
                    articles.forEach(article => article.classList.remove('hidden'));
                });
                
                // Remove "no results" message if exists
                const noResults = document.querySelector('.no-results');
                if (noResults) noResults.remove();
                
                return;
            }
            
            let hasResults = false;
            
            alphabetSections.forEach(section => {
                let sectionHasResults = false;
                const articles = section.querySelectorAll('.article-details');
                
                articles.forEach(article => {
                    const articleText = article.textContent.toLowerCase();
                    
                    if (articleText.includes(searchTerm)) {
                        article.classList.remove('hidden');
                        article.setAttribute('open', ''); // Auto-open matching articles
                        sectionHasResults = true;
                        hasResults = true;
                    } else {
                        article.classList.add('hidden');
                    }
                });
                
                if (sectionHasResults) {
                    section.classList.remove('hidden');
                } else {
                    section.classList.add('hidden');
                }
            });
            
            // Show/hide "no results" message
            let noResults = document.querySelector('.no-results');
            
            if (!hasResults) {
                if (!noResults) {
                    noResults = document.createElement('div');
                    noResults.className = 'no-results';
                    noResults.innerHTML = `
                        <p>😔 Ingen resultater fundet for "<strong>${searchTerm}</strong>"</p>
                        <p style="font-size: 0.9em; margin-top: 10px;">Prøv et andet søgeord</p>
                    `;
                    mainContent.appendChild(noResults);
                }
            } else {
                if (noResults) noResults.remove();
            }
        });
    </script>
</body>
</html>
'''
    
    return html

def main():
    print("Reading knowledge base...")
    articles = read_js_knowledge_base('knowledge-base-content.js')
    print(f"Found {len(articles)} articles")
    
    print("Grouping by letter...")
    grouped = group_by_letter(articles)
    
    print(f"Found articles in {len(grouped)} letters:")
    for letter in DANISH_ALPHABET:
        if letter in grouped:
            print(f"  {letter}: {len(grouped[letter])} articles")
    
    print("Generating HTML...")
    html = generate_html(grouped)
    
    print("Writing output file...")
    with open('staff-handbook-moodle.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Done! Generated staff-handbook-moodle.html")

if __name__ == '__main__':
    main()
