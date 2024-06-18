# En guide för att skapa undersökningar med en csv-fil
Det är möjligt att importera undersökningsalternativ från en csv-fil, så länge filen följer följande regler.

## DEN VIKTIGA DELEN (När du skapar från Elomake)
När du skapar en undersökning genom Elomake måste det första fältet vara namnet på alternativet, det andra fältet måste vara antalet platser tillgängliga för alternativet, och det tredje fältet måste vara det minsta antalet platser för alternativet. Om något av dessa saknas kommer inte importen av csv-filen att fungera.

Visning av undersökningsrespons där dagiset eller liknande fyller i sin information.
<img src="/static/images/csv-reply-view.png" alt="Vastausnäkymä käyttäjälle">

I de tre första fälten spelar namnet ingen roll (dagisets namn, namn, ID osv., eller kapacitet, maximal kapacitet osv., är alla acceptabla, liksom min_size, minimumstorlek osv.), så länge ordningen är korrekt.

Att svara på ovanstående undersökning kommer att generera en CSV-fil, som kan hittas i avsnittet "Formulärrapport" på Elomake.
<img src="/static/images/csv-report-view.png" alt="Lomakeraportti">

<strong>De första två kolumnerna är onödiga (Tall.id, Tallennusaika), så ta bort dem från den skapade .csv-filen.</strong> 

## Annat
De enda obligatoriska fälten är facilitetens namn, kapacitet och minsta gruppsstorlek. Avgränsaren i .csv-filen spelar ingen roll (det kan vara ,, ; eller "," osv.), eftersom Separator automatiskt kommer att ändra dem till ;. Bilden nedan visar formatet på en exempelfil:
<img src="/static/images/csv.png" alt="Esimerkki csv-tiedosto">