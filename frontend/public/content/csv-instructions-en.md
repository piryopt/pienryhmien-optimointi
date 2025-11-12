# A guide for creating surveys with a csv file

It is possible to import survey choices from a CSV file, as long as the file follows the following set of rules. CSV stands for "Comma-Separated Values". In short, a CSV-file stores tabular information, with values seperated by some character (typically a comma is used).

In this case, the seperator in the CSV-file doest not matter (it can be , or ; etc.). The file must at minimun contain name, capacity and minimum group size for each choice. The first row of the file must be a header row.</br>

The image below shows the format of an example file:</br>
<img src="http://localhost:5001/static/images/csv.png" alt="Example CSV-file" class="md-image-small">
</br></br>
<img src="http://localhost:5001/static/images/csv-create.png" alt="Resulting survey" class="md-image-small">
</br></br>

By default, unpopular groups that dont meet the minimum size after distribution will be dropped. If you want to make sure that certaing groups are not dropped, you can add a column called "Mandatory" to the CSV file and fill it with values TRUE or FALSE depending on whether the group is required or not. The values in the "Mandatory" column can be for example TRUE, true, or True, the letter case does not matter. A FALSE value is not strictly required, but each row in the column must contain some value (for example, empty quotation marks " " are acceptable).

The image below shows the format of an example file that has the mandatory column:
<img src="http://localhost:5001/static/images/csv2.png" alt="Example CSV-file">
</br></br>
<img src="http://localhost:5001/static/images/csv2-create.png" alt="Resulting survey" class="md-image-small">

## When using E-lomake

When creating a survey through Elomake, the first field must be the name of the choice, the second field must be the amount of seats available in the choice and the third field must be the minimum size of seats for a choice. If any of these is missing, importing the csv file will not work.

Survey response view, where the daycare, etc., fills in their information.
<img src="http://localhost:5001/static/images/csv-reply-view.png" alt="Vastausnäkymä käyttäjälle">

In the first three fields, the name doesn't matter (Daycare name, name, ID, etc., or capacity, maximum capacity, etc., are all fine, and min_size, minimum size, etc.), as long as the order is correct.

Responding to the above survey will produce a CSV file, which can be found in the Form Report section of Elomake.
<img src="http://localhost:5001/static/images/csv-report-view.png" alt="Lomakeraportti">

<strong>The first two columns are unnecessary (Tall.id, Tallennusaika), so remove them from the created .csv file.</strong>
