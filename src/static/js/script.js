window.onload = function() {
    console.log('Hello from src/static/js/script.js')
};

function submit() {
    var choiceIDs = $("#sortable1").sortable("toArray");
    const formData = new FormData();
    formData.append("choices", choiceIDs);
    
    const xhr = new XMLHttpRequest();
    xhr.open("POST","/get_choices",true);
    xhr.send(formData);
}