---
name: add_image
description: Lisää uuden kuvan portfolioon. Lataa kuvan, ajaa optimointiskriptin, generoi alt-tekstin ja päivittää oikean YML-datatiedoston. Käytä tätä skilliä aina kun käyttäjä pyytää lisäämään kuvan johonkin galleriaan.
---

# Kuvan lisääminen portfolioon

Noudata tätä työnkulkua täsmällisesti ja suorita kaikki vaiheet peräkkäin ilman keskeytyksiä.

## Vaihe 1: Lataa kuva R2-bucketiin

Kuva tulee ladata Cloudflare R2 -buckettiin oikeaan kansioon.

- Kansiorakenne bucketissa: `Photographs/<kategorian-nimi>/<tiedostonimi>`
- Lataus tapahtuu AWS CLI:llä tai boto3:lla `.env`-tiedoston tunnuksilla
- Tiedostonimi säilytetään sellaisenaan ellei käyttäjä toisin ohjeista

## Vaihe 2: Aja optimointiskripti

Aja projektin Python-skripti, joka generoi automaattisesti desktop- ja mobile-thumbnailit R2-bucketiin:

```bash
cd /Volumes/A26/Portfolio\ Home
source venv/bin/activate
python scripts/generate_thumbs.py --prefix "Photographs/<kategorian-nimi>/"
```

- Skripti hakee alkuperäiset kuvat R2:sta, luo niistä WebP-variantit (1600px desktop, 600px mobile) ja lataa ne takaisin `thumbs/`-alikansioon
- Tarkista tulosteesta että kaikki thumbnailt luotiin onnistuneesti
- Jos haluat testata ensin: lisää `--dry-run`-lippu

## Vaihe 3: Selvitä kuvan metadata

Tarvitset seuraavat tiedot YML-merkintää varten:

- **kuva**: tiedostonimi (esim. `DSC4115-1.jpg`)
- **width / height**: alkuperäiskuvan pikselidimensiot (käytä PIL:iä tai exiftool-komentoa)
- **otsikko**: kaksikielinen otsikko muodossa `English Title / Suomenkielinen otsikko`
- **paikka**: muodossa `Kaupunki, Maa Vuosi` (esim. `Oulu, Finland 2025`)
- **alt_text**: kirjoitetaan vaiheessa 4

## Vaihe 4: Kirjoita alt-teksti

Alt-teksti kirjoitetaan **englanniksi**. Noudata näitä sääntöjä tiukasti:

### Kielletyt sanat (älä koskaan käytä)
| Kielletty sana | Korvaa näin |
|---|---|
| moody | poista tai kuvaile valaistus faktisesti |
| striking | poista kokonaan |
| ethereal / dreamy | poista kokonaan |
| vibrant | käytä värin nimeä suoraan (esim. "bright green") |
| cinematic | poista kokonaan |
| dramatic | poista tai kuvaile mikä tekee siitä dramaattisen |
| contrasts sharply | kuvaile suoraan (esim. "stands out against") |
| perfectly | poista kokonaan |
| intimate | poista kokonaan |
| prominent | poista tai sano suoraan mikä on etualalla |

### Tyyli
- Kirjoita suoraan: kuvaile mitä kuvassa on, ei mitä se "edustaa"
- 1–3 lausetta riittää
- Älä aloita "A [adj] [genre] photograph of..." -rakenteella
- Älä käytä sanoja "photograph of" tai "image of"

### Rakenne
1. Mitä tai keitä kuvassa on
2. Missä tai millaisessa ympäristössä
3. Tarvittaessa paikka ja vuosi

### Esimerkki
HUONO: "A moody street photograph of a crowd walking down a wet street."
HYVÄ: "A crowd walking down a wet street in the rain. A dark pink umbrella stands out in the foreground."

## Vaihe 5: Päivitä YML-datatiedosto

Lisää uusi merkintä tiedostoon `_data/<kategorian-nimi>.yml`. Noudata täsmälleen olemassa olevaa rakennetta:

```yaml
- kuva: tiedostonimi.jpg
  width: 3000
  height: 2000
  otsikko: English Title / Suomenkielinen otsikko
  paikka: Oulu, Finland 2025
  alt_text: "Kirjoitettu alt-teksti tähän."
```

- Lisää uusi kuva listan loppuun ellei käyttäjä toisin ohjeista
- Säilytä muiden merkintöjen rakenne ja sisennykset täsmälleen ennallaan

## Vaihe 6: Testaa build

Varmista että sivusto rakentuu virheettömästi:

```bash
cd /Volumes/A26/Portfolio\ Home
bundle exec jekyll build
```

Tarkista että build päättyy onnistuneesti eikä sisällä varoituksia kyseisestä tiedostosta.

## Vaihe 7: Raportoi käyttäjälle

Ilmoita lyhyesti:
- Mihin kategoriaan kuva lisättiin
- Tiedostonimi
- Generoidut thumbnailt (desktop + mobile)
- Alt-teksti jota käytettiin

Älä pyydä git push -lupaa — käyttäjä antaa sen itse erikseen.
