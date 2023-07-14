var emptyCellText = "tyhjä"

function parseObjFromRow(row, headers) {
    var cells = Array.from(row.getElementsByTagName('td'))
    console.log("Cells", cells)
    console.log("Headers", headers)
    obj = {}

    for (var i=0; i < headers.length;i++) {
        obj[headers[i]] = cells[i].innerText
    }

    return obj
}

function createNewSurvey() {
    console.log("createNewSurvey()")
    
    // Get column names from the choice table
    var tableHeaders = Array.from(document.querySelectorAll("#table-headers th:not(:last-of-type)")).map(elem => elem.innerText)
    console.log(tableHeaders)

    var tableRows = Array.from(document.querySelectorAll("#choiceTable tr"))
    var rowsAsJson = tableRows.map(function(x) { return parseObjFromRow(x, tableHeaders) })

    var requestData = {
        surveyGroupname: $("#groupname").val(),
        choices: rowsAsJson,
        surveyInformation: document.getElementById("survey-information").value
    }

    console.log(requestData)

    $.ajax({
    type: "POST",
    url: "/create_survey",
    data: JSON.stringify(requestData),
    contentType: "application/json",
    dataType: "json",
    success: function(result) {
        console.log(result)
    }
    }); 
}

function addRow() {
    var choiceTable = document.getElementById("choiceTable")
    var newRow = choiceTable.insertRow(choiceTable.rows.length)

    // Getting the number of columns in the table,
    // Last header is subtracted, it is the add new column one
    headersCount = (document.getElementById("table-headers").getElementsByTagName("th").length) - 1
    
    for (var i = 0; i < headersCount; i++) {
        // create an empty cell and attach event listener to it
        var newEmptyCell = document.createElement("td")
        newEmptyCell.innerHTML = emptyCellText
        newRow.appendChild(newEmptyCell).addEventListener("click", editCell)
    }      
}

function editCell(event) {
    console.log("editCell")
    console.log(event.target)
    var editableField = document.createElement("input");
    editableField.setAttribute('type', 'text');

    // if edited cell is not the "add new column" header, edit the current content 
    // special case for "add new column" header to not keep old value
    if (event.target.id !== "add-column-header") {
        editableField.value = event.target.innerText    
    }

    event.target.innerText = ""
    event.target.setAttribute('class', 'edited')
    event.target.appendChild(editableField)

    // Special event handler for "add new column" header
    if (event.target.id !== "add-column-header") {
        editableField.addEventListener("focusout", submitCell)
    } else {
        editableField.addEventListener("focusout", submitNewColumn)
    }


    editableField.focus()

}

function submitNewColumn(event) {
    var newValue = event.target.value
    var editedCell = event.target.parentNode
    editedCell.classList.remove("edited")

    // Case: New column name was left empty
    //  -->: No new column will be added
    if (event.target.value === "") {
        editedCell.innerHTML = ""
        editedCell.innerText = "+ Lisää sarake"
        return
    }

    // Case: New column has a name
    //  -->: Change name of the column, remove id
    editedCell.removeAttribute("id")

    //  -->: Set header value to what was given to the input field
    editedCell.innerHTML = ""
    editedCell.innerText = newValue

    // -->: Create new "Add new column" header to the table
    var headers = document.getElementById("table-headers")
    var newAddColumnHeader = document.createElement("th")
    newAddColumnHeader.setAttribute("id", "add-column-header")
    newAddColumnHeader.setAttribute("class", "variable-header")
    newAddColumnHeader.innerText = "+ Lisää sarake"
    headers.appendChild(newAddColumnHeader)
    newAddColumnHeader.addEventListener("click", editCell)

    // -->: Add cell matching the header to all existing rows in the table
    var rows = document.getElementById("choiceTable").getElementsByTagName("tr")
    for (var row of rows) {
        var newCell = document.createElement("td")
        newCell.innerText = emptyCellText
        row.appendChild(newCell)
        newCell.addEventListener("click", editCell)
    }
}

function submitCell(event) {
    var newValue = event.target.value
    var editedCell = event.target.parentNode
    editedCell.classList.remove("edited")
    editedCell.innerHTML = ""
    editedCell.innerText = newValue

}

function pageLoadActions() {
    var choiceTable = document.getElementById("choiceTable")

    // Add onClick event to all regular table cells
    var cells = choiceTable.getElementsByTagName("td")
    for (var cell of cells) {
        cell.addEventListener("click", editCell)
    }

    // Add onClick event to "add new column" -header
    var addColHeader = document.getElementById("add-column-header")
    addColHeader.addEventListener("click", editCell)
}

document.addEventListener("DOMContentLoaded",function() {
   pageLoadActions() 
})
