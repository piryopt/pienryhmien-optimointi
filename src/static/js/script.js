window.onload = function() {
    console.log('Hello from src/static/js/script.js')
};

function submit() {
    var choiceIDs = $("#sortable1").sortable("toArray");
    var alertContainer = document.getElementById("message");
    
    alertContainer.style.display = "block";


    $.ajax({
    type: "POST",
    url: "/get_choices",
    data: JSON.stringify(choiceIDs),
    contentType: "application/json",
    dataType: "json",
    success: function(result) {
        alertContainer.innerHTML = result.msg;
        var fade = document.getElementById("fade");
        if (fade.style.display === "none") {
            fade.style.display = "block";
        } else {
        }
        $("#fade").delay(3000).fadeOut(500);
    }
    });
}