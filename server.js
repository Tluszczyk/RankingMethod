const spawn = require("child_process").spawn;
const express = require('express');
const path = require('path');
const pug = require('pug');
const fs = require('fs');

var app = express();

app.use(express.urlencoded());
app.use(express.json());
app.use(express.static(__dirname + '/public'));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, "public/html/inputComparation.html"));
});

var RANKING = null;

app.get('/ranking', (req, res) => {
    console.log(RANKING);

    res.send(pug.renderFile(
        'public/pug/ranking.pug', {
            map: RANKING
        })
    );
})

app.post('/calculate', (req, res) => {

    var calculatingRankingProcess = spawn('python3', [
        'public/python/calculatingRanking.py',
        req.body.matrix,
        req.body.alternatives
    ]);

    calculatingRankingProcess.stdout.on('data', data => {
        RANKING = JSON.parse(String(data).replace(/'/g, '"'));
        res.redirect('/ranking');
    });
});

app.listen(3000, () => {
    console.log("Application started and Listening on port http://localhost:3000");
});