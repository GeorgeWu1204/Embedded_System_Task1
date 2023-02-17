import React, { Component } from "react";
import { useEffect } from 'react';
import {Switch} from 'antd'
import axios from "axios";
import './History.css';
import TimePicker from 'react-time-picker';
import DatePicker from 'react-datepicker';
import CanvasJSReact from '../assets/canvasjs.react';
import "react-datepicker/dist/react-datepicker.css";

const CanvasJSChart = CanvasJSReact.CanvasJSChart;

class History extends Component {
    constructor(props) {
        super(props)
        this.state = {
            startDate: new Date(Date.now()),
            startTime: '00:00',
            endDate: new Date(Date.now()),
            endTime: '00:00',
            errorFinding: false,
            humidityList:[
                { x: '2023-02-07T21:06:00.114Z', y: 24.99995231628418 },
                { x: '2023-02-07T23:27:25.524Z', y: 0 },
                { x: '2023-02-07T23:28:25.529Z', y: 0 },
                { x: '2023-02-07T23:37:55.823Z', y: 0 },
                { x: '2023-02-07T23:38:55.827Z', y: 0 },
                { x: '2023-02-07T23:39:55.833Z', y: 0 }
              ],
            temperatureList:[],
            heartList:[]
        }
    }

    handleReturn(){
        this.props.toggle();
    }

    handleStartChangeDate = date => {
        this.setState({startDate: date});
        // console.log(this.state.startDate);
    };

    handleStartChangeTime = time => {
        this.setState({ startTime:time })
        // console.log(this.state.startTime);
      };

    handleEndChangeDate = date => {
        this.setState({endDate: date});
    };

    handleEndChangeTime = time => {
        this.setState({endTime:time });
    };

   

    handleSubmitTime(){
        var startDateTime = new Date(this.state.startDate.getFullYear(), this.state.startDate.getMonth(), this.state.startDate.getDate(), this.state.startTime.slice(0, 2), this.state.startTime.slice(3,5));
        var endDateTime = new Date(this.state.endDate.getFullYear(), this.state.endDate.getMonth(), this.state.endDate.getDate(), this.state.endTime.slice(0, 2), this.state.endTime.slice(3,5));
        var data = {start: startDateTime, end: endDateTime}
        try {
            axios
                .post('http://localhost:9000/History/Date', data)
                .then(response=>{
                    var length = response.data.humidity.length;
                    var prepHumidityList = [];
                    var prepTemperatureList = [];
                    var prepHeartList = [];
                    for (var i = 0; i<length; i++){
                        prepHumidityList.push({x:new Date(response.data.time[i]), y:response.data.humidity[i]});
                        prepTemperatureList.push({x:new Date(response.data.time[i]), y:response.data.temperature[i]});
                        prepHeartList.push({x:new Date(response.data.time[i]), y:response.data.heart[i]});
                    }
                    this.setState({
                        humidityList:prepHumidityList,
                        temperatureList:prepTemperatureList,
                        heartList:prepHeartList
                    })
                    console.log(prepHumidityList);
                })
        } 
        catch (error) {
            console.error(error);
            this.setState({errorFinding:true});
        }
        
        console.log(this.state.humidityList);
        // console.log(endDateTime)
    }
    render() {
        const HeartChartOptions = {
            animationEnabled: true,
            theme: "dark2",
            width: 300,
            title: {
              text: 'Heart Rate History Plot',
              fontSize:15
            },
            axisX:{
              title: "Time",        
            //   valueFormatString: "hh:mm", 
              labelAngle: -20
            },
            axisY:{
              title : "BPM"
            },
            width: 310, 
            height: 250,
            data: [{
              type: 'line',
              dataPoints: this.state.heartList,
              lineColor: "#DA70D6",
              markerColor: "#BA55D3"
            }]
        };

        const TempChartOptions = {
            animationEnabled: true,
            theme: "dark2",
            title: {
              text: 'Temperature History Plot',
              fontSize:15
            },
            axisX:{
              title: "Time",        
            //   valueFormatString: "hh:mm", 
              labelAngle: -20
            },
            axisY:{
              title : "Temperature (degree)"
            },
            width: 310, 
            height: 250,
            data: [{
              type: 'line',
              dataPoints: this.state.temperatureList,
              lineColor: "#DA70D6",
              markerColor: "#BA55D3"
            }]
        };

        const HumidityChartOptions = {
            animationEnabled: true,
            theme: "dark2",
            title: {
              text: 'Humidity History Plot',
              fontSize:15
            },
            axisX:{
              title: "Time",        
            //   valueFormatString: "hh:mm", 
              labelAngle: -20
            },
            axisY:{
              title : "Humidity"
            },
            width: 310, 
            height: 250,
            data: [{
              type: 'line',
              dataPoints: this.state.humidityList,
              lineColor: "#DA70D6",
              markerColor: "#BA55D3"
            }]
        };

        return(
            <div class="popup_window">
                <div class= "close" onClick={()=>this.handleReturn()}>  
                    <img style={{ height: 20 }} src={require('../assets/imgs/Back.png')}>
                    </img>
                </div>
                <div class="status_title"> <span>{window.babyinfo[window.index].name}'s History </span></div>
                <div class="window_section"> 
                    <div class="start_section">
                        <span class="start_end_time_title"> Start Time</span>
                        <div class="start_date_picker">
                            <DatePicker
                                selected={this.state.startDate}
                                onChange={this.handleStartChangeDate}
                                format="dd/MM/yyyy"
                            />
                        </div>
                        <div class="start_time_picker">  
                            <TimePicker
                                value={this.state.startTime}
                                onChange={this.handleStartChangeTime}
                                disableClock="true"
                                
                            />
                        </div>  
                    </div>

                    <div class="end_section">
                        <span class="start_end_time_title"> End time</span>
                        
                        <div class="end_date_picker">
                            <DatePicker
                                selected={this.state.endDate}
                                onChange={this.handleEndChangeDate}
                                format="dd/MM/yyyy"
                            />
                        </div>

                        <div class="end_time_picker">  
                            <TimePicker
                                value={this.state.endTime}
                                onChange={this.handleEndChangeTime}
                                disableClock="true"
                                
                            />
                        </div>  
                    </div>
                    <div>
                        <button class='submittime' onClick={() => this.handleSubmitTime()}>Submit Time</button>
                    </div>

                    <div class="charts">
                        <div class="heart_chart"><CanvasJSChart options={HeartChartOptions}/></div>
                        <div class="temperature_chart"><CanvasJSChart options={TempChartOptions}/></div>
                        <div class="humidity_chart"><CanvasJSChart options={HumidityChartOptions}/></div>
                    </div>

                    <img class="unicorn_image" style={{ height: 140 }} src={require('../assets/imgs/unicorn.png')}>
                    </img>

                </div>
            </div>
        )
    }
}

export default History;