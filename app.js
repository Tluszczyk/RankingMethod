const spawn = require("child_process").spawn;
const bodyParser = require('body-parser');
const express = require('express');
const path = require('path');
const pug = require('pug');
const fs = require('fs');

const port = process.env.PORT || 3000;

var app = express();

app.use(express.urlencoded());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.json());
app.use(express.static(__dirname + '/public'));

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
        comparations,
        criteriaComparations
    ]);

    calculatingRankingProcess.stdout.on('data', data => {
        RANKING = JSON.parse(String(data).replace(/'/g, '"'));

        res.redirect('/ranking');
    });
    // res.redirect('/');
};

var criteria;
var alternatives;
var comparations = [];
var criteriaComparations;
var comparedCriteria = false;

app.post('/addCriteriumData', (req, res) => {
    comparations.push(req.body.matrix);
    res.redirect('/getAllComparations');
});

app.post('/addCriteriaComparation', (req, res) => {
    criteriaComparations = req.body.matrix;
    calculate(req, res);
})

var missCall = true;
app.get('/getAllComparations', (req, res) => {
    if (missCall) {
        missCall = false;
        criteriaLeft++;

    } else missCall = true;

    if( criteriaLeft == 0 ) {
        if( comparedCriteria ) {

        } else res.send(pug.renderFile(
            'public/pug/compareCriteria.pug', {
                alternatives: criteria
            }
        ));

    } else res.send(pug.renderFile(
            'public/pug/inputCriterium.pug', {
            criterium: criteria[criteria.length - (criteriaLeft--)],
            alternatives: alternatives
        })
    );
});

app.post('/processCriteriaAndAlternatives', (req, res) => {
    criteria = req.body.criteria;
    alternatives = req.body.alternatives;

    criteriaLeft = criteria.length;

    res.redirect("/getAllComparations");
});

app.listen(port, () => {
    console.log("Application started and Listening on port http://localhost:3000 or on some other environmental port");
});