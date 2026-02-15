# Staff Handbook Wiki - Knowledge Base Generation

This project extracts content from the Danish staff handbook PDF and generates a structured JavaScript knowledge base for the interactive wiki HTML page.

## Files

### Input
- **PDF Source**: `C:\Users\franz\Desktop\Nye tekster til Personalhåndbog 05.08.2025.pdf`
  - Danish staff handbook (Personalhåndbog) with various HR policies and procedures

### Processing Scripts
- **parse_pdf_improved.py**: Improved PDF parser that identifies 48 major sections
- **generate_final_kb.py**: Generates the final JavaScript knowledge base with proper formatting

### Output
- **knowledge-base-content.js**: Complete JavaScript array with 40 structured entries
  - Ready to use in `staff-handbook-wiki.html`
  - Total size: ~104 KB
  - All content in Danish

### Supporting Files
- **extracted_content_improved.json**: Intermediate JSON with parsed sections
- **staff-handbook-wiki.html**: HTML wiki page that uses the knowledge base

## Knowledge Base Structure

Each entry in the knowledge base has:

```javascript
{
    id: <number>,              // Unique identifier
    title: "<string>",         // Section title (Danish)
    category: "<string>",      // Category for filtering
    tags: [<strings>],         // Search tags
    content: `<HTML>`          // Formatted HTML content
}
```

## Categories

The 40 articles are distributed across 9 categories:

- **adfærd** (9 articles): Behavior policies
  - Alkohol og rusmidler, Gaver, Konflikthåndtering, Krænkende handlinger, 
    Personalepolitik, Private relationer, Tavshedspligt, Whistleblowerordning

- **ansættelse** (5 articles): Employment
  - Ansættelse, Barsel, Elever, Fratrædelse, Opsigelsesvarsler

- **arbejdstid** (3 articles): Working hours
  - Arbejdstid, Omsorgsdage, Tidsregistrering

- **ferie** (2 articles): Vacation
  - Ferie, Fridage

- **it** (2 articles): IT systems
  - Blanketter, Moodle

- **sikkerhed** (6 articles): Safety
  - Akut psykologisk krisehåndtering, Arbejdsmiljø, Arbejdsskader og -ulykker,
    Overvågning, Psykologisk rådgivning, Skærmbriller

- **sygdom** (3 articles): Illness
  - Barnets første og anden sygedag, Stress, Sygdomshåndtering

- **udvikling** (5 articles): Development
  - APV og MTU, DSR, Jubilæum, Kompetencefonden, Kompetenceudvikling,
    Medarbejderudviklingssamtale

- **økonomi** (5 articles): Finance
  - Honorar til eksterne oplægsholdere, Immaterielle rettigheder, 
    Kørsel i egen bil, Seniorbonus, Udlandet

## Major Sections Extracted

Top 10 largest sections by content:

1. **Whistleblowerordning** (10,730 chars)
2. **Barsel** (7,029 chars)
3. **Ferie** (6,073 chars)
4. **God adfærd ved brug af Zealands ressourcer** (4,460 chars)
5. **Psykologisk rådgivning** (4,237 chars)
6. **Kørsel i egen bil** (4,029 chars)
7. **Ansættelse** (2,718 chars)
8. **Stress** (2,617 chars)
9. **Alkohol og rusmidler** (1,967 chars)
10. **Overvågning** (1,961 chars)

## Content Formatting

Content is formatted as HTML with:
- **`<h3>`** tags for section titles
- **`<ul>` and `<li>`** for bullet lists
- **`<strong>`** for sub-section headings
- **`<p>`** for paragraphs
- Proper nesting of main lists and sub-lists

## Usage

To use the knowledge base in your HTML wiki:

```javascript
// Option 1: Direct inclusion
<script src="knowledge-base-content.js"></script>

// Option 2: Copy the knowledgeBase array
// Open knowledge-base-content.js and copy the const knowledgeBase = [...] 
// into your staff-handbook-wiki.html file
```

The wiki page includes:
- Search functionality across all content
- Category filtering
- Tag-based navigation
- Responsive design
- Danish language interface

## How to Regenerate

If you need to update the knowledge base from a new PDF version:

1. Update the PDF path in `parse_pdf_improved.py`
2. Run the parser:
   ```bash
   python parse_pdf_improved.py
   ```
3. Generate the knowledge base:
   ```bash
   python generate_final_kb.py
   ```
4. The updated `knowledge-base-content.js` is ready to use

## Technical Notes

- All text is UTF-8 encoded
- Danish characters (æ, ø, å) are properly preserved
- Content structure preserves hierarchical relationships
- Duplicate sections are automatically merged
- Empty or very short sections are filtered out

## Dependencies

- Python 3.x
- PyPDF2 library

Install dependencies:
```bash
pip install PyPDF2
```

---

Generated: January 2025
