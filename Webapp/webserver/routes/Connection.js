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
  var topic = ['sensor', 'music/downloaded'];
  for (var i = 0; i < topic.length; i++) {
    MQTTclient.subscribe(topic[i], { qos: 1 }, (err, granted) =>  {
      if (err) {
        console.log(err);
        process.kill(process.pid, 'SIGTERM');
      }
      
    });
    console.log("Subscribed to topic: "+topic[i]);
  }
    
});

MQTTclient.on('error', (error) => {
  console.error(`MQTT client connection error: ${error}`);
  process.kill(process.pid, 'SIGTERM');
});


const mongoose = require('mongoose')

const url = "mongodb+srv://goldcrest101:Goldcrest123456@goldcrest.drrwpk3.mongodb.net/Goldcrest";

const connectionParams={
    useNewUrlParser: true,
    useUnifiedTopology: true 
}
mongoose.connect(url,connectionParams)
    .then( () => {
        console.log('Connected to the database ')
    })
    .catch( (err) => {
        console.error(`Error connecting to the database. n${err}`);
    })
    



const userSchema = new mongoose.Schema({
  username: String,
  password: String,
  baby:  mongoose.Schema.Types.Mixed
});

const User = mongoose.model("User", userSchema,"Users");

// const newUser = new User({
//   username: "Mom",
//   password: "Goldcrest123456",
//   baby:  [{id:0,name:"Mengyuan",month:1,gender:"girl"},
//           {id:1,name:"George",month:3,gender:"boy"},
//           {id:2,name:"Cathy",month:2,gender:"girl"},
//           {id:3,name:"Jeffery",month:5,gender:"boy"}]
// })
//   // Save the document to the collection
// newUser.save(function(error) {
//     if (error) {
//     console.log(error);
//     } else {
//     console.log("Document inserted successfully");
//     }
// });


router.post('/Id', (req, res) => {
  try{
      console.log(req.body);
      var username = req.body.username;
      var password = req.body.password;
      console.log(username);
      console.log(password);

      User.find({"username": { $regex: username }, "password": { $regex: password }},(err,user) => {
        if (err) {
          console.error(err);
          res.send("Error");
        } 
        else {
          if (user === null || user.length === 0) {
            console.log('No matching user found');
            res.send("No matching user found");
          } 
          else {
            var data = {babies:user[0].baby};
            return res.send(JSON.stringify(data));
          }
        } });
  }
  catch (error) {
      console.log("imhere")
      res.status(500).send(error)
  }
});


module.exports = router;
module.exports.MQTTclient= MQTTclient;
module.exports.mongoose= mongoose;