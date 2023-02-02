var express = require("express");
var router = express.Router();

var MQTTclient = require('./Connection').MQTTclient;

var onbed, crying, awake, heart_rate, temperature, humidity;

MQTTclient.on('message', (topic, message) => {
    console.log('Received message:', message.toString());
    if (topic === "sensor") {
        msg = JSON.parse(message.toString())
        onbed = msg.data.onbed;
        crying = msg.data.crying;
        awake = msg.data.awake;
        heart_rate = msg.data.heart_rate;
        temperature = msg.data.temperature;
        humidity = msg.data.humidity;
    }
});

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
        var data = {onbed:onbed,crying:crying,awake:awake,heart_rate:heart_rate,temperature:temperature,humidity:humidity};
        return res.send(JSON.stringify(data));
    }
    catch (error) {
        res.status(500).send(error)
    }
});

router.post('/music', (req, res) => {
    try{
        play_or_stop = req.body.checked;
        if (play_or_stop==true){
            console.log('Play music instruction received');
            PublishToMQTT('music', 'play');
        }
        else{
            console.log('Stop music instruction received');
            PublishToMQTT('music', 'stop');
            // res.send('OK');
        }
        res.json({ message: 'Instruction received' });
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