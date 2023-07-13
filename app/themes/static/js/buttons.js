function switchButton(event){
    let divId = event.currentTarget.value;

    let columns = document.getElementsByClassName("col search");
    console.log(columns);
    for (let column in columns){
        console.log(column);
        column.style.display = "none";
    }
    let targetColumn = document.getElementById(divId);
        targetColumn.style.display = "block"

}
