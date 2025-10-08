# En guide för att skapa undersökningar med en csv-fil
Det är möjligt att importera undersökningsalternativ från en csv-fil, så länge filen följer följande regler.</br>

De enda obligatoriska fälten är facilitetens namn, kapacitet och minsta gruppsstorlek. Avgränsaren i .csv-filen spelar ingen roll (det kan vara ,, ; eller "," osv.), eftersom Separator automatiskt kommer att ändra dem till ;. </br></br>

Bilden nedan visar formatet på en exempelfil:</br>
<img src="/static/images/csv.png" alt="Exempel CSV-fil" width="900">
</br></br>
<img src="static/images/csv-create.png" alt="CSV-tiedostosta luonti" width="900">
</br></br>

Som standard utesluter fördelaren ett mindre populärt gruppalternativ om dess minimistorlek inte uppfylls i fördelningen. Om du vill att vissa grupper alltid ska ingå kan du lägga till en kolumn som heter "Mandatory" i CSV-filen och fylla den med värdena TRUE eller FALSE beroende på om gruppen är obligatorisk eller inte. Värdena i kolumnen "Mandatory" kan till exempel vara TRUE, true eller True – det spelar ingen roll med versaler eller gemener. Ett FALSE-värde behöver egentligen inte anges, men kolumnen måste ha något värde på varje rad (till exempel tomma citattecken " " fungerar bra).

Bilden nedan visar formatet på en exempelfil som innehåller grupper som måste ingå:
<img src="/static/images/csv2.png" alt="Exempel CSV-fil">
</br></br>
<img src="static/images/csv2-create.png" alt="CSV-tiedostosta luonti" width="900">

## När du skapar från E-lomake
När du skapar en undersökning genom E-lomake måste det första fältet vara namnet på alternativet, det andra fältet måste vara antalet platser tillgängliga för alternativet, och det tredje fältet måste vara det minsta antalet platser för alternativet. Om något av dessa saknas kommer inte importen av csv-filen att fungera.

Visning av undersökningsrespons där dagiset eller liknande fyller i sin information.
<img src="/static/images/csv-reply-view.png" alt="Vastausnäkymä käyttäjälle">

I de tre första fälten spelar namnet ingen roll (dagisets namn, namn, ID osv., eller kapacitet, maximal kapacitet osv., är alla acceptabla, liksom min_size, minimumstorlek osv.), så länge ordningen är korrekt.

Att svara på ovanstående undersökning kommer att generera en CSV-fil, som kan hittas i avsnittet "Formulärrapport" på E-lomake.
<img src="/static/images/csv-report-view.png" alt="Lomakeraportti">

<strong>De första två kolumnerna är onödiga (Tall.id, Tallennusaika), så ta bort dem från den skapade .csv-filen.</strong> 
