window.onload = function() {
    console.log('Hello from src/static/js/script.js')
};

function submit(resubmit) {
    var maxBadChoices = document.getElementById("max_bad_choices").value;
    var surveyID = document.getElementById("survey_id").value;
    var neutralIDs = $("#sortable-neutral").sortable("toArray");
    var goodIDs = $("#sortable-good").sortable("toArray");
    var badIDs = [];
    var reasons = "";

    if (maxBadChoices > 0) {
        var badIDs = $("#sortable-bad").sortable("toArray");
        var reasons = document.getElementById("reasons").value;
    }

    var IDs = {
        "neutralIDs": neutralIDs,
        "goodIDs": goodIDs,
        "badIDs": badIDs,
        "allIDs": neutralIDs.concat(goodIDs,badIDs),
        "reasons": reasons
    }

    $.ajax({
    type: "POST",
    url: "/get_choices/" + surveyID,
    data: JSON.stringify(IDs),
    contentType: "application/json",
    dataType: "json",
    success: function(result) {
        var alertMsg = {
            msg: result.msg,
            color: ""
        }
        if (result.status === "1") {
            alertMsg.color = "#216620";
            if (resubmit === 1) {
                $("#submitExists").toggle();
                $("#submitDoesntExist").toggle();
                $("#deleteContainer").toggle();
            }
        }
        if (result.status === "0") {
            alertMsg.color = "#9c2b2e";
        }
        showAlert(alertMsg);   
    }
    });
}

function showAlert(props) {
    var alertContainer = document.getElementById("message");
    var fade = document.getElementById("fade");

    alertContainer.style.display = "block";
    alertContainer.innerHTML = props.msg;
    fade.style.backgroundColor = props.color;
    if (fade.style.display === "none") {
        fade.style.display = "block";
    }
    $("#fade").delay(3000).fadeOut(500);
}

function deleteSubmission() {
    var surveyID = document.getElementById("survey_id").value;

    $.ajax({
        type: "POST",
        url: "/surveys/" + surveyID + "/deletesubmission",
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
            $("#submitExists").hide();
            $("#submitDoesntExist").show();
            $("#deleteContainer").hide()
            $("#confirmContainer").hide()
            
        }
    });
}

function add_teacher() {
    var surveyID = document.getElementById("survey_id").value;
    var teacherEmail = document.getElementById("teacher_email").value

    $.ajax({
        type: "POST",
        url: "/surveys/" + surveyID + "/edit/add_teacher/" + teacherEmail,
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

function showMoreInfo(choiceID) {
    var infoContainer = document.getElementById("info-container");
    var currentlySelected = document.getElementById("currently_selected").value;

    if (currentlySelected === "") {
        $.ajax({
            type: "POST",
            url: "/surveys/getinfo",
            data: JSON.stringify(choiceID),
            contentType: "application/json",
            datatype: "html",
            success: function(result) {
                infoContainer.innerHTML = result;
                $('input[id="currently_selected"]').val(choiceID);
            }
        });
    }
    
    if (currentlySelected != choiceID) {
        $.ajax({
            type: "POST",
            url: "/surveys/getinfo",
            data: JSON.stringify(choiceID),
            contentType: "application/json",
            dataType: "html",
            success: function(result) {
                infoContainer.innerHTML = result;
                $('input[id="currently_selected"]').val(choiceID);
            }
        });
    } else {
        exitMoreInfo();
    }
}

function exitMoreInfo() {
    document.getElementById("info-container").innerHTML = "<p>Klikkaa valintavaihtoehtoa nähdäksesi siitä lisätietoa.</p>";
    $('input[id="currently_selected"]').val("");
}
