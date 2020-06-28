let app = require('express')();

var turn = 'White';
var wait = true;

var old_x = '';
var old_y = '';
var new_x = '';
var new_y = '';

app.get('/White', function (req, res) {
    if (turn == 'Black') {
        if (wait){
            res.status(208);
            res.send('still waiting')
        }
        else {
            turn = 'White';
            wait = true;
            res.append('old_x', old_x);
            res.append('old_y', old_y);
            res.append('new_x', new_x);
            res.append('new_y', new_y);
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
        old_x = query['old_x'];
        old_y = query['old_y'];
        new_x = query['new_x'];
        new_y = query['new_y'];
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
            res.append('old_x', old_x);
            res.append('old_y', old_y);
            res.append('new_x', new_x);
            res.append('new_y', new_y);
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
        old_x = query['old_x'];
        old_y = query['old_y'];
        new_x = query['new_x'];
        new_y = query['new_y'];
        res.status(200);
        res.send('sent successfully');
    }
});

app.listen(3000, console.log('Server listening on port 3000'));