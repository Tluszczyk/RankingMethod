function addColumn() {
    var column = document.querySelectorAll("#inputTable tr");

    column.forEach(row => {
        var cell = document.createElement('td');

        var input = document.createElement('input');
        input.type = "text";

        cell.appendChild(input);
        row.appendChild(cell);
    });
};

function subtractColumn() {
    var rows = document.querySelectorAll("#inputTable tr");

    rows.forEach(row => {
        row.removeChild(row.lastChild);
    });
}

function addRow() {
    var row = document.createElement('tr');
    row.innerHTML = document.getElementById('default-row').innerHTML;

    document.getElementById("inputTable").appendChild(row);
}

function subtractRow() {
    var lastRow = document.getElementById('inputTable').lastChild;

    document.getElementById("inputTable").removeChild(lastRow);
}

function sendToCalculate(matrix) {

    fetch('/addCriteriaComparation', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=UTF-8'
        },
        body: JSON.stringify({
            matrix: matrix
        })
    }).then(respCrit => {
        let res = respCrit.json();
        res.then(obj => fetch('/confirmInconsistentData', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json;charset=UTF-8'
            },
            body: JSON.stringify({
                confirmed: !obj.consistent && confirm(`This matrix is has CI = ${obj.CI}. Do you want to proceed?`)
            })
        }).then(response => window.location.href = response.url));
    });
}

function sendValues() {
    var matrix = [];

    matrix = Array.from(
        document.querySelectorAll("#inputTable tr")
    ).slice(1)
        .map(tr => Array.from(
            tr.children
        ).splice(1)
        .map(td => td.children[0].value)
        .map(v => v == '' ? '0' : v)
    )

    sendToCalculate(matrix);
}

function symmetricAutocompletionInit() {
    inputMatrix = Array.from(
        document.querySelectorAll("#inputTable tr")
    ).slice(1)
        .map(tr => Array.from(
            tr.children
        ).splice(1).map(td => td.lastChild)
    );

    for (let i = 0; i < inputMatrix.length; i++)
        inputMatrix[i][i].value = 1;

    for (let y = 0; y < inputMatrix.length; y++) {
        for (let x = 0; x < inputMatrix.length; x++) {

            inputMatrix[y][x].addEventListener(
                'input', e => inputMatrix[x][y].value = 1/parseFloat(e.target.value)
            );
        }
    }
}

window.onload = () => {

    symmetricAutocompletionInit();

    // document.getElementById("add").onclick = () => {
    //     addColumn();
    //     addRow();
    // };

    // document.getElementById("subtract").onclick = () => {
    //     subtractColumn();
    //     subtractRow();
    // };

    document.getElementById('submit').onclick = () => {
        document.getElementById("loader-div").style.visibility = "visible";
        sendValues();
    }
};