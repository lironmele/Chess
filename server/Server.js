let app = require('express')();

var turn = 'light';
var wait = true;

var piece = '';
var x = '';
var y = '';

app.get('/light', function (req, res) {
    if (turn == 'dark') {
        if (wait){
            res.send('still waiting')
            res.status(208);
        }
        else {
            res.append('piece', peice);
            res.append('x', x);
            res.append('y', y);
            res.status(200);
        }
    }
    else {
        res.status(203);
    }
});

app.post('/light', function (req, res) {
    if (turn == 'light' && wait) {
        wait = false;
        let query = req.query()
        piece = query['piece'];
        x = query['x'];
        y = query['y'];
        res.status(200);
    }
});

app.get('/dark', function (req, res) {
    if (turn == 'light') {
        if (wait){
            res.send('still waiting')
            res.status(208);
        }
        else {
            turn = 'dark';
            res.append('piece', peice);
            res.append('x', x);
            res.append('y', y);
            res.status(200);
        }
    }
    else {
        res.status(203);
    }
});

app.post('/dark', function (req, res) {
    if (turn == 'dark' && wait) {
        wait = false;
        let query = req.query()
        piece = query['piece'];
        x = query['x'];
        y = query['y'];
        res.status(200);
    }
});

app.listen(3000, console.log('Server listening on port 3000'));