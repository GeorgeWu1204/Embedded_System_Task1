var express = require("express");
var router = express.Router();

var MQTTclient = require('./Connection').MQTTclient;
var mongoose = require('./Connection').mongoose;

var onbed, crying, awake, songDownloaded;
var heart_rate = 0;
var temperature = 0;
var humidity = 0;
var averageHumidity = 0;
var averageTemperature = 0;
var averageHeartrate = 0;

var onceReceived = false;

MQTTclient.on('message', (topic, message) => {
    if (!onceReceived){
        setInterval(storeDatabase, 60000);
        onceReceived = true;
    }
    console.log('Received message on', message.toString());
    msg = JSON.parse(message.toString())
    
    if (topic === "sensor") {
        if (msg.data){
            onbed = msg.data.onbed;
            // onbed = true;
            // crying = true;
            crying = msg.data.crying;
            awake = msg.data.awake;
            // awake = true;
            heart_rate = msg.data.heart_rate;
            // heart_rate = 0;
            temperature = msg.data.temperature;
            humidity = msg.data.humidity;
            averageHeartrate = (averageHeartrate + heart_rate)/2;
            averageTemperature = (averageTemperature + temperature)/2;
            averageHumidity = (averageHumidity + humidity)/2;
        }
    }
    else if (topic === "music/downloaded"){
        if (msg.downloaded){
            songDownloaded = msg.downloaded;
        } 
    }
});



// Define the schema for a document
const conditionSchema = new mongoose.Schema({
    temperature: Number,
    humidity: Number,
    heart: Number,
    time: Date
  });
  
// Compile the schema into a model
const Condition = mongoose.model("Condition", conditionSchema,"HistoryConditions");


function storeDatabase() {
    const newCondition = new Condition({
        temperature: averageTemperature,
        humidity: averageHumidity,
        heart: averageHeartrate,
        time: new Date()
    })
      // Save the document to the collection
    newCondition.save(function(error) {
        if (error) {
        console.log(error);
        } else {
        console.log("Document inserted successfully");
        }
    });
    console.log('called about every 6 seconds');
}
  
// Create a new document
//   const newRoom = new Room({
//     temperature: 40,
//     humidity: 60
//   });
  
  // Save the document to the collection
//   newRoom.save(function(error) {
//     if (error) {
//       console.log(error);
//     } else {
//       console.log("Document inserted successfully");
//     }
//   });
  
//   // Find all sensor in the collection
//   Sensor.find({}, (err, sensors) => {
//     if (err) {
//       console.error(err);
//       return;
//     }
  
//     console.log(sensors);
//   });


function PublishToMQTT(topic,msg){
	console.log("topic:", topic, ", publishing", msg);
    try{
        if (MQTTclient.connected == true){
            MQTTclient.publish(topic, msg.toString(), {qos: 1});
        }
    }
    catch(err) {
        console.error(`Error while sending message: ${err}`);
    }
}

router.get('/', (req, res) => {
    try{
        var data = {onbed:onbed,crying:crying,awake:awake,heart_rate:heart_rate,temperature:temperature,humidity:humidity,songDownloaded:songDownloaded};
        return res.send(JSON.stringify(data));
    }
    catch (error) {
        res.status(500).send(error)
    }
});

router.post('/startStop', (req, res) => {
    try{
        play_or_stop = req.body.startStop;
        songDownloaded = 0;
        if (play_or_stop==true){
            console.log('Play music instruction received');
            PublishToMQTT('music/play', 'play');
        }
        else{
            console.log('Stop music instruction received');
            PublishToMQTT('music/play', 'stop');
            // res.send('OK');
        }
        res.json({ message: 'Instruction received' });
    }
    catch (error) {
        res.status(500).send(error)
    }
});

router.post('/music', (req, res) => {
    try{
        music_name = req.body.Name;
        PublishToMQTT('music/name', music_name);
        res.json({ message: 'Music name received' });
    }
    catch (error) {
        res.status(500).send(error)
    }
});

router.post('/cradle', (req, res) => {
    try{
        rock_or_not = req.body.checked;
        if (rock_or_not ==true){
            console.log('Rock cradle instruction received');
            PublishToMQTT('rock', 'play');
            // res.send('OK');
        }
        else{
            console.log('Stop rocking cradle instruction received');
            PublishToMQTT('rock', 'stop');
            // res.send('OK');
        }
        res.json({ message: 'Instruction received' });
    }
    catch (error) {
        res.status(500).send(error)
    }
});
module.exports = router;
module.exports.Condition = Condition;