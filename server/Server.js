let app = require('express')();

var turn = 'White';
var wait = true;

var piece = '';
var x = '';
var y = '';

app.get('/White', function (req, res) {
    if (turn == 'Black') {
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

app.post('/White', function (req, res) {
    if (turn == 'White' && wait) {
        wait = false;
        let query = req.query()
        piece = query['piece'];
        x = query['x'];
        y = query['y'];
        res.status(200);
    }
});

app.get('/Black', function (req, res) {
    if (turn == 'White') {
        if (wait){
            res.send('still waiting')
            res.status(208);
        }
        else {
            turn = 'Black';
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

app.post('/Black', function (req, res) {
    if (turn == 'Black' && wait) {
        wait = false;
        let query = req.query()
        piece = query['piece'];
        x = query['x'];
        y = query['y'];
        res.status(200);
    }
});

app.listen(3000, console.log('Server listening on port 3000'));