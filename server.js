var express = require('express');
var app = express();

var PORT = 8080;

app.use(express.static(__dirname + '/public'));

app.get('*', function(req, res){
  res.sendFile(__dirname + '/public/index.html');
});

app.listen(PORT, function(){
  console.log('app is lostening at port - ' + PORT);
});
