import json
import re
from collections import defaultdict

# Load the improved extracted content
with open('extracted_content_improved.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Category mapping
category_map = {
    'Akut psykologisk krisehåndtering': 'sikkerhed',
    'Alkohol og rusmidler': 'adfærd',
    'Ansættelse': 'ansættelse',
    'APV og MTU': 'udvikling',
    'Arbejdsmiljø': 'sikkerhed',
    'Arbejdstid': 'arbejdstid',
    'Arbejdsskader og -ulykker': 'sikkerhed',
    'Barnets første og anden sygedag': 'sygdom',
    'Barsel': 'ansættelse',
    'Bibeskæftigelse': 'adfærd',
    'Blanketter': 'it',
    'DSR': 'udvikling',
    'Elever': 'ansættelse',
    'Ferie': 'ferie',
    'Fridage': 'ferie',
    'Fratrædelse': 'ansættelse',
    'Gaver': 'adfærd',
    'God adfærd ved brug af Zealands ressourcer': 'adfærd',
    'Honorar til eksterne oplægsholdere': 'økonomi',
    'Immaterielle rettigheder': 'økonomi',
    'Jubilæum': 'udvikling',
    'Kompetencefonden': 'udvikling',
    'Kompetenceudvikling': 'udvikling',
    'Konflikthåndtering': 'adfærd',
    'Krænkende handlinger': 'adfærd',
    'Kørsel i egen bil': 'økonomi',
    'Medarbejderudviklingssamtale': 'udvikling',
    'MUS': 'udvikling',
    'LUS': 'udvikling',
    'Moodle': 'it',
    'Omsorgsdage': 'arbejdstid',
    'Opsigelsesvarsler': 'ansættelse',
    'Overvågning': 'sikkerhed',
    'Personalepolitik': 'adfærd',
    'Private relationer': 'adfærd',
    'Psykologisk rådgivning': 'sikkerhed',
    'Rejser i ind- og udland': 'økonomi',
    'Røgfri arbejdsplads': 'sikkerhed',
    'Seniorbonus': 'økonomi',
    'Skærmbriller': 'sikkerhed',
    'Stress': 'sygdom',
    'Sygdomshåndtering': 'sygdom',
    'Tavshedspligt': 'adfærd',
    'Tidsregistrering': 'arbejdstid',
    'Udlandet': 'økonomi',
    'Whistleblowerordning': 'adfærd',
}

def extract_tags(title, content):
    """Extract relevant tags from title and content"""
    tags = []
    
    # Add words from title
    title_words = re.findall(r'\b[a-zæøåA-ZÆØÅ]{4,}\b', title)
    tags.extend([w.lower() for w in title_words[:3]])
    
    # Common keywords to look for
    keywords = [
        'ferie', 'barsel', 'sygdom', 'arbejdstid', 'løn', 'ansættelse',
        'kontrakt', 'mus', 'kompetence', 'udvikling', 'sikkerhed',
        'rejse', 'kørsel', 'it', 'moodle', 'sdbf', 'leder', 'medarbejder',
        'orlov', 'fridag', 'overarbejde', 'stress', 'gave', 'alkohol',
        'tavshedspligt', 'whistleblower', 'apv', 'mtu', 'ulykke', 'hr'
    ]
    
    content_lower = content.lower()
    for keyword in keywords:
        if keyword in content_lower and keyword not in tags:
            tags.append(keyword)
    
    return tags[:8]  # Limit to 8 tags

def format_content_as_html(title, content):
    """Convert plain text content to HTML with proper structure"""
    html = f"            <h3>{title}</h3>\n"
    
    lines = content.split('\n')
    in_main_list = False
    in_sub_list = False
    paragraph_buffer = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        
        if not line:
            continue
        
        # Check if it's a main bullet point (-)
        if line.startswith('- '):
            # Close any open paragraph
            if paragraph_buffer:
                html += f"            <p>{' '.join(paragraph_buffer)}</p>\n"
                paragraph_buffer = []
            
            # Close sub-list if open
            if in_sub_list:
                html += "                </ul>\n            </li>\n"
                in_sub_list = False
            
            # Open main list if not open
            if not in_main_list:
                html += "            <ul>\n"
                in_main_list = True
            
            text = line[2:].strip()
            
            # Check if next line is a sub-item (indicates this might be a heading)
            is_heading = False
            if i < len(lines) and lines[i].strip().startswith('o '):
                is_heading = True
            
            if is_heading:
                html += f"            <li><strong>{text}</strong>\n"
            else:
                html += f"            <li>{text}</li>\n"
        
        # Check if it's a sub bullet point (o)
        elif line.startswith('o '):
            # Close any open paragraph
            if paragraph_buffer:
                html += f"            <p>{' '.join(paragraph_buffer)}</p>\n"
                paragraph_buffer = []
            
            text = line[2:].strip()
            
            # Open sub-list if not open
            if not in_sub_list:
                html += "                <ul>\n"
                in_sub_list = True
            
            html += f"                    <li>{text}</li>\n"
        
        # Regular paragraph text
        else:
            # Close any open lists
            if in_sub_list:
                html += "                </ul>\n            </li>\n"
                in_sub_list = False
            if in_main_list:
                html += "            </ul>\n"
                in_main_list = False
            
            # Accumulate paragraph text
            paragraph_buffer.append(line)
    
    # Close any remaining elements
    if paragraph_buffer:
        html += f"            <p>{' '.join(paragraph_buffer)}</p>\n"
    if in_sub_list:
        html += "                </ul>\n            </li>\n"
    if in_main_list:
        html += "            </ul>\n"
    
    return html

# Merge duplicate sections
merged_articles = defaultdict(list)
for article in data['articles']:
    title = article['title']
    content = article['content'].strip()
    
    # Skip very short content (likely incomplete)
    if len(content) < 30:
        continue
    
    merged_articles[title].append(content)

# Combine duplicates
final_articles = {}
for title, contents in merged_articles.items():
    # Join all content for this title
    combined_content = '\n\n'.join(contents)
    final_articles[title] = combined_content

# Generate JavaScript knowledge base
js_entries = []
entry_id = 1

for title, content in sorted(final_articles.items()):
    category = category_map.get(title, 'generelt')
    tags = extract_tags(title, content)
    html_content = format_content_as_html(title, content)
    
    # Escape for JavaScript
    html_content = html_content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    
    js_entry = f"""    {{
        id: {entry_id},
        title: "{title}",
        category: "{category}",
        tags: {json.dumps(tags, ensure_ascii=False)},
        content: `
{html_content}        `
    }}"""
    
    js_entries.append(js_entry)
    entry_id += 1

# Generate complete JavaScript file
js_content = f"""// Generated Knowledge Base for Personalhåndbog
// Generated from: Nye tekster til Personalhåndbog 05.08.2025.pdf
// Total entries: {len(js_entries)}
// Generation date: 2025-01-XX

const knowledgeBase = [
{',\n'.join(js_entries)}
];

// Export for use in HTML
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = knowledgeBase;
}}
"""

# Save to file
with open('knowledge-base-content.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"✓ Generated {len(js_entries)} knowledge base entries")
print("\nCategories distribution:")
categories = defaultdict(int)
for title in final_articles.keys():
    cat = category_map.get(title, 'generelt')
    categories[cat] += 1

for cat, count in sorted(categories.items()):
    print(f"  {cat:15s}: {count:2d} articles")

print("\nTop 10 largest articles:")
sorted_by_size = sorted(final_articles.items(), key=lambda x: len(x[1]), reverse=True)
for i, (title, content) in enumerate(sorted_by_size[:10], 1):
    print(f"  {i:2d}. {title[:50]:50s} ({len(content):5d} chars)")
