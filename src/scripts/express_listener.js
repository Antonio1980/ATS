var express = require('express');
var fs = require('fs');
var bodyParser = require('body-parser');

var app = express();
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json()); 
app.post('/response', function(req, res) {

    // path of the file to output
    var outputFilename = './output/customers_precondition.csv';
    
    // write to the file system
    fs.writeFileSync(outputFilename, JSON.stringify(req.body.payload), null, 4); 
    // fs.appendFileSync(outputFilename, JSON.stringify(req.body.payload), null, 4);
    // fs.appendFileSync(outputFilename, "\n", null, 4);

    res.send('Saved to ' + outputFilename);

});

var port = 3000;
app.listen(port);
