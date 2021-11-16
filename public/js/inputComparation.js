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

function sendToCalculate( alternatives, matrix ) {

    fetch('/calculate', {
        method: "POST",
        headers: { 
            'Content-Type': 'application/json;charset=UTF-8'
        },
        body: JSON.stringify({
            alternatives: alternatives,
            matrix: matrix
        })
    }).then(response => window.location.href = response.url);
}

function sendValues() {
    var alternatives = Array.from(
        document.querySelectorAll("#default-row > td > input")
    ).map(td => td.value).slice(1);

    var matrix = [];

    if( alternatives.filter(a => a.length == 0).length > 0 ) {
        alert("You have to fill the alternatives!");
        return;
    }
    
    matrix = Array.from(
        document.querySelectorAll("#inputTable tr")
    ).slice(1)
    .map(tr => Array
        .from(tr.childNodes)
        .slice(2)
        .map(td => td.firstChild)
        .filter(td => !!td)
        .map(input => input.value)
    );

    sendToCalculate( alternatives, matrix );
}

window.onload = () => {
    
    document.getElementById("add").onclick = () => {
        addColumn();
        addRow();
    };

    document.getElementById("subtract").onclick = () => {
        subtractColumn();
        subtractRow();
    };

    document.getElementById('submit').onclick = sendValues;
};