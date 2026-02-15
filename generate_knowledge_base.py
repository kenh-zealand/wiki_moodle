import json
import re

# Load the extracted content
with open('extracted_content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Category mapping - explicit mappings for major sections
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
    'AMO': 'sikkerhed',
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
    'Kørselsbemyndigelse': 'økonomi',
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
    'Rejser': 'økonomi',
    'Røgfri arbejdsplads': 'sikkerhed',
    'Rygeforbuddet': 'sikkerhed',
    'Seniorbonus': 'økonomi',
    'Skærmbriller': 'sikkerhed',
    'Stress': 'sygdom',
    'Sygdomshåndtering': 'sygdom',
    'Tavshedspligt': 'adfærd',
    'Tidsregistrering': 'arbejdstid',
    'Udlandet': 'økonomi',
    'Whistleblowerordning': 'adfærd',
}

def determine_category(title):
    """Determine category based on title keywords"""
    title_lower = title.lower()
    
    # Check if title matches any key
    for key, cat in category_map.items():
        if key.lower() in title_lower:
            return cat
    
    # Keyword-based fallback
    if any(word in title_lower for word in ['ansættelse', 'onboarding', 'kontrakt', 'rekruttering', 'adjunkt']):
        return 'ansættelse'
    elif any(word in title_lower for word in ['arbejdstid', 'fleks', 'overarbejde', 'timer', 'merarbejde']):
        return 'arbejdstid'
    elif any(word in title_lower for word in ['ferie', 'fridag', 'helligdag']):
        return 'ferie'
    elif any(word in title_lower for word in ['syg', 'sygdom', 'stress', 'barn']):
        return 'sygdom'
    elif any(word in title_lower for word in ['it', 'moodle', 'blanket', 'sdbf', 'system']):
        return 'it'
    elif any(word in title_lower for word in ['adfærd', 'alkohol', 'gave', 'privat', 'tavshed', 'whistleblower']):
        return 'adfærd'
    elif any(word in title_lower for word in ['udvikling', 'kompetence', 'mus', 'lus', 'apv', 'mtu']):
        return 'udvikling'
    elif any(word in title_lower for word in ['rejse', 'kørsel', 'økonomi', 'udgift', 'honorar', 'senior']):
        return 'økonomi'
    elif any(word in title_lower for word in ['sikkerhed', 'ulykke', 'arbejdsmiljø', 'krise', 'overvågning']):
        return 'sikkerhed'
    else:
        return 'generelt'

def extract_tags(title, content):
    """Extract relevant tags from title and content"""
    tags = []
    
    # Add words from title
    title_words = re.findall(r'\b[a-zæøåA-ZÆØÅ]{4,}\b', title)
    tags.extend([w.lower() for w in title_words[:3]])
    
    # Common keywords
    keywords = [
        'ferie', 'barsel', 'sygdom', 'arbejdstid', 'løn', 'ansættelse',
        'kontrakt', 'mus', 'kompetence', 'udvikling', 'sikkerhed',
        'rejse', 'kørsel', 'it', 'moodle', 'sdbf', 'leder', 'medarbejder',
        'orlov', 'fridag', 'overarbejde', 'stress', 'gave', 'alkohol',
        'tavshedspligt', 'whistleblower', 'apv', 'mtu', 'ulykke'
    ]
    
    content_lower = content.lower()
    for keyword in keywords:
        if keyword in content_lower and keyword not in tags:
            tags.append(keyword)
    
    return tags[:8]  # Limit to 8 tags

def format_content_as_html(title, content):
    """Convert plain text content to HTML with proper structure"""
    html = f"<h3>{title}</h3>\n"
    
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
                html += f"<p>{' '.join(paragraph_buffer)}</p>\n"
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
            
            # Check if this is a section heading (short line that acts as a header)
            if len(text) < 80 and not text.endswith('.') and not text.endswith(','):
                # This might be a heading - check if next line is 'o'
                if i < len(lines) and lines[i].strip().startswith('o '):
                    html += f"            <li><strong>{text}</strong>\n"
                else:
                    html += f"            <li>{text}</li>\n"
            else:
                html += f"            <li>{text}</li>\n"
        
        # Check if it's a sub bullet point (o)
        elif line.startswith('o '):
            # Close any open paragraph
            if paragraph_buffer:
                html += f"<p>{' '.join(paragraph_buffer)}</p>\n"
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

# Major section titles we know should be standalone
major_sections = [
    'Akut psykologisk krisehåndtering',
    'Alkohol og rusmidler',
    'Ansættelse',
    'APV og MTU',
    'Arbejdsmiljø',
    'Arbejdstid',
    'Arbejdsskader og -ulykker',
    'Barnets første og anden sygedag',
    'Barsel',
    'Bibeskæftigelse',
    'Blanketter',
    'DSR',
    'Ferie',
    'Fridage',
    'Fratrædelse',
    'Gaver',
    'God adfærd ved brug af Zealands ressourcer',
    'Honorar til eksterne oplægsholdere',
    'Immaterielle rettigheder',
    'Jubilæum',
    'Kompetencefonden',
    'Kompetenceudvikling',
    'Konflikthåndtering',
    'Krænkende handlinger',
    'Kørsel i egen bil',
    'Medarbejderudviklingssamtale',
    'Moodle',
    'Omsorgsdage',
    'Opsigelsesvarsler',
    'Overvågning',
    'Personalepolitik',
    'Private relationer',
    'Psykologisk rådgivning',
    'Rejser i ind- og udland',
    'Røgfri arbejdsplads',
    'Seniorbonus',
    'Skærmbriller',
    'Stress',
    'Sygdomshåndtering',
    'Tavshedspligt',
    'Tidsregistrering',
    'Whistleblowerordning',
]

def is_major_section(title):
    """Check if title is a major section"""
    return title in major_sections or any(title.startswith(s) for s in major_sections)

# Merge related articles
merged_articles = {}
skip_indices = set()

# First pass: identify major sections and their content
current_major_section = None
current_content = []

for i, article in enumerate(data['articles']):
    title = article['title']
    content = article['content']
    
    # Check if this is a major section
    if is_major_section(title) and len(title) > 10:
        # Save previous section if exists
        if current_major_section and current_content:
            merged_articles[current_major_section] = '\n'.join(current_content)
        
        # Start new section
        current_major_section = title
        current_content = [content]
    
    # Otherwise, append to current section or skip if no section started
    elif current_major_section:
        # This is continuation of current section
        current_content.append(content)
    else:
        # Standalone small section or continuation without major section
        # Try to use as standalone if meaningful
        if len(title) > 15 and len(content) > 100:
            merged_articles[title] = content

# Save last section
if current_major_section and current_content:
    merged_articles[current_major_section] = '\n'.join(current_content)

# Generate JavaScript knowledge base
js_entries = []
entry_id = 1

for title, content in merged_articles.items():
    if len(content.strip()) < 50:  # Skip very short content
        continue
    
    category = determine_category(title)
    tags = extract_tags(title, content)
    html_content = format_content_as_html(title, content)
    
    # Escape for JavaScript
    html_content = html_content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    
    js_entry = f"""    {{
        id: {entry_id},
        title: "{title}",
        category: "{category}",
        tags: {json.dumps(tags)},
        content: `
{html_content}        `
    }}"""
    
    js_entries.append(js_entry)
    entry_id += 1

# Generate complete JavaScript file
js_content = f"""// Generated Knowledge Base for Personalhåndbog
// Generated from: Nye tekster til Personalhåndbog 05.08.2025.pdf
// Total entries: {len(js_entries)}

const knowledgeBase = [
{','.join(js_entries)}
];

// Export for use in HTML
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = knowledgeBase;
}}
"""

# Save to file
with open('knowledge-base-content.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Generated {len(js_entries)} knowledge base entries")
print("\nCategories distribution:")
categories = {}
for entry in merged_articles.keys():
    cat = determine_category(entry)
    categories[cat] = categories.get(cat, 0) + 1

for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count}")
