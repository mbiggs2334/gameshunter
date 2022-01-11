//sets the TextArea height to auto adjust on input
document.getElementById('report_message').addEventListener('input', () => {
    $("textarea").each(function () {
        this.setAttribute("style", "height:" + (this.scrollHeight) + "px;overflow-y:hidden;");
        }).on("input", function () {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + "px";
    });
    textArea.style.resize = 'vertical';
    textArea.style.maxHeight = '275px';
});
let textArea = document.querySelector('textarea');
textArea.style.resize = 'vertical';
textArea.style.maxHeight = '275px';