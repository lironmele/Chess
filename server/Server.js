let app = require('express')();

var turn;
var wait;

var old_x;
var old_y;
var new_x;
var new_y;

function start_game() {
    turn = 'White';
    wait = true;

    old_x = '';
    old_y = '';
    new_x = '';
    new_y = '';
}


app.get('/', function (req, res) {
    start_game();
    res.send();
});

app.get('/White', function (req, res) {
    if (wait || turn == 'White'){
        res.status(208);
        res.send('still waiting');
    }
    else {
        res.append('old_x', old_x);
        res.append('old_y', old_y);
        res.append('new_x', new_x);
        res.append('new_y', new_y);
        res.status(200);
        res.send('turn ended');
        old_x = '';
        old_y = '';
        new_x = '';
        new_y = '';
        wait = true;
        turn = 'White';
    }
});

app.post('/White', function (req, res) {
    if (turn == 'White' && wait) {
        headers = req.headers;
        old_x = headers['old_x'];
        old_y = headers['old_y'];
        new_x = headers['new_x'];
        new_y = headers['new_y'];
        res.status(200);
        res.send('sent successfully');
        wait = false;
    }
});

app.get('/Black', function (req, res) {
    if (wait || turn == 'Black'){
        res.status(208);
        res.send('still waiting');
    }
    else {
        res.append('old_x', old_x);
        res.append('old_y', old_y);
        res.append('new_x', new_x);
        res.append('new_y', new_y);
        res.status(200);
        res.send('turn ended');
        old_x = '';
        old_y = '';
        new_x = '';
        new_y = '';
        wait = true;
        turn = 'Black';
    }
});

app.post('/Black', function (req, res) {
    if (turn == 'Black' && wait) {
        headers = req.headers;
        old_x = headers['old_x'];
        old_y = headers['old_y'];
        new_x = headers['new_x'];
        new_y = headers['new_y'];
        res.status(200);
        res.send('sent successfully');
        wait = false;
    }
});

app.listen(3000, console.log('Server listening on port 3000'));