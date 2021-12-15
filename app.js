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

app.post('/addCriteriumData', (req, res) => {
    comparations.push(req.body.matrix);
    res.redirect('/getAllComparations');
});

app.post('/addCriteriaComparation', (req, res) => {
    criteriaComparations = req.body.matrix;
    saveComparationsToFile();

    res.redirect('/getAllExperts');
})

var missCallComp = true;
app.get('/getAllComparations', (req, res) => {
    if (missCallComp) {
        missCallComp = false;
        criteriaLeft++;

    } else missCallComp = true;

    if( criteriaLeft == 0 ) {
        res.send(pug.renderFile(
            'public/pug/compareCriteria.pug', {
            expertNum: expertsNum - expertsLeft + 1,
            alternatives: criteria
        }));

    } else res.send(pug.renderFile(
            'public/pug/inputCriterium.pug', {
            expertNum: expertsNum - expertsLeft + 1,
            criterium: criteria[criteria.length - (criteriaLeft--)],
            alternatives: alternatives
        })
    );
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