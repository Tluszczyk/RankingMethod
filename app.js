const spawn = require("child_process").spawn;
const bodyParser = require('body-parser');
const express = require('express');
const path = require('path');
const pug = require('pug');
const fs = require('fs');

const zip = (a, b) => a.map((k, i) => [k, b[i]]);

const port = process.env.PORT || 3000;

var app = express();

app.use(express.urlencoded());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.json());
app.use(express.static(__dirname + '/public'));

var criteria = [];
var method;
var expertsNum;
var expertsLeft;
var criteriaLeft;
var alternatives = [];
var comparations = [];
var criteriaComparations = [];

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, "public/html/index.html"));
});

var RANKING = null;

app.get('/ranking', (req, res) => {
    res.send(pug.renderFile(
        'public/pug/ranking.pug', {
        map: RANKING
    })
    );
})
 
function calculate(req, res) {

    console.log("Calculating...");

    // fs.writeFileSync('public/data/comparationData.txt',
    //     String(alternatives) + "\n" +
    //     String(criteria) + "\n" +
    //     String(comparations) + "\n" +
    //     String(criteriaComparations)
    // );

    // var calculatingRankingProcess = spawn('python3', [
    //     'public/python/calculatingRanking.py',
    //     'public/data/comparationData.txt'
    // ]);

    var calculatingRankingProcess = spawn('python3', [
        'public/python/calculatingRanking.py',
        alternatives,
        criteria,
        method,
        expertsNum,
    ]);

    calculatingRankingProcess.stdout.on('data', data => {
        // console.log(data);
        RANKING = JSON.parse(String(data).replace(/'/g, '"'));

        res.redirect('/ranking');
    });
};

function saveComparationsToFile() {
    zip(criteria, comparations).forEach(pair => {
        let [criterion, comparation] = pair;

        fs.writeFileSync(
            "public/python/matrices/"+criterion+"_exp"+(expertsNum-expertsLeft+1)+".txt", 
            comparation.reduce((x, y) => x + '\n' + y).replace(/,/g, ' ')
        );
    });

    fs.writeFileSync(
        "public/python/matrices/"+"priorities_exp" + (expertsNum - expertsLeft+1) + ".txt",
        criteriaComparations.reduce((x, y) => x + '\n' + y).replace(/,/g, ' ')
    );
}

function checkCICR(matrix, method, _callback) {
    var checkingCICRProcess = spawn('python3', [
        'public/python/calculateIndex.py',
        matrix,
        method
    ]);

    checkingCICRProcess.stdout.on('data', data => {
        let [CI, CR] = String(data).split(' ');

        _callback(parseFloat(CI), parseFloat(CR));
    });
}

let _confirm_matrix_pipe;

app.post('/confirmInconsistentData', (req, res) => {
    if( req.body.confirmed ) {
        if (!comparingCriteria) criteriaLeft++;
    } else {
        if (comparingCriteria) {
            saveComparationsToFile();
            res.redirect('/getAllExperts');
        } else comparations.push(_confirm_matrix_pipe);
    }
    
    res.redirect('/getAllComparations');
});

app.post('/addCriteriumData', (req, res) => {
    let matrix = req.body.matrix;
    _confirm_matrix_pipe = matrix;

    checkCICR(matrix, method, (CI, CR) => {
        res.send({ CI: CI, CR: CR, consistent: false});//CI <= 0.1 });
    });
});

app.post('/addCriteriaComparation', (req, res) => {
    let matrix = req.body.matrix;

    _confirm_matrix_pipe = matrix;
    criteriaComparations = matrix;
    
    checkCICR(matrix, method, (CI, CR) => {
        res.send({ CI: CI, CR: CR, consistent: false });//CI <= 0.1 });
    });
})

var comparingCriteria = false;
var missCallComp = true;
app.get('/getAllComparations', (req, res) => {
    if (missCallComp) {
        missCallComp = false;
        criteriaLeft++;

    } else missCallComp = true;

    if( criteriaLeft == 0 ) {
        comparingCriteria = true;

        res.send(pug.renderFile(
            'public/pug/compareCriteria.pug', {
            expertNum: expertsNum - expertsLeft + 1,
            alternatives: criteria
        }));

    } else {
        comparingCriteria = false;
        res.send(pug.renderFile(
            'public/pug/inputCriterium.pug', {
            expertNum: expertsNum - expertsLeft + 1,
            criterium: criteria[criteria.length - (criteriaLeft--)],
            alternatives: alternatives
        }));
    }
});

var missCallExp = true;
app.get('/getAllExperts', (req, res) => {
    if (missCallExp) {
        missCallExp = false;
        expertsLeft++;

    } else {
        missCallExp = true;

        criteriaLeft = criteria.length;
        comparations = [];
    }

    if (--expertsLeft == 0) {
        calculate(req, res);

    } else res.redirect('/getAllComparations');
});

app.post('/processCriteriaAndAlternatives', (req, res) => {
    criteria = req.body.criteria;
    alternatives = req.body.alternatives;
    method = req.body.method;
    expertsNum = req.body.expertsNum;

    criteriaLeft = criteria.length;
    expertsLeft = expertsNum;

    res.redirect("/getAllExperts");
});

app.listen(port, () => {
    console.log("Application started and Listening on port http://localhost:3000 or on some other environmental port");
});