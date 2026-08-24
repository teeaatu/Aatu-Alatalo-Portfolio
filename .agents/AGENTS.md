# Portfolio-projektin säännöt

## Alt-tekstin kirjoittaminen (TÄRKEÄ)

Kun generoit alt-tekstiä kuville, kirjoita se **aina englanniksi** ja noudata näitä sääntöjä:

### Tyyli
- Kirjoita suoraan ja asiallisesti – kuvaile mitä kuvassa on, ei mitä se "edustaa" tai "tuo esille"
- Lyhyt on usein parempi: 1–3 lausetta riittää
- Älä käytä valokuvaukseen liittyviä tyyliarvioita ("moody", "striking", "cinematic", "dramatic", "ethereal", "intimate", "dreamy", "vibrant", "serene", "powerful")
- Älä käytä AI-kaavamaisia ilmaisuja ("A prominent...", "contrasts sharply against", "adding to the authentic atmosphere", "highlighting the rich textures", "eerie reflections", "vibrant pop of color")
- Älä aloita "A [adjektiivi] [lajityyppi] photograph of..." -rakenteella
- Älä mainitse sanojen "kuva" tai "valokuva" (myös englanniksi: vältä "photograph of", "image of")

### Kielletyt sanat – älä koskaan käytä näitä
Nämä sanat ovat tunnistettavia AI-merkkejä ja ne on aina korvattava neutraalimmalla ilmaisulla:

| Kielletty sana | Korvaa esim. näin |
|---|---|
| `moody` | poista kokonaan tai kuvaile valaistus faktisesti |
| `striking` | poista kokonaan |
| `ethereal` / `dreamy` | poista kokonaan |
| `vibrant` | käytä värin nimeä suoraan (esim. "bright green", "deep red") |
| `cinematic` | poista kokonaan |
| `dramatic` | poista kokonaan tai kuvaile mikä tekee siitä dramaattisen |
| `contrasts sharply` | kuvaile kontrasti suoraan (esim. "stands out against") |
| `perfectly` | poista kokonaan |
| `intimate` | poista kokonaan |
| `prominent` | poista kokonaan tai sano suoraan mikä on etualalla |

### Rakenne
- Kerro ensin mitä tai keitä kuvassa on
- Sitten missä tai millaisessa ympäristössä
- Tarvittaessa paikka ja vuosi lopuksi

### Hyvä esimerkki
❌ `"A moody street photograph of a crowd walking down a wet street on a rainy day. Bright pops of color come from a person in a yellow raincoat, contrasting with the cool blueish tones."`

✅ `"A crowd walking down a wet street in the rain. A dark pink umbrella stands out in the foreground, with a person in a yellow raincoat visible further back."`

---

## Autonomous Debugging & First-Principles Problem Solving Protocol

Kaikessa vianetsinnässä, visuaalisissa virheissä, odottamattomissa tiloissa ja arkkitehtuuripäätöksissä noudatetaan aina tätä 4-vaiheista päättelyprosessia ennen koodimuutoksia:

### 1. Concrete Observation vs. Assumption
- Erottele havainto oletuksesta: mitä tarkalleen tapahtuu vs. mitä odotettiin.
- Erota oire syystä: älä oleta, että ensimmäinen näkyvä virhe johtuu suoraan viimeksi muokatusta komponentista.
- Määritä rajapinta: onko kyseessä renderöinti-, tilavuoto-, elinkaari/ajoitus-, build-työkalu- vai kilpatilanneongelma (race condition)?

### 2. Hypothesis Generation & Active Disproof ("Wait, actually...")
- Luo vähintään 2–3 erillistä teknistä hypoteesia ongelman syystä.
- Yritä aktiivisesti kumota omat hypoteesisi vertaamalla:
  * Framework & kääntäjätoteutus (Astro static build, Vite bundle ordering, hydraatio).
  * Selain- ja alustainternalsit (CSS stacking contexts, event loop, spesifisyys, asynkroninen I/O, välimuisti/session-tila).
  * Datavirta ja reunatapaukset (null-tilat, race conditionit, vanhentunut välimuisti).

### 3. Root Cause Pinpointing
- Tunnista tarkka mekanismi, joka aiheuttaa vian (ei pelkkää oireen pintapaikkaa).
- Hylkää pintapuoliset väliaikaiskorjaukset: ei sokeita `!important`-määritteitä, mielivaltaisia `setTimeout`-viiveitä tai ylimääräisiä wrapper-elementtejä, ellei alusta sitä ehdottomasti vaadi.

### 4. Minimal Surgical Execution
- Toteuta puhtain ja eristetyin ratkaisu, joka korjaa perimmäisen juurisyyn ilman sivuvaikutuksia olemassa oleviin komponentteihin.
- Esitä lyhyt tekninen päättelyketju ja tarkka korjaus ennen lopullisen koodin toimittamista.

