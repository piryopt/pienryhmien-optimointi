# FAQ

## Hur fungerar Jakaja?
- Jakaja använder den så kallade **ungerska algoritmen**.
- Användaren prioriterar de angivna grupperna baserat på deras preferenser.
- Preferenser översätts till poäng så att användaren ger flest poäng till de grupper de har valt som första. Minsta antal poäng ges till det senaste valet eller något icke-markerat alternativ.
- Den ungerska algoritmen prioriterar gruppvalet så att summan för alla poäng som ges till en grupp är så hög som möjligt.
- Om en grupp inte uppnår sitt minsta antal medlemmar tas den bort och dess studenter flyttas till andra grupper.
- En mer detaljerad (engelsk) förklaring av algoritmen finns på [Jakajas GitHub-sida](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/hungarian.md)

## Hur fylls obligatoriska grupper?
- Som standard tar Jakaja bort de grupper som inte uppnår minsta gruppstorlek. Enkätskaparen kan dock ange att en grupp är obligatorisk. I så fall fylls gruppen till minst sin minimistorlek, oavsett svaren.
    - Det betyder att deltagare som inte har valt gruppen kan placeras där vid behov. Jakaja försöker dock alltid i första hand placera de deltagare som har visat störst intresse för gruppen.
- En student som har **avvisat** en grupp kan i vissa fall ändå placeras i den.
    - Detta sker endast om gruppen inte kan uppnå sin minimistorlek med deltagare som inte har avvisat den.
    - I sådana fall är det enkätskaparens ansvar att granska deltagarnas motiveringar till avvisningen och avgöra om studenten kan placeras i gruppen.

**OBS!** En obligatorisk grupp kan ändå tas bort från fördelningen om det finns så få deltagare att det inte går att fylla alla obligatoriska grupper till minimistorlek.

## Jag har frågor – Vem kan jag vända mig till?
Jakaja har en feedbacksida där du kan ställa dina frågor.