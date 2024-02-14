window.onload = function() {
    console.log('Hello from src/static/js/script.js')
};

function submit(resubmit) {
    var maxBadChoices = document.getElementById("max_bad_choices").value;
    var minChoices = document.getElementById("min_choices").value;
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
        "minChoices": minChoices,
        "maxBadChoices": maxBadChoices,
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
    $("#fade").delay(5000).fadeOut(500);
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

function add_owner() {
    var surveyID = document.getElementById("survey_id").value;
    var email = document.getElementById("email").value

    $.ajax({
        type: "POST",
        url: "/surveys/" + surveyID + "/edit/add_owner/" + email,
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

function add_feedback() {
    var title = document.getElementById("title").value;
    var type = document.getElementById("type").value;
    var content = document.getElementById("content").value;
    console.log(title, type, content)

    var data = {
        "title": title,
        "type":type,
        "content":content
    }

    $.ajax({
        type: "POST",
        url: "/feedback",
        data: JSON.stringify(data),
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

function showMoreInfo(choiceID) {
    var name = "info-container " + choiceID
    var infoContainer = document.getElementById(name);
    var currentlySelected = document.getElementById("currently_selected").value;
    var additional_info = document.getElementById("additional_info").value;

    if (additional_info === "False") {
        return
    }

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
    
    else if (currentlySelected != choiceID) {
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
        exitMoreInfo(choiceID);
    }
}

function exitMoreInfo(choiceID) {
    var name = "info-container " + choiceID
    document.getElementById(name).innerHTML = "";
    $('input[id="currently_selected"]').val("");
}

function showRankingResults(email) {
    var surveyID = document.getElementById("survey_id").value;
    var name = "all-rankings-container " + email
    var rankingContainer = document.getElementById(name)
    var currentlySelected = document.getElementById("currently_selected").value
    if (currentlySelected === "") {
        $.ajax({
            type: "POST",
            url: "/surveys/" + surveyID + "/studentranking",
            data: JSON.stringify(email),
            contentType: "application/json",
            datatype: "html",
            success: function(result) {
                rankingContainer.innerHTML = result;
                $('input[id="currently_selected"]').val(email);
            }
        });
    }
    else if (currentlySelected != email) {
        $.ajax({
            type: "POST",
            url: "/surveys/" + surveyID + "/studentranking",
            data: JSON.stringify(email),
            contentType: "application/json",
            datatype: "html",
            success: function(result) {
                rankingContainer.innerHTML = result;
                $('input[id="currently_selected"]').val(email);
            }
        });
    } else {
        exitMoreRankingResults(email);
    }
}

function exitMoreRankingResults(email) {
    var name = "all-rankings-container " + email
    document.getElementById(name).innerHTML = "";
    $('input[id="currently_selected"]').val("");
}
