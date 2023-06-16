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

function addChoice() {
    var newChoice = {
        choiceName: $("#choiceName").val(),
        choiceMaxSpaces: $("#choiceMaxSpaces").val(),
        choiceInfo1: $("#choiceInfo1").val(),
        choiceInfo2: $("#choiceInfo2").val()
    }

    var choiceTable = document.getElementById("choiceTable")
    var newRow = choiceTable.insertRow(choiceTable.rows.length - 1 )

    var rowContent = 
    `<td class="choice-name">
        ${newChoice['choiceName']}
    </td>
    <td class="choice-max-spaces">
        ${newChoice['choiceMaxSpaces']}
    </td>
    <td class="choice-info1">
        ${newChoice['choiceInfo1']}
    </td>
    <td class="choice-info2">
        ${newChoice['choiceInfo2']}
    </td>
    <td class="choice-edit-btn">
        <button onclick="editRow(this)">edit</button>
    </td>
    `
    newRow.setAttribute('class', 'choice-row not-edited')
    newRow.innerHTML = rowContent

    $("#choiceName").val(""),
    $("#choiceMaxSpaces").val(""),
    $("#choiceInfo1").val(""),
    $("#choiceInfo2").val("")
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