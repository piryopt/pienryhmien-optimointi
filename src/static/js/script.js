window.onload = function() {
    console.log('Hello from src/static/js/script.js')
};

function submit(resubmit) {
    var choiceIDs = $("#sortable1").sortable("toArray");
    var alertContainer = document.getElementById("message");
    var surveyID = document.getElementById("survey_id").value;
    alertContainer.style.display = "block";


    $.ajax({
    type: "POST",
    url: "/get_choices/" + surveyID,
    data: JSON.stringify(choiceIDs),
    contentType: "application/json",
    dataType: "json",
    success: function(result) {
        alertContainer.innerHTML = result.msg;
        var fade = document.getElementById("fade");
        if (result.status === "1") {
            fade.style.backgroundColor = "#6F0";
        }
        if (result.status === "0") {
            fade.style.backgroundColor = "red";
        }
        if (fade.style.display === "none") {
            fade.style.display = "block";
        }
        if (resubmit === 1) {
            $("#submitExists").toggle();
            $("#submitDoesntExist").toggle();
            $("#deleteContainer").toggle();
        }
        $("#fade").delay(3000).fadeOut(500);        
    }
    });
}

function deleteSubmission() {
    var alertContainer = document.getElementById("message");
    var surveyID = document.getElementById("survey_id").value;
    alertContainer.style.display = "block";

    $.ajax({
        type: "POST",
        url: "/surveys/" + surveyID + "/deletesubmission",
        success: function(result) {
            alertContainer.innerHTML = result.msg;
            var fade = document.getElementById("fade");
            if (result.status === "1") {
                fade.style.backgroundColor = "#6F0";
            }
            if (result.status === "0") {
                fade.style.backgroundColor = "red";
            }
            if (fade.style.display === "none") {
                fade.style.display = "block";
            }
            $("#submitExists").hide();
            $("#submitDoesntExist").show();
            $("#deleteContainer").hide()
            $("#confirmContainer").hide()
            
            $("#fade").delay(3000).fadeOut(500);
        }
    })
}