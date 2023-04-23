const buttonAdd = document.getElementById("adder");
buttonAdd.addEventListener('click', addQuestion)


function addQuestion(){
    let newQuestion;
    let amount = $('.questions').children().length + 1;
    newQuestion = document.createElement("div");
    newQuestion.className = 'question';
    newQuestion.id = amount
    newQuestion.innerHTML =
        "<form>" +
            '<input type="text" placeholder="Вопрос" name="question' +
                toString(amount)  + '">'
            '<input type="text" placeholder="Ответ" name="answer'  +
                    toString(amount) + '">' +
        "</form>";
    newQuestion.insertAfter(document.getElementById(amount - 1));
    console.log("hello ");
}