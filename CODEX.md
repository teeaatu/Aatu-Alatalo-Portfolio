# Aatu Alatalon Portfolio — Codex & AI-ohjeet

Tämä tiedosto opastaa Codexia (ChatGPT Codex / VS Code / Cursor / AI-agentit) toimimaan tässä koodikannassa.

## 1. Yleiskuva ja arkkitehtuuri
- **Sivusto:** Aatu Alatalon valokuvausportfolio.
- **Teknologia:** Astro (Static Site Generation), HTML/CSS/JS.
- **Kuvien säilytys:** Kuvat ladataan Cloudflare R2 -objektitallennukseen (`https://media.aatualatalo.com/Photographs/...`).
- **Tietorakenne:** Kunkin kategorian kuvat ja sarjat määritellään YAML-tiedostoissa: `src/data/*.yml`.
- **Esikatselut (LQIP):** Pienen resoluution base64-placeholderit tallennetaan tiedostoon `src/data/lqip.json`.
- **Kuvavahti:** `scripts/auto_upload_watch.py` valvoo `Portfolio-Uploads`-kansiota ja lataa pudotetut kuvat automaattisesti R2:een luoden samalla WebP/AVIF-versiot.

## 2. EHDOTTOMAT SÄÄNNÖT (CRITICAL RULES)
1. **Kieli:** Vastaa AINA suomeksi. Pidä vastaukset lyhyinä, ytimekkäinä ja suorina ilman turhia selittelyjä.
2. **Git & Julkaisu:** ÄLÄ KOSKAAN aja `git push` ilman käyttäjän erillistä, nimenomaista lupaa.
3. **Koodimuutokset:** Älä muuta sivuston layoutia, tyylejä tai olemassa olevia toimintoja ilman käyttäjän lupaa.
4. **Laadunvarmistus:** Aja AINA `npm run build` jokaisen koodi- tai datamuutoksen jälkeen varmistaaksesi, että sivusto kääntyy virheettömästi.
5. **Alt-tekstit:** ÄLÄ KOSKAAN käytä alt-teksteissä sanoja "kuva" tai "valokuva". Kuvaile teoksen sisältöä suoraan ja laadukkaasti.

## 3. Uuden kuvan lisäysportfolioon (Työnkulku)
Kun käyttäjä pyytää lisäämään kuvan:
1. Jos kuva on pudotettu `Portfolio-Uploads`-kansioon:
   - Käynnistä kuvavahti tarvittaessa (`./Käynnistä_Kuvavahti.command` tai `python3 scripts/auto_upload_watch.py`).
   - Skripti muuntaa kuvan sRGB-WebP:ksi, luo pikkukuvat, siirtää alkuperäisen `originals/`-kansioon ja lataa R2:een.
2. Generoi tai lue LQIP-base64-merkkijono ja lisää se tiedostoon `src/data/lqip.json`.
3. Lisää kuvan tiedot halutun sarjan tiedostoon `src/data/[sarja].yml`:
   ```yaml
   - kuva: https://media.aatualatalo.com/Photographs/[Tiedostonimi].webp
     width: [leveys]
     height: [korkeus]
     otsikko: [Englanninkielinen otsikko] / [Suomenkielinen otsikko]
     paikka: [Englanninkielinen paikka] / [Suomenkielinen paikka]
     alt_text: "[Kuvaileva suomenkielinen alt-teksti ilman sanaa kuva tai valokuva]"
   ```
4. Aja `npm run build`.
5. Tee paikallinen commit (`git commit -m "..."`).
6. Pyydä käyttäjältä lupa ennen kuin ajat `git push`.

## 4. Tärkeimmät komennot
- **Kehityspalvelin:** `npm run dev` (avautuu osoitteessa http://localhost:4321)
- **Käännöstesti:** `npm run build`
- **Kuvavahti:** `python3 scripts/auto_upload_watch.py`
