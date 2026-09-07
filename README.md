# Max Andersen Frisk – CV & Portföljhemsida

Professionell och modern webbplats för CV och portfölj anpassad för **Chalmers Tekniska Högskola (Civilingenjör Elektroteknik)**.

Plats för projektet:
`C:\Users\maxan\.gemini\antigravity\scratch\mitt-cv`

---

## 🚀 Funktioner

- **Skräddarsydd Chalmers-profil**: Välformulerad text med fokus på kretsteori, hårdvara, inbyggda system och tillämpad programmering.
- **Arbetslivserfarenhet**: Inkluderar återkommande anställning på **Biltema (Sommaren 2025 & Sommaren 2026)** med förnyat förtroende, samt service- och logistikerfarenhet från **Mangold Restauranger**.
- **Besöksräknare & Analytics**: 
  - Livebesöksindikator i sidfoten.
  - Förberedd för gratis och GDPR-godkänd webbanalys (**GoatCounter** eller **Cloudflare Analytics**) utan cookie-banners.
- **Mörkt & ljust läge (Dark/Light mode)**: Sparas i webbläsaren.
- **Utskriftsoptimerad (PDF)**: Klicka på knappen *"Spara som PDF / Skriv ut"* för att skapa ett rent och snyggt pappers-CV för ansökningar.

---

## 📊 Så ser du vem som besöker din hemsida

För en personlig hemsida eller ett CV vill man ofta veta **när en rekryterare öppnar länken**, **vilken stad de sitter i** och **om de klickade från t.ex. ett mejl eller LinkedIn**.

### Rekommenderad metod: GoatCounter (100% gratis, inga cookies)
1. Gå till [https://www.goatcounter.com](https://www.goatcounter.com) och skapa ett gratiskonto (tar 30 sekunder).
2. Välj en kod, t.ex. `maxandersen` (din adress blir då `https://maxandersen.goatcounter.com`).
3. Öppna `index.html` och lägg till följande rad i `<head>` (ersätt `DITT-KONTO` med namnet du valde):
   ```html
   <script data-goatcounter="https://DITT-KONTO.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
   ```
4. Klart! När någon öppnar din hemsida loggas det i din privata instrumentpanel där du ser:
   - **Stad och land** (t.ex. Göteborg, Stockholm, etc.)
   - **Tidpunkt & datum**
   - **Hänvisning / Referrer** (t.ex. om de kom från LinkedIn, ett e-postmeddelande eller direktlänk)
   - **Enhet** (iPhone, Android, Windows, Mac)

---

## 💻 Så här förhandsgranskar du lokalt

### Alternativ 1: Direkt i webbläsaren
Dubbelklicka på [`index.html`](file:///C:/Users/maxan/.gemini/antigravity/scratch/mitt-cv/index.html).

### Alternativ 2: Med lokal server
Öppna PowerShell i projektmappen och kör:
```powershell
python -m http.server 8000
```
Gå sedan till [http://localhost:8000](http://localhost:8000).
