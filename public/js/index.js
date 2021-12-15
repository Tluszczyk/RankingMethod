function addColumn(table, value) {
    if( value != "" ) {
        let row = document.createElement("tr");
        let cell = document.createElement("td");

        cell.textContent = value;

        row.appendChild(cell)
        table.lastChild.appendChild(row);
    
    } else alert("Input a value");
}

function subColumn(table) {
    if (table.lastChild.children.length > 2 )
        table.lastChild.removeChild(table.lastChild.lastChild);

    else alert("No elements in the list");
}

function attachButtons(table, divName, inputName) {
    var input = document.getElementById(inputName);

    document
        .querySelector(`#${divName} > .addButton`)
        .onclick = () => {
            addColumn(
                table,
                input.value
            );
            input.value = "";
        };

    document
        .querySelector(`#${divName} > .subButton`)
        .onclick = () => {
            subColumn(
                table,
                input.value
            );
            input.value = "";
        };
}

function getTableData(table) {
    var tableRowsAll = table.querySelectorAll("tr");
    var tableRowsData = [...tableRowsAll].splice(2, tableRowsAll.length);
    var tableDataCells = tableRowsData.map(rd => rd.children[0]);
    return tableDataCells.map(td => td.textContent);
}

function sendFormData(criteriaTable, alternativesTable, methodSelect, expertsNumInput) {

    var criteriaData = getTableData(criteriaTable);
    var alternativesData = getTableData(alternativesTable);
    var methodData = methodSelect.value;
    var expertsNumData = expertsNumInput.value;

    fetch('/processCriteriaAndAlternatives', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=UTF-8'
        },
        body: JSON.stringify({
            criteria: criteriaData,
            alternatives: alternativesData,
            method: methodData,
            expertsNum: expertsNumData,
        })
    }).then(response => window.location.href = response.url);
}

(function() {
    var criteriaTable = document.getElementById("criteriaTable");
    var alternativesTable = document.getElementById("alternativesTable");
    var methodSelect = document.getElementById("method");
    var expertsNumInput = document.getElementById("expertsNum");

    attachButtons(criteriaTable, "criteriaDiv", "criterionInput");
    attachButtons(alternativesTable, "alternativesDiv", "alternativeInput");

    document.getElementById("submitButton").onclick = () => sendFormData(
        criteriaTable, alternativesTable, methodSelect, expertsNumInput
    );
})();