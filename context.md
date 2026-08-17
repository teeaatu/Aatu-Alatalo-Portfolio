# Portfolion kehityshistoria ja muutosloki (Portfolio History & Context)

Tähän tiedostoon on koottu portfolion arkkitehtuurin, ominaisuuksien ja sisällön merkittävät kehitysaskeleet.

---

## 📅 Elokuu 2026

### 1. Sivuston taustan ja visuaalisuuden hionta (17.8.2026)
- **Täysin puhdas valkoinen tausta (`#ffffff`):** Poistettu aiempi harmahtava/kellertävä sävy ja korvattu se 100 % puhtaalla galleriavalkoisella, jolloin valokuvat ja kontrastit toistuvat kirkkaasti ja raikkaasti.
- **Kohinan ja rakeisuuden poisto:** Poistettu kaikki SVG-noise- ja grain-overlayt, jotta sivusto on täysin puhdas ja veitsenterävä.
- **Index-valikon Editorial Hover Preview (Desktop):**
  - Toteutettu desktop-valikkoon vuorovaikutteinen esikatselu, jossa kunkin kategorian ensimmäinen teoskuva liukuu pehmeästi esiin vasempaan ruutuun.
  - Aito ja rauhallinen kahden kerroksen ristihäivytys (Dual-Layer Smooth Crossfade) ilman äkillisiä välähdyksiä.
  - Valikon ollessa auki kustomoitu laskurikursori piilotetaan ja käytössä on normaali osoitinkursori.
- **Valokuvia Suomenlahdelta (Work IV) editorial-teksti:**
  - Tekstikortit uudistettu kevyeksi ja elegantiksi *EB Garamond* -typografiaksi ilman vanhanaikaisia laatikkoreunuksia.
  - Ylimääräiset vanhat tekstikortit poistettu muista gallerioista.

### 2. Uusi teoslisäys & kuvanhallinta (15.8.2026)
- Lisätty uusi teos *Kaksi ihmistä* sarjoihin **Mustavalkoinen sarja** ja **Uusimmat** (`Kaksiihmista.webp`).

### 3. Mobiilikäytettävyyden ja navigoinnin viimeistely (10.–14.8.2026)
- **Eleohjaukset (Swipe):** Viritetty sulava vaakapyyhkäisy kuvalta toiselle siten, että Safarin natiivi reunan taaksepäinpyyhkäisy toimii samalla esteettömästi.
- **Mobiilinuolet & haptiikka:** Hienosäädetty mobiilin navigointinuolien sijoittelua ja kosketusalueita (min 44px).
- **Kaikki teokset (Thumbs view):** Päivitetty verhomainen liukuanimaatio ja parannettu katselunäkymän sulkemislogiikkaa.

### 4. Karttaintegraatio & Työ IV (10.8.2026)
- Integroitu Leaflet.js-kartta ja interaktiiviset kuvauspisteet *Työ IV (Valokuvia Suomenlahdelta)* -sarjaan.
- Karttapisteitä klikkaamalla esiin aukeavat postikorttimaiset teosnäkymät.

### 5. Arkkitehtuurimigraatio: Jekyll → Astro (9.8.2026)
- Koko sivuston modernisointi: siirrytty vanhasta Jekyll-pohjasta moderniin **Astro (Static Output)** -arkkitehtuuriin.
- Nopeampi build-aika, parempi koodin modulaarisuus (`GalleryLayout.astro`) ja nolla Cumulative Layout Shift (CLS).
- Täysi kaksikielisyysreititys (`/` suomeksi ja `/en/` englanniksi) ilman ylimääräisiä uudelleenohjauksia.
- GEO/SEO-metatietojen, sitemapin ja kanonisten linkkien täydellinen automatisointi.

---

## 📅 Kesäkuu – Heinäkuu 2026

### 1. Pilvi-infrastruktuuri ja Cloudflare R2 -kuvaoptimointi (6.–7.6.2026)
- Siirretty suuret valokuvat ja korkealaatuiset WebP-versiot nopeaan Cloudflare R2 -tallennustilaan (`media.aatualatalo.com`).
- Optimoitu kuvakoot ja LCP (Largest Contentful Paint) huipputasolle.

### 2. SEO, Alt-tekstit ja tekoälyoptimointi (AI-SEO) (31.5.–7.6.2026)
- Kirjoitettu laadukkaat, faktapohjaiset ja neutraalit alt-tekstit kaikille galleriakuville (`vari-ja-muoto`, `mustavalkoinen-sarja`, `masters-2026`, `luonto-ja-ymparisto`, `raw`, `elaimet` jne.).
- Luotu tekoälyhakukoneille optimoidut `llms.txt` ja `llms-full.txt` -tiedostot.

---

## 📅 Toukokuu 2026

### 1. Monikielisyysremontti (27.–30.5.2026)
- Rakennettu kattava suomi–englanti-kaksikielisyysjärjestelmä kaikkiin gallerioihin, valikoihin ja About/Ajatuksia-sivuihin.
- Lisätty tyylikäs pill-muotoinen kielenvaihtaja työpöydälle ja mobiiliin.

### 2. Uudet galleriat ja teokset (21.–28.5.2026)
- Lisätty teoksia: *Prinsessa*, *Dalmatialainen*, *Kinogrilli*, *Unto Välikatto*, *Kaksi naista selin*.
- Luotu diptyykkikuvien tuki ja yhdistetyt kuvatekstit.