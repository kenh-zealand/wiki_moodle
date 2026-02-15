import re
import json

# Read the knowledge base JavaScript file
with open('knowledge-base-content.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Parse entries manually
knowledge_base = []
entry_pattern = r'\{[^}]*?id:\s*(\d+),\s*title:\s*"([^"]*)",\s*category:\s*"([^"]*)",\s*tags:\s*\[(.*?)\],\s*content:\s*`(.*?)`\s*\}'

for match in re.finditer(entry_pattern, js_content, re.DOTALL):
    entry_id = int(match.group(1))
    title = match.group(2)
    category = match.group(3)
    tags_str = match.group(4)
    content = match.group(5)
    
    # Parse tags
    tags = [t.strip().strip('"') for t in tags_str.split(',')]
    
    knowledge_base.append({
        'id': entry_id,
        'title': title,
        'category': category,
        'tags': tags,
        'content': content
    })

def convert_html_to_details(html_content):
    """Convert H3 sections and <li><strong> patterns to details/summary structure"""
    from html.parser import HTMLParser
    
    class ContentParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.sections = []
            self.current_section = None
            self.current_subsection = None
            self.in_strong_li = False
            self.strong_text = ''
            self.tag_stack = []
            self.buffer = []
            
        def handle_starttag(self, tag, attrs):
            self.tag_stack.append(tag)
            
            if tag == 'h3':
                # Save previous section
                if self.current_section:
                    self.sections.append(self.current_section)
                self.current_section = {'title': '', 'content': [], 'subsections': []}
            elif tag == 'strong' and len(self.tag_stack) >= 2 and self.tag_stack[-2] == 'li':
                # This is a <li><strong> pattern - potential subsection
                self.in_strong_li = True
                self.strong_text = ''
            else:
                # Add to buffer
                attrs_str = ' '.join([f'{k}="{v}"' for k, v in attrs]) if attrs else ''
                self.buffer.append(f'<{tag} {attrs_str}>' if attrs_str else f'<{tag}>')
        
        def handle_endtag(self, tag):
            if self.tag_stack and self.tag_stack[-1] == tag:
                self.tag_stack.pop()
            
            if tag == 'strong' and self.in_strong_li:
                # End of strong tag in li - check if we should create subsection
                self.in_strong_li = False
                # Save any pending subsection
                if self.current_subsection:
                    if self.current_section:
                        self.current_section['subsections'].append(self.current_subsection)
                # Start new subsection
                self.current_subsection = {'title': self.strong_text.strip(), 'content': []}
            else:
                self.buffer.append(f'</{tag}>')
        
        def handle_data(self, data):
            if self.in_strong_li:
                self.strong_text += data
            elif not self.current_section:
                # Before any h3, ignore
                pass
            elif self.current_section and 'title' in self.current_section and not self.current_section['title']:
                # This is h3 title text
                self.current_section['title'] = data.strip()
            else:
                self.buffer.append(data)
        
        def flush_buffer(self):
            """Flush buffer to current subsection or section"""
            if not self.buffer:
                return
            content = ''.join(self.buffer).strip()
            if content:
                if self.current_subsection:
                    self.current_subsection['content'].append(content)
                elif self.current_section:
                    self.current_section['content'].append(content)
            self.buffer = []
        
        def get_sections(self):
            self.flush_buffer()
            if self.current_subsection and self.current_section:
                self.current_section['subsections'].append(self.current_subsection)
            if self.current_section:
                self.sections.append(self.current_section)
            return self.sections
    
    # Use BeautifulSoup-like approach for better parsing
    from html.parser import HTMLParser
    
    # Actually, let's use a simpler regex-based approach that's more reliable
    lines = html_content.strip().split('\n')
    sections = []
    current_section = None
    current_subsection = None
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for H3 heading
        h3_match = re.match(r'<h3>(.*?)</h3>', line)
        if h3_match:
            # Save previous section
            if current_subsection and current_section:
                current_section['subsections'].append(current_subsection)
                current_subsection = None
            if current_section:
                sections.append(current_section)
            # Start new section
            current_section = {'title': h3_match.group(1), 'content': [], 'subsections': []}
            i += 1
            continue
        
        # Check for <li><strong> pattern (Level 3 subsection)
        strong_match = re.search(r'<li><strong>(.*?)</strong>', line)
        if strong_match and current_section:
            # Save previous subsection
            if current_subsection:
                current_section['subsections'].append(current_subsection)
            # Start new subsection
            subsection_title = strong_match.group(1)
            current_subsection = {'title': subsection_title, 'content': []}
            i += 1
            continue
        
        # Add content to appropriate place
        if line:
            if current_subsection:
                current_subsection['content'].append(line)
            elif current_section:
                current_section['content'].append(line)
        
        i += 1
    
    # Save last subsection and section
    if current_subsection and current_section:
        current_section['subsections'].append(current_subsection)
    if current_section:
        sections.append(current_section)
    
    # Generate details/summary HTML
    output = []
    for section in sections:
        if section['title']:
            output.append('<details>')
            output.append(f'    <summary>{section["title"]}</summary>')
            output.append('    <div class="details-content">')
            
            # Add main content (before any subsections)
            for content_line in section['content']:
                output.append(f'        {content_line}')
            
            # Add subsections
            for subsection in section['subsections']:
                output.append('        <details>')
                output.append(f'            <summary>{subsection["title"]}</summary>')
                output.append('            <div class="details-content">')
                for sub_content in subsection['content']:
                    output.append(f'                {sub_content}')
                output.append('            </div>')
                output.append('        </details>')
            
            output.append('    </div>')
            output.append('</details>')
    
    return '\n'.join(output)

# Generate the HTML file
html_template = '''<!DOCTYPE html>
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
        
        .article {
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 1px solid #e9ecef;
        }
        
        .article:last-child {
            border-bottom: none;
        }
        
        .article h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.8em;
        }
        
        /* Details/Summary styling */
        details {
            margin: 15px 0;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            background: #fff;
        }
        
        details summary {
            padding: 12px 45px 12px 15px;
            cursor: pointer;
            background: #f8f9fa;
            border-radius: 6px;
            font-weight: 600;
            color: #495057;
            list-style: none;
            position: relative;
            transition: all 0.3s;
        }
        
        details summary::-webkit-details-marker {
            display: none;
        }
        
        details summary::after {
            content: '▼';
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            transition: transform 0.3s;
            font-size: 0.8em;
            color: #667eea;
        }
        
        details[open] summary::after {
            transform: translateY(-50%) rotate(-180deg);
        }
        
        details summary:hover {
            background: #e9ecef;
            border-color: #667eea;
        }
        
        .details-content {
            padding: 15px;
        }
        
        /* Nested details (level 2) */
        details details {
            margin: 10px 0 10px 15px;
            border-left: 3px solid #764ba2;
        }
        
        details details summary {
            background: #ffffff;
            font-size: 1em;
            padding: 10px 40px 10px 20px;
        }
        
        .article p {
            margin-bottom: 15px;
            text-align: justify;
        }
        
        .article ul, .article ol {
            margin: 15px 0 15px 30px;
        }
        
        .article li {
            margin-bottom: 8px;
        }
        
        .article strong {
            color: #495057;
        }
        
        .tag {
            display: inline-block;
            background: #e7f1ff;
            color: #004085;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            margin-right: 5px;
            margin-top: 10px;
        }
        
        .highlight {
            background-color: #fff3cd;
            padding: 2px 4px;
            border-radius: 2px;
        }
        
        .no-results {
            text-align: center;
            padding: 60px 20px;
            color: #6c757d;
            font-size: 1.2em;
        }
        
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            
            .wiki-header h1 {
                font-size: 1.8em;
            }
            
            .main-content {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="wiki-container">
        <div class="wiki-header">
            <h1>📚 Personalhåndbog</h1>
            <p>Søgbar videnbase for Zealand medarbejdere</p>
        </div>
        
        <div class="search-container">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Søg i håndbogen..." />
                <span class="search-icon">🔍</span>
            </div>
        </div>
        
        <div class="main-content">
            <div id="articlesContainer">
'''

# Add all articles
for entry in knowledge_base:
    article_html = f'''
                <div class="article" data-id="{entry['id']}" data-title="{entry['title']}" data-tags="{' '.join(entry['tags'])}" data-category="{entry['category']}">
                    <h2>{entry['title']}</h2>
'''
    
    # Convert content to details/summary
    converted_content = convert_html_to_details(entry['content'])
    article_html += '                    ' + converted_content.replace('\n', '\n                    ')
    
    # Add tags
    article_html += '\n                    <div class="tags">\n'
    for tag in entry['tags']:
        article_html += f'                        <span class="tag">{tag}</span>\n'
    article_html += '                    </div>\n'
    article_html += '                </div>\n'
    
    html_template += article_html

# Add closing tags and search script
html_template += '''
                <div class="no-results" id="noResults" style="display: none;">
                    <h3>Ingen resultater fundet</h3>
                    <p>Prøv at søge med andre ord</p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Simple search functionality
        const searchInput = document.getElementById('searchInput');
        const articles = document.querySelectorAll('.article');
        const noResults = document.getElementById('noResults');
        
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase().trim();
            let visibleCount = 0;
            
            articles.forEach(article => {
                const title = article.dataset.title.toLowerCase();
                const tags = article.dataset.tags.toLowerCase();
                const category = article.dataset.category.toLowerCase();
                const content = article.textContent.toLowerCase();
                
                if (searchTerm === '' || 
                    title.includes(searchTerm) || 
                    tags.includes(searchTerm) || 
                    category.includes(searchTerm) ||
                    content.includes(searchTerm)) {
                    article.style.display = 'block';
                    visibleCount++;
                } else {
                    article.style.display = 'none';
                }
            });
            
            noResults.style.display = visibleCount === 0 ? 'block' : 'none';
        });
    </script>
</body>
</html>
'''

# Write the file
with open('staff-handbook-moodle.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("✅ Moodle-compatible HTML file created successfully!")
print(f"📄 Generated {len(knowledge_base)} articles")
print("📍 Location: staff-handbook-moodle.html")
