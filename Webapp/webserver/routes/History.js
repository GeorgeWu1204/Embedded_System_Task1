var express = require("express");
var router = express.Router();
var Condition = require('./Popup').Condition;

router.post('/Date', (req, res) => {
    try{
        console.log(req.body);
        startTime = req.body.start;
        endTime = req.body.end;
        console.log(startTime);
        console.log(endTime);

        Condition.find({"time": {"$gt": startTime, "$lt": endTime}},(err,conditions) => {
            if (err) {
                console.error(err);
                return;
            }
            var humidity_list = [];
            var temperature_list = [];
            var heart_list = [];
            var time_list = [];
            for (var i=0; i<conditions.length; i++){
                humidity_list.push(conditions[i].humidity);
                temperature_list.push(conditions[i].temperature);
                heart_list.push(conditions[i].heart);
                time_list.push(conditions[i].time);
            }
            var data = {humidity:humidity_list,temperature:temperature_list,heart:heart_list,time:time_list};
            console.log(data);
            console.log(typeof data.humidity);
            // return res.send(JSON.stringify(data));
            return res.send(data);
        });
       
    }
    catch (error) {
        res.status(500).send(error)
    }
});

module.exports = router;