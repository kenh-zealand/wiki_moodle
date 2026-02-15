# H5P Staff Handbook - Implementation Plan

## Objective
Convert the searchable, alphabetical staff handbook wiki into a custom H5P content type that preserves all features:
- 3-level hierarchy (A-Å, Articles, Subsections)
- Search functionality
- Collapsible sections (HTML5 details)
- Alphabetical organization

## H5P Structure Overview

A custom H5P content type consists of:
1. **library.json** - Metadata and dependencies
2. **semantics.json** - Content structure/fields
3. **presave.js** - Data processing
4. **js/staffhandbook.js** - Main JavaScript logic
5. **css/staffhandbook.css** - Styles
6. **content/content.json** - Actual content data

## Implementation Steps

### Phase 1: H5P Content Type Setup
- [ ] Create H5P library folder structure (H5P.StaffHandbook-1.0)
- [ ] Write library.json with metadata
- [ ] Write semantics.json defining content fields
- [ ] Extract CSS from staff-handbook-moodle.html
- [ ] Extract JavaScript from staff-handbook-moodle.html

### Phase 2: Content Conversion
- [ ] Parse knowledge-base-content.js into H5P content.json format
- [ ] Structure: alphabet letters → articles → subsections
- [ ] Preserve all HTML content and hierarchy
- [ ] Generate content.json with full data structure

### Phase 3: H5P Package Creation
- [ ] Create h5p.json with content metadata
- [ ] Package all files into .h5p ZIP file
- [ ] Test upload to Moodle
- [ ] Verify all functionality works

### Phase 4: Testing & Documentation
- [ ] Test search functionality
- [ ] Test collapsible sections at all levels
- [ ] Test mobile responsiveness
- [ ] Write deployment guide for H5P

## File Structure
```
H5P.StaffHandbook-1.0/
├── library.json
├── semantics.json
├── presave.js
├── js/
│   └── staffhandbook.js
├── css/
│   └── staffhandbook.css
└── language/
    └── da.json

StaffHandbook.h5p (ZIP containing):
├── h5p.json
├── content/
│   └── content.json
└── H5P.StaffHandbook-1.0/ (library folder)
```

## Technical Considerations

**Advantages of H5P:**
- Native Moodle integration
- No CSS filtering issues
- Better tracking/analytics
- Responsive by default
- Can be embedded anywhere

**Challenges:**
- Initial setup complexity
- Need to test H5P development locally first
- May need H5P CLI tools for packaging
- Moodle admin may need to enable custom content types

## Next Steps
1. Set up H5P library folder structure
2. Convert existing HTML/CSS/JS to H5P format
3. Create content.json with all 40 articles
4. Package as .h5p file
5. Test in Moodle
