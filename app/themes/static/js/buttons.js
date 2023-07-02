function switchButton(event){
    let divId = event.currentTarget.value;

    let columns = document.getElementsByClassName("col search");
    for (let column in columns){
        column.style.display = "none";
    }
    let targetColumn = document.getElementById(divId);
    console.log(divId);
    targetColumn.style.display = "block"

}

for (let button in document.getElementsByClassName('btn')){
    button.addEventListener("onclick", switchButton)
}
