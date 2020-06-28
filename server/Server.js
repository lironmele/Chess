let app = require('express')();

var turn = 'White';
var wait = true;

var x = '';
var y = '';

app.get('/White', function (req, res) {
    if (turn == 'Black') {
        if (wait){
            res.status(208);
            res.send('still waiting')
        }
        else {
            turn = 'White';
            wait = true;
            res.append('x', x);
            res.append('y', y);
            res.status(200);
            r.send('turn ended');
        }
    }
    else {
        res.status(203);
        res.send("it's your turn");
    }
});

app.post('/White', function (req, res) {
    if (turn == 'White' && wait) {
        wait = false;
        let query = req.query()
        x = query['x'];
        y = query['y'];
        res.status(200);
        res.send('sent successfully');
    }
});

app.get('/Black', function (req, res) {
    if (turn == 'White') {
        if (wait){
            res.status(208);
            res.send('still waiting')
        }
        else {
            turn = 'Black';
            wait = true;
            res.append('x', x);
            res.append('y', y);
            res.status(200);
            r.send('turn ended');
        }
    }
    else {
        res.status(203);
        res.send("it's your turn");
    }
});

app.post('/Black', function (req, res) {
    if (turn == 'Black' && wait) {
        wait = false;
        let query = req.query()
        x = query['x'];
        y = query['y'];
        res.status(200);
        res.send('sent successfully');
    }
});

app.listen(3000, console.log('Server listening on port 3000'));