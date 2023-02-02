var express = require('express');
var router = express.Router();
var mqtt = require('mqtt');
var fs = require('fs');

var clientOptions = {
    clientID: "goldcrestwebapp",
    username: "webapp",
    password: "123456",
    key: fs.readFileSync('../webserver/cert/webapp.key'),
    cert: fs.readFileSync('../webserver/cert/webapp.crt'),
    ca: [ fs.readFileSync('../webserver/cert/ca.crt') ]
}

var MQTTclient;

MQTTclient = mqtt.connect('mqtts://goldcrest101.duckdns.org', clientOptions);

MQTTclient.on('connect', () => {
  console.log('MQTT client connected');
  topic = 'sensor'
  MQTTclient.subscribe(topic, (err, granted) => {
    if (err) {
      console.log(err);
      process.kill(process.pid, 'SIGTERM');
    }
    console.log('Subscribed to topics: ' + topic);
  });
});

MQTTclient.on('error', (error) => {
  console.error(`MQTT client connection error: ${error}`);
  process.kill(process.pid, 'SIGTERM');
});




// router.get('/', function(req, res, next) {
// });


module.exports = router;
module.exports.MQTTclient= MQTTclient;
