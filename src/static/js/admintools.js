function postDatabaseResetRequest() {
    newDbSchema = document.getElementById('schema-field').value
    console.log(newDbSchema)

    var requestData = {
        schema: newDbSchema
    }

    $.ajax({
        type: "POST",
        url: "/api/admintools/reset",
        data: JSON.stringify(requestData),
        contentType: "application/json",
        dataType: "json",
        success: function(result) {
            console.log(result)
        }
        }); 
}
console.log("ASD")
resetDbSubmitBtn = document.getElementById('db-reset-btn')
resetDbSubmitBtn.addEventListener("click", postDatabaseResetRequest)