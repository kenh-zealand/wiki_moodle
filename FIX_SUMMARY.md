# Fix Summary: Nested Details/Summary Structure

## Problem
Level 3 sections (marked by `<li><strong>` tags like "Den fødende", "Medforælderen") were NOT being converted to `<details>` tags. They appeared as plain text in the HTML output.

## Root Cause
The original `convert_html_to_details()` function in `generate_moodle_html.py` only detected H4 tags as subsections. It didn't recognize the `<li><strong>` pattern that represents Level 3 sections in the knowledge base content.

## Solution
Modified the `convert_html_to_details()` function to:

1. **Detect `<li><strong>` patterns** as Level 3 subsections using regex: `r'<li><strong>(.*?)</strong>'`
2. **Collect ALL content** after each `<li><strong>` section until the next `<li><strong>` or end of H3 section
3. **Generate proper nested structure**:
   - H3 tags → `<details><summary>` (Level 2)
   - `<li><strong>` tags → nested `<details><summary>` (Level 3)

## Example: Barsel Article

### Before (incorrect)
```html
<h3>Barsel</h3>
<ul>
  <li><strong>Den fødende</strong>
    <ul><li>Graviditetsorlov...</li></ul>
  </li>
</ul>
<p>Content after the strong section...</p>  <!-- NOT grouped with "Den fødende" -->
```

### After (correct)
```html
<details>
  <summary>Barsel</summary>
  <div>
    <details>
      <summary>Den fødende</summary>
      <div>
        <ul><li>Graviditetsorlov...</li></ul>
        <p>Content after the strong section...</p>  <!-- NOW properly grouped -->
        <ul><li>Barselsorlov (uge 1-10)</li></ul>
        <p>More content...</p>
      </div>
    </details>
    
    <details>
      <summary>Medforælderen</summary>
      <div>
        <ul><li>Fædreorlov...</li></ul>
        <p>Content for medforælder...</p>
      </div>
    </details>
  </div>
</details>
```

## Files Modified
- `generate_moodle_html.py` - Updated `convert_html_to_details()` function (lines 30-136)

## Testing
Verified with multiple articles:
- ✅ **Barsel** - "Den fødende", "Medforælderen", "Soloforældre", "Tvillinger, trillinger mv efter den 1. maj 2024"
- ✅ **Akut psykologisk krisehåndtering** - "Tilbud til medarbejdere", "Kontakt til psykologisk krisehjælp", "Indhold af ordningen", "Håndtering af studerende i krise/akut psykisk sygdom"
- ✅ All 40 articles generated successfully

## Result
All Level 3 sections are now properly collapsible with nested `<details>` tags. Search functionality and styling remain intact.
