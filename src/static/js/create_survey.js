var emptyCellText = "tyhjä"

function parseObjFromRow(row, headers) {
    var cells = Array.from(row.getElementsByTagName('td'))
    obj = {}

    for (var i=0; i < headers.length;i++) {
        obj[headers[i]] = cells[i].innerText
    }

    return obj
}

function validateChoiceTable() {
    Array.from(document.querySelectorAll("#choiceTable td")).forEach( cell => {
        cellIsValid(cell)
    })
}



function cellIsValid(elem) {
    var cellIndex = elem.cellIndex
    var colHeader = document.querySelector(`#choice-table-headers th:nth-child(${cellIndex + 1})`)
    var pattern = colHeader.getAttribute("col-validation-regex")
    if(!pattern) { return true }

    var cellText = elem.classList.contains("empty") ? "": elem.innerText
    var colWarningItemId = `col-${cellIndex}-validation-warning`
    var warningsList = document.getElementById("choicetable-validation-warnings")

    if (!isExactMatch(pattern, cellText)){
        elem.classList.add("active-warning")
        if(!document.getElementById(colWarningItemId)) {
            var newWarning = document.createElement("li")
            newWarning.setAttribute("id", colWarningItemId)
            newWarning.classList.add("input-validation-warning")
            newWarning.innerText = `Sarakkeen "${colHeader.innerText}" arvojen tulee olla ${colHeader.getAttribute("validation-text")}`
            warningsList.appendChild(newWarning)
            
            warningsList.classList.remove("hidden")
        }
        return false
    } else {
        var warningItem = document.getElementById(colWarningItemId)
        if(warningItem !== null) {
            warningItem.remove()
            if(!warningsList.hasChildNodes) {
                warningsList.classList.add("hidden")
            }
        }
    }
}


function toggleClass(elem, classname) {
    if(elem.classList.contains(classname)) { elem.classList.remove(classname)}
    else {elem.classList.add(classname)}
}


function isExactMatch(pattern, string) {
    var regexMatches = string.match(new RegExp(pattern))
    return !regexMatches ?  false : regexMatches[0] === string
}

function fieldIsValid(elem) {
    if(!isExactMatch(elem.getAttribute("validation-regex"), elem.value)) {
        setValidationErrorMsg(elem)
        return false
    }

    if (elem.classList.contains('active-warning')) {
        removeValidationErrorMsg(elem)
    }

    return true
}

function removeValidationErrorMsg(elem) {
    elem.classList.remove("active-warning")
    var fieldName = elem.getAttribute('name')
    var warningTextElement = document.querySelector(`#${fieldName}-validation-warning`)
    warningTextElement.classList.add("hidden")
    warningTextElement.parentElement.parentElement.classList.add("hidden")
}

function setValidationErrorMsg(elem) {
    // Expects that every field that can raise validation error has a corresponding
    // span element with id matching "#${fieldName}-validation-warning" -scheme
    elem.classList.add("active-warning")
    elem.classList.remove("hidden")
    var fieldName = elem.getAttribute("name")
    
    var alertMsg = elem.getAttribute("validation-text") ? elem.getAttribute("validation-text") : "Jokin meni pieleen! Tarkasta kenttien sisältö"
    var warningTextContainer = document.querySelector(`#${fieldName}-validation-warning`)
    
    if(!warningTextContainer) {
        showAlert({msg: alertMsg, color:"red"})
    }

    warningTextContainer.innerText = alertMsg
    warningTextContainer.classList.add("active-warning")
    warningTextContainer.classList.remove("hidden")
    warningTextContainer.parentElement.parentElement.classList.remove('hidden')
}

function createNewSurvey() {
    // Front-end Validatation of fields
        // Validate choice table
        validateChoiceTable()

        // Validate single fields
    var elementsToValidate = document.querySelectorAll("input[validation-regex]:not(.hidden)")
    var validContent = true

    elementsToValidate.forEach(elem => {
        console.log(elem)
        if(!fieldIsValid(elem)) {
            validContent = false
        }
    })

    if (!validContent) {
        // Not valid, won't try to post
        console.log("Form contents not valid, won't post")
        return;
    }


    //Valid content, continue to post

    // Get column names from the choice table
    var tableHeaders = Array.from(document.querySelectorAll("#choice-table-headers th:not(:last-of-type)")).map(elem => elem.innerText)
    console.log(tableHeaders)

    var tableRows = Array.from(document.querySelectorAll("#choiceTable tr"))
    var rowsAsJson = tableRows.map(function(x) { return parseObjFromRow(x, tableHeaders) })
    var minChoicesElement = document.getElementById("minchoices")
    var allowedDeniedChoices = document.getElementById("denied-choices-count")

    var startDateParts = document.getElementById("start-date").value.split(".")
    var endDateParts = document.getElementById("end-date").value.split(".")
    var endDate = new Date(Number(endDateParts[2]), Number(endDateParts[1]-1), Number(endDateParts[0]))
    var startDate = new Date(Number(startDateParts[2]), Number(startDateParts[1]-1), Number(startDateParts[0]))
    
    if(endDate < startDate) {
        showAlert({msg: "Vastausaika ei saa päättyä ennen vastausajan alkua", color: "red"})
        return;
    }
    var today = new Date()
    var todaysEnd = new Date(today.getFullYear(), today.getMonth(), today.getDate(),23,59)
    if(endDate <= todaysEnd) {
        showAlert({msg: "Vastausajan päättymispäivä ei saa olla kuluva päivä tai menneisyydessä", color: "red"})
        return;
    }

    var requestData = {
        surveyGroupname: $("#groupname").val(),
        choices: rowsAsJson,
        surveyInformation: document.getElementById("survey-information").value,
        startdate: document.getElementById("start-date").value,
        starttime: document.getElementById("starttime").value,
        enddate: document.getElementById("end-date").value,
        endtime: document.getElementById("endtime").value,
        minchoices: minChoicesElement.classList.contains("hidden") ? rowsAsJson.length : Number(minChoicesElement.value),
        allowedDeniedChoices: allowedDeniedChoices.classList.contains("hidden") ? 0 : Number(allowedDeniedChoices.value),
        allowSearchVisibility: document.getElementById("search-visibility-yes").checked
    }

    console.log("requestData", requestData)

    $.ajax({
    type: "POST",
    url: "/surveys/create",
    data: JSON.stringify(requestData),
    contentType: "application/json",
    dataType: "json",
    success: function(result) {
        var alertMsg = {
            msg: result.msg,
            color: ""
        }
        if (result.status === "1") {
            alertMsg.color = "#216620";
        }
        if (result.status === "0") {
            alertMsg.color = "#9c2b2e";
        }
        showAlert(alertMsg);
    }
    }); 
}

function saveEdit() {
    // Front-end Validatation of fields
        // Validate choice table
        validateChoiceTable()

        // Validate single fields
    var elementsToValidate = document.querySelectorAll("[validation-regex]")
    var validContent = true

    elementsToValidate.forEach(elem => {
        if(!fieldIsValid(elem)) {
            validContent = false
        }
    })

    if (!validContent) {
        // Not valid, won't try to post
        console.log("Form contents not valid, won't post")
        return;
    }

    //Valid content, continue to post

    // Get column names from the choice table
    //var tableHeaders = Array.from(document.querySelectorAll("#choice-table-headers th:not(:last-of-type)")).map(elem => elem.innerText)

    //var tableRows = Array.from(document.querySelectorAll("#choiceTable tr"))
    //var rowsAsJson = tableRows.map(function(x) { return parseObjFromRow(x, tableHeaders) })

    var surveyID = document.getElementById("survey_id").value;

    var requestData = {
        surveyGroupname: $("#groupname").val(),
        //choices: rowsAsJson,
        surveyInformation: document.getElementById("survey-information").value,
        startdate: document.getElementById("start-date").value,
        starttime: document.getElementById("starttime").value,
        enddate: document.getElementById("end-date").value,
        endtime: document.getElementById("endtime").value,
    }

    console.log("requestData", requestData)

    $.ajax({
    type: "POST",
    url: "/surveys/" + surveyID + "/edit",
    data: JSON.stringify(requestData),
    contentType: "application/json",
    dataType: "json",
    success: function(result) {
        var alertMsg = {
            msg: result.msg,
            color: ""
        }
        if (result.status === "1") {
            alertMsg.color = "#216620";
        }
        if (result.status === "0") {
            alertMsg.color = "#9c2b2e";
        }
        showAlert(alertMsg);
    }
    });
}

function saveGroupSizes() {

    // Get column names from the choice table
    var tableHeaders = Array.from(document.querySelectorAll("#choice-table-headers th:not(:last-of-type)")).map(elem => elem.innerText)
    console.log(tableHeaders)

    var surveyID = document.getElementById("survey_id").value
    var tableRows = Array.from(document.querySelectorAll("#choiceTable tr"))
    var rowsAsJson = tableRows.map(function(x) { return parseObjFromRow(x, tableHeaders) })
    var requestData = {
        surveyGroupname: $("#groupname").val(),
        choices: rowsAsJson,
    }

    console.log("requestData", requestData)

    $.ajax({
    type: "POST",
    url: "/surveys/"+surveyID+"/group_sizes",
    data: JSON.stringify(requestData),
    contentType: "application/json",
    dataType: "json",
    success: function(result) {
        var alertMsg = {
            msg: result.msg,
            color: ""
        }
        if (result.status === "1") {
            alertMsg.color = "#216620";
        }
        if (result.status === "0") {
            alertMsg.color = "#9c2b2e";
        }
        showAlert(alertMsg);
    },
    error: function(result) {
        if (result.responseJSON) {
            showAlert({msg: result.status + ": " + result.responseJSON.msg, color: "red"})
        } else {
            showAlert({msg: `Jokin meni vikaan, palvelimeen ei saatu yhteyttä`, color: "red"})
        }
    
    }
    }); 
}

function addRow() {
    var newRow = document.getElementById("choiceTable").insertRow()

    headers = document.querySelectorAll("#choice-table-headers th:not(#add-column-header)")
    headers.forEach( _ => {
        newRow.appendChild(createEmptyInputCell())
    })

    newRow.appendChild(createDeleteRowCell())
}

function addCellEventListeners(cellElem) {
    cellElem.addEventListener("click", editCell)
    cellElem.addEventListener("keydown", enterKeypressOnFocucedCell)
}


function enterKeypressOnFocucedCell(event) {
    if(event.key === "Enter" && $(event.target).is(":focus")) {
        editCell(event)
    }
}

function enterKeyPressOnEditedCell(event) {
    var parent_tag = event.target.parentNode.tagName
    if(event.key === "Enter" && parent_tag === "TD") {
        submitCell(event)
    } else if (event.key === "Enter" && parent_tag === "TH") {
        submitNewColumn(event)
    }
}

function showDeleteColumnIconOnHover(event){
    var columnIndex = event.target.cellIndex
    if(columnIndex > 2) {
        var columnDeleteBtn = document.querySelector(`#column-delete-btns td:nth-child(${columnIndex + 1})`)
        columnDeleteBtn.classList.add("visible")
        columnDeleteBtn.querySelector(".delete-col-btn").classList.add("delete-col-btn-visible")
    }
}

function createDeleteColumnCell() {
    var cell = document.createElement('td')
    var btn = document.createElement('div')
    btn.classList.add('delete-col-btn')
    cell.appendChild(btn)
    btn.addEventListener("click", removeColumn)
    return cell
}

function removeColumn(event) {
    var cellIndex = event.target.parentElement.cellIndex
    var rows = document.querySelector(".choice-table-main").querySelectorAll("tr")
    Array.from(rows).forEach(row => {
        row.querySelector(`td:nth-child(${cellIndex + 1}), th:nth-child(${cellIndex + 1})`).remove()
    })
}

function createEmptyInputCell() {
    var newEmptyCell = document.createElement("td")
    newEmptyCell.classList.add("empty")
    newEmptyCell.setAttribute("tabindex", "0")
    newEmptyCell.innerHTML = emptyCellText
    addCellEventListeners(newEmptyCell)

    return newEmptyCell
}

function createDeleteRowCell() {
    var actionCell = document.createElement("td")
    actionCell.classList.add("action-cell")
    var deleteBtn = document.createElement("div")
    deleteBtn.classList.add("delete-row-btn")
    actionCell.appendChild(deleteBtn)
    deleteBtn.addEventListener("click", deleteRow)

    return actionCell
}


function createAddColumnHeader() {

    var newAddColumnHeader = createElementWithText("th", "+ Lisää tietokenttä", editCell)
    newAddColumnHeader.setAttribute("id", "add-column-header")
    newAddColumnHeader.setAttribute("class", "variable-header")

    return newAddColumnHeader
}


function editCell(event) {
    var editableField = document.createElement("input");
    editableField.setAttribute('type', 'text');

    // if edited cell is not the "add new column" header, edit the current content 
    // special cases for "add new column" header and empty cell to not keep old value
    if (event.target.id !== "add-column-header" && !event.target.classList.contains("empty")) {
        editableField.value = event.target.innerText    
    }

    event.target.innerText = ""
    event.target.setAttribute('class', 'edited')
    event.target.appendChild(editableField)

    // Special event handler for "add new column" header
    if (event.target.id !== "add-column-header") {
        editableField.addEventListener("focusout", submitCell)
        editableField.addEventListener("keydown", enterKeyPressOnEditedCell)
    } else {
        editableField.addEventListener("focusout", submitNewColumn)
        editableField.addEventListener("keydown", enterKeyPressOnEditedCell)
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
        editedCell.innerText = "+ Lisää tietokenttä"
        return
    }

    // Case: New column has a name
    //  -->: Change name of the column, remove id
    editedCell.removeAttribute("id")
    editedCell.addEventListener("mouseover",showDeleteColumnIconOnHover)

    //  -->: Set header value to what was given to the input field
    editedCell.innerHTML = ""
    editedCell.innerText = newValue
    editedCell.addEventListener("mouseover",showDeleteColumnIconOnHover)

    //add delete button for new column
    document.querySelector("#column-delete-btns").appendChild(createDeleteColumnCell())
    
    
    if (!document.getElementById("add-column-header")){
        // -->: Create new "Add new column" header to the table if it does not exist anymore
        document.getElementById("choice-table-headers").appendChild(createAddColumnHeader())

        // -->: Add a new cell matching the header to all existing rows in the table
        Array.from(document.querySelectorAll('#choiceTable tr')).forEach(row => {
            row.insertBefore(createEmptyInputCell(), row.querySelector(".action-cell"))
        })
    }
    
}


function submitCell(event) {
    var newValue = event.target.value
    var editedCell = event.target.parentNode
    var wasEmpty = editedCell.classList.contains("empty")
    editedCell.classList.remove("edited")
    editedCell.innerHTML = ""
    
    if (newValue === '' && !wasEmpty) {
        editedCell.innerText = emptyCellText
        editedCell.classList.add("empty")
    } else {
        editedCell.innerText = newValue
        if (wasEmpty) {
            editedCell.classList.remove("empty")
        }
    }
    cellIsValid(editedCell)
}

function deleteRow(event) {
    event.target.closest('tr').remove()
}

function pageLoadActions() {
    var choiceTable = document.getElementById("choiceTable")

    // Add onClick event to all regular table cells
    var cells = choiceTable.getElementsByTagName("td")
    for (var cell of cells) {
        addCellEventListeners(cell)
    }

    // add onClick event to all delete row-buttons
    var deleteRowBtns = choiceTable.getElementsByClassName("delete-row-btn")
    Array.from(deleteRowBtns).forEach(btn => {
        btn.addEventListener("click", deleteRow)
    })

    // Add onClick event to "add new column" -header
    var addColHeader = document.getElementById("add-column-header")
    addColHeader.addEventListener("click", editCell)

    //Check for existing custom headers
    var variableHeaders = document.querySelectorAll('#choice-table-headers th:not(.constant-header, #add-column-header)')
    variableHeaders.forEach( header => {
        header.addEventListener("mouseover",showDeleteColumnIconOnHover)
    } )
    document.querySelectorAll('.delete-col-btn').forEach(btn => {
        btn.addEventListener("click", removeColumn)
    })
}

document.addEventListener("DOMContentLoaded",function() {
   pageLoadActions() 
})

function uploadChoiceFileBtn() {
    document.getElementById("choiceFileInput").click()
}

function handleFileUpload() {
    var uploadInput = document.getElementById("choiceFileInput")
    var file = uploadInput.files[0]
    var reader = new FileReader()
    reader.readAsText(file)
    reader.onload = function() {
        // Validate file and handle uploading it to backend

        var requestData = {
            surveyGroupname: $("#groupname").val(),
            surveyInformation: document.getElementById("survey-information").value,
            uploadedFileContent: reader.result
        }

        $.ajax({
            type: "POST",
            url: "/surveys/create/import",
            data: JSON.stringify(requestData),
            contentType: "application/json",
            dataType: "json",
            success: function(result) {
                setUploadedTableValues(result)
            }
            }); 

    }
    
}

function visibilityToggleRadioClick(event) {
    if(event.target.value === "show") {
        Array.from(document.querySelectorAll(`.${event.target.getAttribute("data-dependant-class")}`)).forEach(element => {
            element.classList.remove("hidden")
        })
    } else if(event.target.value === "hide") {
        Array.from(document.querySelectorAll(`.${event.target.getAttribute("data-dependant-class")}`)).forEach(element => {
            element.classList.add("hidden")
        })
    }

}

function setUploadedTableValues(table) {
    var headersRow = document.getElementById('choice-table-headers')
    // Remove variable columns if they exist
    var begin = (headersRow.childElementCount-3)*-1
    var end = headersRow.childElementCount - 1
    var variableHeaders = Array.from(headersRow.children).slice(begin, end)
    variableHeaders.forEach(header => header.remove())

    // Add new headers if they exist
    // TODO: Correct naming
    var headers = Object.keys(table[0])
    var headers = Object.keys(table[0]).filter(header => header !== 'name' && header !== 'spaces' && header !== 'min_size')

    var deleteColRow = document.getElementById("column-delete-btns")

    for(var header of headers) {
        deleteColRow.appendChild(createDeleteColumnCell())
        var newHeader = createElementWithText('th', header, clickHandler=editCell)
        newHeader.addEventListener("mouseover",showDeleteColumnIconOnHover)
        headersRow.insertBefore(newHeader, document.getElementById('add-column-header'))
    }
    // This fixes bug where the last column couldn't be deleted
    deleteColRow.appendChild(createDeleteColumnCell())

    // set table body
    var tableBody = document.getElementById('choiceTable')
    tableBody.innerHTML = ''
    
    table.forEach(row => {
        var rowElement = document.createElement('tr')
        addCellEventListeners(rowElement.appendChild(createElementWithText('td', row['name'])))
        addCellEventListeners(rowElement.appendChild(createElementWithText('td', row['spaces'])))
        addCellEventListeners(rowElement.appendChild(createElementWithText('td', row['min_size'])))

        headers.forEach( header => {
                addCellEventListeners(rowElement.appendChild(createElementWithText('td', row[header])))
            }   
        )
        rowElement.appendChild(createDeleteRowCell())
        tableBody.append(rowElement)
    })
}

function createElementWithText(type, content, clickHandler=null) {
    var element = document.createElement(type)
    element.innerText = content

    if(clickHandler) {
        element.addEventListener("click", clickHandler)
    }

    return element
}