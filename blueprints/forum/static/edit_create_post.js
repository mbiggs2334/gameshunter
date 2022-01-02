$("textarea").each(function () {
    this.setAttribute("style", "height:" + (this.scrollHeight) + "px;overflow-y:hidden;");
    }).on("input", function () {
    this.style.height = "auto";
    this.style.height = (this.scrollHeight) + "px";
});

let backButton = document.getElementById('backBtn')
backButton.addEventListener('click', () => {
    window.history.go(-1); 
    return false;
});

let textArea = document.querySelector('textarea')
    textArea.style.resize = 'vertical';
    textArea.style.maxHeight = '500px';
    textArea.style.whiteSpace = 'pre-wrap';

$('form').addEventListener('submit', () => {
    textArea.value.trim()
})