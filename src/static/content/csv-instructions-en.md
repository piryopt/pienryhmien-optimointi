# A guide for creating surveys with a csv file
It is possible to import survey choices from a csv file, as long as the file follows the following set of rules.

## THE IMPORTANT PART (When creating from Elomake)
When creating a survey through Elomake, the first field must be the name of the choice, the second field must be the amount of seats available in the choice and the third field must be the minimum size of seats for a choice. If any of these is missing, importing the csv file will not work. 

Survey response view, where the daycare, etc., fills in their information.
<img src="/static/images/csv-reply-view.png" alt="Vastausnäkymä käyttäjälle">

In the first three fields, the name doesn't matter (Daycare name, name, ID, etc., or capacity, maximum capacity, etc., are all fine, and min_size, minimum size, etc.), as long as the order is correct.

Responding to the above survey will produce a CSV file, which can be found in the Form Report section of Elomake.
<img src="/static/images/csv-report-view.png" alt="Lomakeraportti">

<strong>The first two columns are unnecessary (Tall.id, Tallennusaika), so remove them from the created .csv file.</strong> 

## Other
The only mandatory fields are the name of the facility, capacity, and the minimum size of groups. The delimiter in the .csv file doesn't matter (it can be ,, ;, or "," etc.), as the Separator will automatically change them to ;. The image below shows the format of an example file:
<img src="/static/images/csv.png" alt="Esimerkki csv-tiedosto">