function addQuestion(event){
    let newQuestion;

    let amount = document.getElementById("question_amount").value
    document.getElementById("title").value = "ПРиет"
    newQuestion = document.createElement("div");
    newQuestion.className = 'question';
    newQuestion.id = amount
    newQuestion.innerHTML =  "<form>" + '<input type="text" placeholder="Вопрос" name="question' + amount.toString()  + '">'
    newQuestion.innerHTML += '<input type="text" placeholder="Ответ" name="answer'  + amount.toString() + '">' + "</form>";
    newQuestion.insertAfter(document.getElementById("question" + (amount - 1).toString()));
    console.log("hello ");
}



