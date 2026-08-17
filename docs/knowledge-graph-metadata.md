# Aatu Elias Alatalo — Google Knowledge Graph, Wikidata & Wikipedia -dokumentaatio

Tämä tiedosto sisältää Aatu Alatalon (Aatu Elias Alatalo) virallisen entiteettikuvauksen, Schema.org Person -määrittelyn, Wikidata-kentät sekä suomenkielisen Wikipedia-artikkeliluonnoksen.

---

## 1. Schema.org Person JSON-LD (Sivuston koodissa)

Sivuston [aatualatalo.com](https://aatualatalo.com) `<head>`-osioon on sijoitettu seuraava Googlen Knowledge Graph -optimoitu rakenne:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "https://aatualatalo.com/#person",
      "name": "Aatu Elias Alatalo",
      "alternateName": ["Aatu Alatalo", "Teeaatu"],
      "jobTitle": "Valokuvaaja",
      "description": "Suomalainen valokuvaaja ja Hasselblad Masters 2026 -finalisti (Project//21).",
      "url": "https://aatualatalo.com",
      "image": "https://aatualatalo.com/assets/images/aatu-alatalo-valokuvaaja-oulu.jpg",
      "birthDate": "2005-01-25",
      "birthPlace": {
        "@type": "Place",
        "name": "Tyrnävä, Finland"
      },
      "homeLocation": {
        "@type": "Place",
        "name": "Oulu, Finland"
      },
      "nationality": {
        "@type": "Country",
        "name": "Finland"
      },
      "alumniOf": {
        "@type": "EducationalOrganization",
        "name": "Oulun ammattikorkeakoulu"
      },
      "award": [
        "Hasselblad Masters 2026 Finalist (Project//21)",
        "SAKUstars 2023 Honorable Mention (Photographic Art in a Day)"
      ],
      "sameAs": [
        "https://www.instagram.com/teeaatu/",
        "https://www.linkedin.com/in/aatu-alatalo-b67274304/",
        "https://www.hasselblad.com/inspiration/masters/2026/"
      ],
      "knowsAbout": [
        "Photography",
        "Fine Art Photography",
        "Portrait Photography",
        "Street Photography",
        "Landscape Photography",
        "Documentary Photography"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://aatualatalo.com/#website",
      "url": "https://aatualatalo.com",
      "name": "Aatu Alatalo Portfolio",
      "publisher": {
        "@id": "https://aatualatalo.com/#person"
      },
      "inLanguage": ["fi", "en"]
    }
  ]
}
```

---

## 2. Wikidata-syötteet (www.wikidata.org)

Wikidata on Wikipedian sisarhanke ja **Googlen Knowledge Graphin tärkein rakenteisen datan lähde**. Voit luoda uuden kohteen osoitteessa [wikidata.org/wiki/Special:NewItem](https://www.wikidata.org/wiki/Special:NewItem).

### Perustiedot (Label & Description)
* **Kieli fi:**
  * Otsikko: `Aatu Alatalo`
  * Kuvaus: `suomalainen valokuvaaja`
  * Aliakset: `Aatu Elias Alatalo`, `Teeaatu`
* **Kieli en:**
  * Label: `Aatu Alatalo`
  * Description: `Finnish photographer`
  * Aliases: `Aatu Elias Alatalo`

### Väitteet (Statements / Properties)
| Ominaisuus (Property) | Arvo (Value) | Huomiot / Lähteet |
|---|---|---|
| **instance of (P31)** | `human (Q5)` | Ihmisyksilö |
| **sex or gender (P21)** | `male (Q6581097)` | Mies |
| **country of citizenship (P27)** | `Finland (Q33)` | Suomi |
| **given name (P735)** | `Aatu (Q18689945)` | Etunimi |
| **family name (P734)** | `Alatalo (Q11850123)` | Sukunimi |
| **date of birth (P569)** | `25 January 2005` | Tarkkuus: päivä |
| **place of birth (P19)** | `Tyrnävä (Q999233)` | Syntymäpaikka |
| **occupation (P106)** | `photographer (Q33231)` | Valokuvaaja |
| **educated at (P69)** | `Oulu University of Applied Sciences (Q3356064)` | Oamk |
| **official website (P856)** | `https://aatualatalo.com` | Virallinen kotisivu |
| **Instagram username (P2002)** | `teeaatu` | @teeaatu |
| **LinkedIn personal profile ID (P6634)** | `aatu-alatalo-b67274304` | LinkedIn |
| **award received (P166)** | `Hasselblad Masters Finalist (2026)` | Sarja Project//21 |

---

## 3. Suomenkielinen Wikipedia-artikkeliluonnos (Wikitext)

Voit luoda tämän luonnoksen Wikipedian hiekkalaatikkoon / käyttäjäsivulle:

```wikitext
{{Valokuvaaja
| nimi = Aatu Alatalo
| syntymäaika = {{Syntymäaika ja ikä|2005|1|25}}
| syntymäpaikka = [[Tyrnävä]]
| kansalaisuus = [[Suomi]]
| koulutus = Media-alan perustutkinto ([[Jokilaaksojen koulutuskuntayhtymä|JEDU]])<br />[[Oulun ammattikorkeakoulu]] (medianomi, opiskelee)
| ammatti = [[Valokuvaaja]]
| tunnetut_työt = Valokuvia Suomenlahdelta, Hasselblad Masters 2026 (Project//21)
| palkinnot = Hasselblad Masters 2026 -finalisti (Project//21)<br />SAKUstars 2023 -kunniamaininta
| kotisivu = [https://aatualatalo.com aatualatalo.com]
}}

'''Aatu Elias Alatalo''' (s. [[25. tammikuuta]] [[2005]] [[Tyrnävä]]) on suomalainen [[Oulu]]ssa asuva valokuvaaja. Hänet valittiin kansainvälisen [[Hasselblad Masters]] 2026 -valokuvakilpailun finaaliin alle 21-vuotiaiden sarjassa (Project//21).

== Ura ja opinnot ==
Alatalo aloitti valokuvauksen vuonna 2014. Hän on suorittanut media-alan ja kuvallisen ilmaisun perustutkinnon [[Jokilaaksojen koulutuskuntayhtymä|Jokilaaksojen koulutuskuntayhtymä Jedussa]] ja opiskelee medianomiksi [[Oulun ammattikorkeakoulu|Oulun ammattikorkeakoulussa]]. Alatalon valokuvataiteelle on ominaista dokumentaarinen ja toimituksellinen ote, jossa yhdistyvät suomalainen arki, katuvalokuvaus ja pohjoinen valo.

Vuonna 2026 Alatalo valittiin kymmenen parhaan joukkoon kansainvälisessä Hasselblad Masters -kilpailussa yli 108 000 osallistuneen kuvan joukosta sarjassa Project//21.

Alatalon teoksia on ollut esillä yksityis- ja ryhmänäyttelyissä muun muassa Piippolan Könkkölässä sekä Kestilän kirjastossa vuosina 2023 ja 2024.

== Palkinnot ja tunnustukset ==
* '''Hasselblad Masters 2026''': Finalisti, Project//21 -sarja.
* '''SAKUstars 2023''': Kunniamaininta, sarja ''Valokuvataide päivässä''.

== Lähteet ==
{{Viitteet|lähteet=
<ref>[https://www.hasselblad.com/inspiration/masters/2026/ Hasselblad Masters 2026 Finalists]. Hasselblad. Viitattu 17.8.2026.</ref>
<ref>[https://aatualatalo.com Virallinen portfoliosivusto]. Viitattu 17.8.2026.</ref>
}}

== Aiheesta muualla ==
* [https://aatualatalo.com Virallinen verkkosivusto]
* [https://www.instagram.com/teeaatu/ Aatu Alatalo Instagramissa]
* [https://www.linkedin.com/in/aatu-alatalo-b67274304/ Aatu Alatalo LinkedInissä]

{{Tynkä/Valokuvaaja}}

[[Luokka:Suomalaiset valokuvaajat]]
[[Luokka:Vuonna 2005 syntyneet]]
[[Luokka:Tyrnävältä kotoisin olevat henkilöt]]
```

---

## 4. Googlen Knowledge Panelin lunastus (Claiming Knowledge Panel)

Kun Google muodostaa nimesi haulla oikeanpuoleisen tietopaneelin:
1. Hae Googlella: `Aatu Alatalo` tai `Aatu Alatalo valokuvaaja`.
2. Klikkaa tietopaneelin alareunasta linkkiä **"Claim this knowledge panel"** (tai *"Omistatko tämän tietopaneelin?"*).
3. Tunnistaudu Google Search Console -tililläsi, jolla hallinnoit `aatualatalo.com` -verkkotunnusta. Vahvistus tapahtuu välittömästi.
4. Tämän jälkeen voit ehdottaa Googlelle suoraan pääkuvan vaihtoa, kuvatekstien korjauksia ja sosiaalisen median linkkien päivityksiä.
