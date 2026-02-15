# Guide: Indsæt Personalhåndbog Wiki i Moodle

## 📋 Metode 1: Page Aktivitet (Anbefalet)

### Trin 1: Åbn HTML-filen
1. Åbn `staff-handbook-wiki.html` i en teksteditor (Notepad, VS Code, etc.)
2. Tryk **Ctrl+A** for at markere alt
3. Tryk **Ctrl+C** for at kopiere

### Trin 2: Opret Page i Moodle
1. Log ind på Moodle
2. Gå til dit kursus
3. Klik **"Slå redigering til"** / **"Turn editing on"**
4. Klik **"Tilføj en aktivitet eller ressource"** / **"Add an activity or resource"**
5. Vælg **"Page"** / **"Side"**
6. Klik **"Tilføj"** / **"Add"**

### Trin 3: Konfigurer Page
1. **Navn**: "Personalhåndbog - Searchable Wiki" (eller dit ønskede navn)
2. **Beskrivelse**: Valgfrit - beskrivelse af indholdet
3. Scroll ned til **"Sideindhold"** / **"Page content"**

### Trin 4: Indsæt HTML
1. I editoren, find og klik på **"< >"** knappen (HTML source editor)
   - Normalt i værktøjslinjen øverst
   - Kan også hedde "HTML" eller "Vis HTML"
2. En ny dialogboks åbnes med HTML-kode
3. **Slet alt** eksisterende indhold (hvis der er noget)
4. Tryk **Ctrl+V** for at indsætte din HTML
5. Klik **"Gem"** / **"Save"** eller **"Update"** i dialogen

### Trin 5: Gem og Test
1. Scroll ned og klik **"Gem og vis"** / **"Save and display"**
2. Wiki'en skulle nu være synlig med fuld funktionalitet
3. Test:
   - Søgning virker
   - Kategorier kan filtreres
   - Collapsible sektioner kan foldes ud/sammen
   - "Udfold alt" knap fungerer

---

## 📋 Metode 2: Label Aktivitet (Kompakt)

### Trin 1: Opret Label
1. Gå til dit kursus i Moodle
2. Klik **"Slå redigering til"**
3. Klik **"Tilføj en aktivitet eller ressource"**
4. Vælg **"Label"** / **"Etiket"**
5. Klik **"Tilføj"**

### Trin 2: Indsæt HTML
1. Åbn `staff-handbook-wiki.html` i teksteditor
2. Kopier alt indhold (Ctrl+A, Ctrl+C)
3. Tilbage i Moodle, klik **"< >"** knappen (HTML editor)
4. Indsæt HTML-koden (Ctrl+V)
5. Klik **"Gem"** / **"Save"**

### Trin 3: Gem
1. Klik **"Gem og vend tilbage til kursus"** / **"Save and return to course"**
2. Wiki'en vises nu direkte på kursets forside

---

## 📋 Metode 3: File Resource (Download)

Hvis JavaScript ikke virker i Moodle:

### Trin 1: Upload fil
1. Gå til dit kursus
2. Klik **"Slå redigering til"**
3. Klik **"Tilføj en aktivitet eller ressource"**
4. Vælg **"File"** / **"Fil"**
5. Upload `staff-handbook-wiki.html`

### Trin 2: Konfigurer
1. **Navn**: "Personalhåndbog - Download og åbn"
2. **Beskrivelse**: "Download HTML-filen og åbn i browser"
3. Vælg **"Åbn"** eller **"Download"** som visningsmetode
4. Klik **"Gem og vis"**

Studerende kan nu downloade og åbne filen lokalt.

---

## ⚠️ Mulige Problemer og Løsninger

### Problem 1: JavaScript virker ikke
**Symptom**: Søgning og collapsible sektioner virker ikke

**Løsning**:
- Tjek Moodle's sikkerhedsindstillinger
- Kontakt Moodle administrator for at tillade JavaScript
- Alternativt: Brug File resource metoden

### Problem 2: Styling ser forkert ud
**Symptom**: Farver, layout eller fonter vises ikke korrekt

**Løsning**:
- Sørg for at du kopierede **ALT** HTML-indhold inklusive `<style>` tags
- Tjek at du er i HTML-editor mode (ikke visual mode)
- Prøv at gemme og genindlæse siden

### Problem 3: For stor fil
**Symptom**: Moodle accepterer ikke filen pga. størrelse

**Løsning**:
- Filen er ~112 KB, så det skulle ikke være et problem
- Kontakt administrator hvis der er upload begrænsninger
- Alternativt: Host filen eksternt og link til den

### Problem 4: HTML tags fjernes automatisk
**Symptom**: Kun tekst vises, ingen struktur

**Løsning**:
- Tjek at du bruger **HTML source editor** (< > knap)
- Ikke visual editor mode
- Moodle skal tillade HTML indhold i Page/Label aktiviteter

### Problem 5: Collapsible virker ikke på mobile
**Symptom**: Kan ikke klikke på sektioner på mobil/tablet

**Løsning**:
- Dette er sandsynligvis ikke et problem - designet er responsive
- Test i forskellige browsers (Chrome, Safari, Firefox)
- Tjek at JavaScript er aktiveret på enheden

---

## 🎯 Bedste Praksis

### For Studerende/Medarbejdere:
- **Page aktivitet**: Bedst for intern visning i Moodle
- Nem adgang direkte i kurset
- Ingen download nødvendig

### For Eksterne/Print:
- **File resource**: Til download og lokal brug
- Kan åbnes offline
- Nem at dele

### For Integration:
- **Label aktivitet**: Hvis du vil have det synligt på forsiden
- Tager mere plads på kursets forside

---

## 📊 Verificer Funktionalitet

Efter indsættelse, test følgende:

- [ ] Søgeboksen accepterer input
- [ ] Søgeresultater opdateres live
- [ ] Søgeord highlightes i gult
- [ ] Kategorier kan vælges i sidebar
- [ ] Lag 2 sektioner kan foldes ud/sammen
- [ ] Lag 3 sektioner kan foldes ud/sammen
- [ ] "Udfold alt" knap virker
- [ ] "Sammenfold alt" knap virker
- [ ] Responsivt design på mobil/tablet
- [ ] Tags vises under hver artikel

---

## 🆘 Support

**Tekniske problemer med Moodle:**
- Kontakt IT Helpdesk eller Moodle administrator

**Indholdsrettelser:**
- Kontakt HR@zealand.dk

**HTML/Wiki problemer:**
- Check filerne i `C:\copilottest\wiki_moodle\`
- Gendan fra GitHub hvis nødvendigt

---

**Succes med deployment!** 🎉
