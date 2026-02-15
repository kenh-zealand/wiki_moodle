# Moodle Wiki - Structure Quick Reference

## 3-Level Hierarchical Structure

### Visual Representation

```
📖 Personalhåndbog
├── 🔍 Search Bar (filters all levels)
│
├── 📑 A (Level 1 - Static Header)
│   ├── 📄 Ansættelse (Level 2 - Collapsible Article)
│   │   ├── 📌 Opslag af stillinger (Level 3 - Collapsible Subsection)
│   │   ├── 📌 Lønforhandling (Level 3 - Collapsible Subsection)
│   │   ├── 📌 Ansættelseskontrakt og lønaftale (Level 3)
│   │   ├── 📌 Oprettelse af IT-adgange (Level 3)
│   │   └── 📌 Introduktion af nye medarbejdere (Level 3)
│   │
│   ├── 📄 APV og MTU (Level 2 - Collapsible Article)
│   │   └── 📌 APV og MTU (Level 3 - Collapsible Subsection)
│   │
│   ├── 📄 Akut psykologisk krisehåndtering (Level 2)
│   │   ├── 📌 Tilbud til medarbejdere (Level 3)
│   │   ├── 📌 Kontakt til psykologisk krisehjælp (Level 3)
│   │   ├── 📌 Indhold af ordningen (Level 3)
│   │   └── 📌 Håndtering af studerende i krise (Level 3)
│   │
│   └── ... (more A articles)
│
├── 📑 B (Level 1 - Static Header)
│   ├── 📄 Barnets første og anden sygedag (Level 2)
│   │   ├── 📌 Ved barns sygdom... (Level 3)
│   │   └── 📌 Hvad skal dokumenteres... (Level 3)
│   │
│   ├── 📄 Barsel (Level 2)
│   │   ├── 📌 Den fødende (Level 3)
│   │   ├── 📌 Medforælderen (Level 3)
│   │   ├── 📌 Soloforældre (Level 3)
│   │   └── 📌 Tvillinger, trillinger mv (Level 3)
│   │
│   ├── 📄 Bibeskæftigelse (Level 2)
│   │   └── 📌 Bibeskæftigelse (Level 3)
│   │
│   └── 📄 Bliv hjemme, hvis du er syg (Level 2)
│       └── 📌 Content (Level 3)
│
├── 📑 C (Level 1 - would be here if C articles existed)
│
├── 📑 D (Level 1 - Static Header)
│   └── 📄 Datahåndtering (Level 2)
│       └── ... (subsections)
│
└── ... (continues through alphabet)
```

## HTML Structure Details

### Level 1: Alphabet Section
```html
<div class="alphabet-section" data-letter="A">
  <h2>A</h2>
  <!-- Articles go here -->
</div>
```
- **Not collapsible**
- Large header with colored underline
- Acts as visual separator and navigation point

### Level 2: Article
```html
<details class="article-details">
  <summary>Article Title</summary>
  <div class="article-content">
    <!-- Subsections go here -->
  </div>
</details>
```
- **Collapsible** with `<details>` element
- Closed by default
- Opens when clicked or when matching search
- Gradient background for prominence

### Level 3: Subsection
```html
<details class="subsection-details">
  <summary>Subsection Title</summary>
  <div class="subsection-content">
    <!-- Content here -->
  </div>
</details>
```
- **Nested collapsible** within articles
- Closed by default
- Lighter styling than Level 2
- Contains the actual content

## Key Features

### 🎯 All Closed by Default
- Clean initial view
- User expands what they need
- Reduces information overload

### 🔍 Smart Search
- Filters all three levels
- Auto-opens matching articles
- Hides non-matching sections
- Shows "no results" feedback

### 📱 Responsive Design
- Works on desktop and mobile
- Touch-friendly collapse/expand
- Readable on all screen sizes

### 🎨 Visual Hierarchy
- **Level 1**: Large, bold, colored border
- **Level 2**: Gradient background, larger font
- **Level 3**: Simple background, standard font
- Clear visual distinction between levels

## Statistics

- **Total Articles**: 40
- **Alphabet Letters**: 17 (A, B, D, E, F, G, H, I, J, K, L, M, O, P, S, T, U, W)
- **Total Subsections**: 108
- **File Size**: ~75 KB

## Benefits vs Old Structure

| Old Structure | New Structure |
|---------------|---------------|
| Category-based | Alphabetical |
| Flat hierarchy | 3-level hierarchy |
| Category sidebar | Clean single view |
| H2 articles | Details/summary |
| Mixed collapsible | Consistent nested |
| Hard to scan | Easy alphabetical scan |

## Usage Tips

1. **Find by letter**: Scroll to the letter section
2. **Expand article**: Click article title to see subsections
3. **Expand subsection**: Click subsection to see content
4. **Search**: Type keyword to filter everything
5. **Collapse all**: Refresh page to reset

---

**Structure Type**: Alphabetical 3-Level Hierarchy  
**All Sections**: Closed by Default  
**Search**: Enabled with Auto-Expand  
**Mobile**: Fully Responsive
