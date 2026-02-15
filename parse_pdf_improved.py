import PyPDF2
import re
import json

pdf_path = r'C:\Users\franz\Desktop\Nye tekster til Personalhåndbog 05.08.2025.pdf'

# Known major section titles from the staff handbook
MAJOR_SECTIONS = [
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
    'Elever',
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
    'MUS',
    'LUS',
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
    'Udlandet',
    'Whistleblowerordning',
]

# Extract all text from PDF
with open(pdf_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    full_text = ''
    for page in pdf_reader.pages:
        full_text += page.extract_text() + '\n\n'

# Clean up the text
full_text = re.sub(r'\n{3,}', '\n\n', full_text)
full_text = re.sub(r' +', ' ', full_text)

# Split into lines
lines = [line.strip() for line in full_text.split('\n') if line.strip()]

# Find sections
articles = []
current_section = None
current_content = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Skip page numbers and single letters
    if line.isdigit() or (len(line) <= 2 and line.isalpha()):
        i += 1
        continue
    
    # Check if this line matches a major section title
    is_major_section = False
    for section in MAJOR_SECTIONS:
        # Check for exact match or match at start
        if line == section or line.startswith(section):
            is_major_section = True
            
            # Save previous section
            if current_section and current_content:
                articles.append({
                    'title': current_section,
                    'content': '\n'.join(current_content)
                })
            
            # Start new section
            current_section = section
            current_content = []
            break
    
    if not is_major_section:
        # Add to current section content
        if current_section:
            current_content.append(line)
    
    i += 1

# Add last section
if current_section and current_content:
    articles.append({
        'title': current_section,
        'content': '\n'.join(current_content)
    })

# Output as JSON
output = {
    'total_articles': len(articles),
    'articles': articles
}

with open('extracted_content_improved.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(articles)} articles")
print("\nArticle titles:")
for i, article in enumerate(articles, 1):
    content_len = len(article['content'])
    print(f"{i}. {article['title']} ({content_len} chars)")
