# H5P Staff Handbook - Deployment Guide

## 📦 Hvad er H5P?

H5P er en open-source framework til interaktivt indhold der er indbygget i Moodle. Ved at bruge H5P får du:

- ✅ **Ingen CSS filtering problemer** - Alt virker i Moodle
- ✅ **Native integration** - Ser ud som en del af Moodle
- ✅ **Bedre ydeevne** - Optimeret til Moodle
- ✅ **Tracking & Analytics** - Kan spore brugeradfærd
- ✅ **Responsive** - Virker perfekt på mobil

## 🚀 Installation i Moodle

### Trin 1: Upload H5P bibliotek (Første gang kun)

1. Log ind som Moodle administrator
2. Gå til **Site administration** → **Plugins** → **Install plugins**
3. Upload `H5P.StaffHandbook-1.0` som ZIP fil
4. Klik **Install plugin from the ZIP file**
5. Følg installations-wizarden

**ALTERNATIVT:** Udpak `H5P.StaffHandbook-1.0` manuelt til:
```
moodle/mod/hvp/library/H5P.StaffHandbook-1.0/
```

### Trin 2: Upload H5P indhold

1. Gå til dit Moodle kursus
2. Klik **Turn editing on**
3. Klik **Add an activity or resource**
4. Vælg **Interactive Content (H5P)**
5. Upload `StaffHandbook.h5p` filen
6. Klik **Upload**
7. Give aktiviteten et navn (fx "Personalhåndbog")
8. Klik **Save and display**

## 📋 Fil Oversigt

Projektet indeholder følgende filer:

### H5P Library (H5P.StaffHandbook-1.0/)
```
H5P.StaffHandbook-1.0/
├── library.json            # H5P bibliotek metadata
├── semantics.json          # Content type definition
├── js/
│   └── staffhandbook.js    # JavaScript logic (søgning, rendering)
├── css/
│   └── staffhandbook.css   # Alle styles
└── language/
    └── da.json             # Danske oversættelser
```

### H5P Content Package (StaffHandbook.h5p)
```
StaffHandbook.h5p (ZIP fil med):
├── h5p.json                # Package metadata
├── content/
│   └── content.json        # Alt indhold (40 artikler, 108 subsektioner)
└── H5P.StaffHandbook-1.0/  # Bibliotek (inkluderet i package)
```

## 🔧 Opdatering af Indhold

Hvis du skal opdatere indholdet senere:

### Metode 1: Direkte i Moodle (Simpel)
1. Åbn H5P aktiviteten i Moodle
2. Klik **Edit**
3. Rediger indhold direkte i H5P editoren
4. Gem ændringer

### Metode 2: Regenerer H5P fil (Fuld kontrol)

1. Rediger `staff-handbook-moodle.html` (tilføj/fjern artikler)
2. Kør konvertering:
   ```powershell
   python generate_h5p_content.py
   ```
3. Generer ny H5P package:
   ```powershell
   .\create_h5p_package.ps1
   ```
4. Upload ny `StaffHandbook.h5p` til Moodle (erstatter gammel)

## 🎯 Features

### Søgning
- Live søgning mens du skriver
- Automatisk åbning af matches
- "Ingen resultater" besked

### 3-Niveau Hierarki
- **Niveau 1:** Alfabetiske bogstaver (A-W) - IKKE collapsible
- **Niveau 2:** Artikler (fx "Barsel") - Collapsible
- **Niveau 3:** Subsektioner (fx "Den fødende") - Nested collapsible med indryk

### Visual Design
- Gradient header (lilla/blå)
- Blå venstre kant på subsektioner
- 30px indryk på subsektioner
- Responsive design for mobil

## 🧪 Test Checklist

Efter upload til Moodle, test følgende:

- [ ] H5P content loader uden fejl
- [ ] Søgning virker (prøv "barsel", "sygdom")
- [ ] Alle artikler kan foldes ud/ind
- [ ] Subsektioner har synlig indryk
- [ ] Mobil responsivt design
- [ ] Ingen JavaScript errors i console
- [ ] Indhold ser korrekt ud (40 artikler, 17 bogstaver)

## 📱 Browser Kompatibilitet

H5P Staff Handbook virker i:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari, Chrome Android)

## 🔍 Troubleshooting

### H5P vises ikke
- Check at H5P plugin er aktiveret i Moodle
- Verificer at biblioteket er installeret korrekt
- Check Moodle logs for fejl

### Collapsibles virker ikke
- H5P bruger HTML5 `<details>` tags - sikr dig at browser understøtter det
- Check browser console for JavaScript errors

### Content loader ikke
- Verificer `content.json` er valid JSON
- Check at file size ikke er for stor (>2MB kan være et problem)

### Styling ser forkert ud
- H5P kan have sin egen CSS der konflikter
- Prøv at tilføje `!important` til kritiske CSS rules

## 📞 Support

Ved problemer:
1. Check Moodle administrator logs
2. Verify alle filer er uploadet korrekt
3. Test i forskellige browsers
4. Check H5P documentation: https://h5p.org/documentation

## 🎉 Resultat

Efter korrekt installation har du:
- 📚 40 artikler fra personalhåndbog
- 🔤 17 alfabetiske sektioner (A-W)
- 📝 108 subsektioner
- 🔍 Real-time søgning
- 📱 Mobil responsive
- ✨ Ingen Moodle CSS filtering problemer!
