import PyPDF2
import re
import json

pdf_path = r'C:\Users\franz\Desktop\Nye tekster til Personalhåndbog 05.08.2025.pdf'

# Extract all text from PDF
with open(pdf_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    full_text = ''
    for page in pdf_reader.pages:
        full_text += page.extract_text() + '\n'

# Clean up the text
full_text = re.sub(r'\n+', '\n', full_text)
full_text = re.sub(r' +', ' ', full_text)

# Split into sections based on main headers
lines = full_text.split('\n')

articles = []
current_article = None
current_content = []

for line in lines:
    line = line.strip()
    if not line or line.isdigit():
        continue
    
    # Check if this is a main header (single letter followed by title, or standalone title)
    # Examples: "A", "B", or titles like "Akut psykologisk krisehåndtering"
    if (len(line) < 100 and 
        not line.startswith('o ') and 
        not line.startswith('- ') and
        (line[0].isupper() or line[0] in ['Å', 'Ø', 'Æ']) and
        not re.match(r'^\d', line)):
        
        # Check if it's a major section header
        is_major_header = False
        
        # Single letter headers (A, B, C, etc.)
        if len(line) <= 2 and line.isalpha():
            is_major_header = True
            continue  # Skip single letter, next line will be the title
        
        # Headers that don't start with lowercase or common sub-items
        if (not any(line.lower().startswith(prefix) for prefix in ['når', 'hvis', 'ved', 'som', 'der', 'det', 'man', 'for', 'efter']) and
            ':' not in line[:50] and
            len(line) > 10):
            is_major_header = True
        
        if is_major_header:
            # Save previous article
            if current_article and current_content:
                current_article['content'] = '\n'.join(current_content)
                articles.append(current_article)
            
            # Start new article
            current_article = {
                'title': line,
                'content': []
            }
            current_content = []
            continue
    
    # Add to current content
    if current_article:
        current_content.append(line)

# Add last article
if current_article and current_content:
    current_article['content'] = '\n'.join(current_content)
    articles.append(current_article)

# Output as JSON
output = {
    'total_articles': len(articles),
    'articles': articles
}

with open('extracted_content.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(articles)} articles")
print("\nArticle titles:")
for i, article in enumerate(articles, 1):
    print(f"{i}. {article['title']}")
