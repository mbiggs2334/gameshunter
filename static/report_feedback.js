$("textarea").each(function () {
    this.setAttribute("style", "height:" + (this.scrollHeight) + "px;overflow-y:hidden;");
    }).on("input", function () {
    this.style.height = "auto";
    this.style.height = (this.scrollHeight) + "px";
});

let textArea = document.querySelector('textarea');
textArea.style.resize = 'vertical';
textArea.style.maxHeight = '500px';