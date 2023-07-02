function addQuestion(event){
    let amount = document.getElementById("cards-count").value
    let newNumber = parseInt(amount) + 1;
    newNumber = newNumber.toString();
    console.log(amount)

    let newTabLink = document.createElement("button")
    newTabLink.className = "tablink";
    newTabLink.innerText = newNumber;
    newTabLink.setAttribute("id", newNumber + "-tab");
    newTabLink.addEventListener("click", switchTab)
    newTabLink.setAttribute("type", "button")

    tablinks.appendChild(newTabLink);

    let newQuestion = document.createElement("div");
    newQuestion.className = "tab-pane fade";
    newQuestion.setAttribute("id", newNumber)
    let newRow = document.createElement("div");
    newRow.className = "question row";
    newRow.setAttribute("id", "question" + newNumber);
    let questionColumn = document.createElement("div")
    questionColumn.className = "col"
    let questionLabel = document.createElement("label");
    questionLabel.setAttribute("for", "question" + newNumber + '-textarea')
    questionLabel.innerText = "Вопрос";
    questionColumn.appendChild(questionLabel)
    let questionTextArea = document.createElement("textarea")
    questionTextArea.className = "form-control";
    questionTextArea.style.height = "160px"
    questionTextArea.setAttribute("name", "questions" + newNumber)
    questionTextArea.setAttribute("id", "question" +  newNumber +"-textarea")
    questionTextArea.setAttribute('placeholder', "Вопрос:")
    questionColumn.appendChild(questionTextArea);
    newRow.appendChild(questionColumn);

    let answerColumn = document.createElement("div");
    answerColumn.className = 'col';

    let answerLabel = document.createElement("label");
    answerLabel.setAttribute("for", answerLabel.for = "answer" + newNumber + '-textarea')
    answerLabel.innerText = "Ответ";
    answerColumn.appendChild(answerLabel)

    let answerTextArea = document.createElement("textarea")
    answerTextArea.className = "form-control"
    answerTextArea.style.height = "160px"
    answerTextArea.setAttribute("name", "answer" + newNumber)
    answerTextArea.setAttribute("id", "answer" +  newNumber +"-textarea")
    answerTextArea.setAttribute('placeholder', "Ответ:")
    answerTextArea.setAttribute("minlength", "1")
    answerColumn.appendChild(answerTextArea);
    newRow.appendChild(answerColumn);
    newQuestion.appendChild(newRow);

    let fileRow = document.createElement("div");
    fileRow.className = "question row";
    let fileLabel = document.createElement("label");
    fileLabel.innerText = "Картинка";
    fileLabel.setAttribute("for", "photo" + newNumber);
    let fileInput = document.createElement("input");
    fileInput.className = "form-control";
    fileInput.setAttribute("type", "file")
    fileInput.setAttribute("id", "photo" + newNumber);

    fileRow.appendChild(fileLabel)
    fileRow.appendChild(fileInput)

    newQuestion.appendChild(fileRow)

    document.getElementById("tab-content").appendChild(newQuestion)

    document.getElementById("cards-count").value = newNumber;
}


function switchTab(event) {
  let i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tab-pane");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].className = tabcontent[i].className.replace("show active", "");
  }

  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
    tablinks[i].style.backgroundColor = "#cccccc";
  }
  number = event.currentTarget.innerText
  event.currentTarget.style.backgroundColor = "#55b1df"
  document.getElementById(number).className += "show active";
  event.currentTarget.className += " active"

}

