function parseObjFromRow(row) {
    var cells = Array.from(row.getElementsByTagName('td'))
    
    return {
        choiceName: cells[0].innerText,
        choiceMaxSpaces: cells[1].innerText,
        choiceInfo1: cells[2].innerText,
        choiceInfo2: cells[3].innerText
    }
}

function createNewSurvey() {
    console.log("createNewSurvey()")
    
    var choiceTableRows = Array.from(document.querySelectorAll("#choiceTable tr:not(:last-of-type)"))
    var rowsAsJson = choiceTableRows.map(parseObjFromRow)

    var requestData = {
        surveyGroupname: $("#groupname").val(),
        choices: rowsAsJson,
        course_id: "dummy"
    }

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

    var rowContent = 
    `<td class="choice-name">
        <span>tyhjä<span>
    </td>
    <td class="choice-max-spaces">
        <span>tyhjä<span>
    </td>
    `
    newRow.setAttribute('class', 'choice-row not-edited')
    newRow.innerHTML = rowContent
}

function invokeAddColumn() {
    console.log("Hello!")
    var headersRow = document.getElementById("table-headers")
    var addColHeader = document.getElementById("add-column-header")
    //stash inner html, it is returned after new column is created
    var addColHeaderInnerHtml = addColHeader.innerHTML

    var newColField = document.createElement("input");
    var stylingDiv = document.createElement("div");
    
    newColField.setAttribute('type', 'text');
    newColField.setAttribute('id', 'new-col-name-input')
    stylingDiv.appendChild(newColField)

    addColHeader.removeAttribute('onclick')
    addColHeader.setAttribute('class', 'edited')

    addColHeader.innerHTML = stylingDiv.outerHTML

    newColField = document.getElementById('new-col-name-input')
    newColField.addEventListener(
        'focusout', function() {finishAddColumn(evt, addColHeaderInnerHtml)}, false )
    newColField.focus()
}

function finishAddColumn(evt, addColumnHeader) {
    console.log(evt)
    console.log(addColumnHeader)

    var headersRow = document.getElementById("table-headers")
    var addColHeader = document.getElementById("add-column-header")
    headersRow.insertBefore(newCol, addColHeader)
}

function editRow(element) {
    document.getElementById('newRow').classList.remove('editable')
    var rowToEdit = element.parentNode.parentNode
    rowToEdit.classList.add('editable')
    rowToEdit.classList.remove('not-edited')
    choiceNameTd = rowToEdit.querySelector(".choice-name")
    choiceMaxSpacesTd = rowToEdit.querySelector(".choice-max-spaces")
    choiceInfo1Td = rowToEdit.querySelector(".choice-info1")
    choiceInfo2Td = rowToEdit.querySelector(".choice-info2")
    choiceEditBtnTd = rowToEdit.querySelector(".choice-edit-btn")

    choiceNameTd.innerHTML = `<input type="text" id="choiceNameEditedRow" value="${choiceNameTd.innerText}" />`
    choiceMaxSpacesTd.innerHTML = `<input type="number" id="choiceMaxSpacesEditedRow" value="${choiceMaxSpacesTd.innerText}" />`
    choiceInfo1Td.innerHTML = `<textarea id="choiceInfo1EditedRow">${choiceInfo1Td.innerText}</textarea>`
    choiceInfo2Td.innerHTML = `<textarea id="choiceInfo2EditedRow">${choiceInfo2Td.innerText}</textarea>`
    choiceEditBtnTd.innerHTML = `<button onclick="applyRowEdit(this)">apply</button>`

    toggleEditRowElements()
}

function applyRowEdit(element) {
    var rowToEdit = element.parentNode.parentNode
    rowToEdit.classList.remove('editable')

    choiceNameTd = rowToEdit.querySelector(".choice-name")
    choiceMaxSpacesTd = rowToEdit.querySelector(".choice-max-spaces")
    choiceInfo1Td = rowToEdit.querySelector(".choice-info1")
    choiceInfo2Td = rowToEdit.querySelector(".choice-info2")
    choiceEditBtnTd = rowToEdit.querySelector(".choice-edit-btn")

    var rowContent = 
    `<td class="choice-name">
        ${ $(choiceNameTd.querySelector(":first-child")).val()}
    </td>
    <td class="choice-max-spaces">
        ${ $(choiceMaxSpacesTd.querySelector(":first-child")).val()}
    </td>
    <td class="choice-info1">
        ${ $(choiceInfo1Td.querySelector(":first-child")).val()}
    </td>
    <td class="choice-info2">
        ${ $(choiceInfo2Td.querySelector(":first-child")).val()}
    </td>
    <td class="choice-edit-btn">
        <button onclick="editRow(this)">edit</button>
    </td>
    `

    rowToEdit.innerHTML = rowContent
    document.getElementById('newRow').classList.add('editable')
    toggleEditRowElements()
}

function toggleEditRowElements() {
    var editRowElements = document.querySelectorAll("#newRow .new-row-input")
    editRowElements.forEach(elem => {elem.disabled = (elem.disabled?false:true)})

    var otherRowsEditBtns = document.querySelectorAll(".not-edited .choice-edit-btn>button")
    otherRowsEditBtns.forEach(elem => {elem.disabled = (elem.disabled?false:true)})
}