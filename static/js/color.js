function changeColor(color) {
    var note = document.getElementById("note");
    var text = document.getElementById("text-area");
    var title = document.getElementById("note-name");
    note.style.backgroundColor = color;
    text.style.backgroundColor = color;
    title.style.backgroundColor = color;
}