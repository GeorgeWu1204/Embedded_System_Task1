import React, { Component } from "react";
import { useEffect } from 'react';
import {Switch, Button} from 'antd'
import axios from "axios";
import './Popup.css';
import History from "./History"; 
import CanvasJSReact from '../assets/canvasjs.react';
import ReactLoading from "react-loading";

const CanvasJSChart = CanvasJSReact.CanvasJSChart;

class PopUp extends Component {
  constructor(props) {
    super(props)
    this.state = {
      HeartChart: false,
      // HeartDataPoints:[{x: new Date(Date.now()),y:200},{x:new Date(Date.now()+1000),y:400}],
      HeartDataPoints: [],
      TemperatureChart: false,
      TemperatureDataPoints: [],
      HumidityDataPoints: [],
      TimeDataPoints: [],
      // TemperatureDataPoints:[{x: new Date(Date.now()),y:200},{x:new Date(Date.now()+1000)}],
      // HumidityDataPoints:[{x: new Date(Date.now()),y:100},{x:new Date(Date.now()+1000),y:200}],
      
      onbed: null,
      crying: false,
      awake: true,
      heart_rate: 0,
      temperature: 0,
      humidity: 0,
      ViewHistory: false,
      songName: "",
      songLoading: false,
      songDownloaded: 0
    }
  }
  componentDidMount() {
    this.intervalId = setInterval(() => {
      axios
        .get("http://localhost:9000/Popup")
        .then(response => {
          this.setState({ 
            onbed: response.data.onbed,
            crying: response.data.crying,
            awake: response.data.awake,
            heart_rate: response.data.heart_rate,
            temperature: response.data.temperature,
            humidity: response.data.humidity,
            songDownloaded: response.data.songDownloaded
          });
          if (response.data.songDownloaded === 1){
            this.setState({songLoading: false})
          }
          var newHeartDataPoints = [...this.state.HeartDataPoints,{x:new Date(), y:response.data.heart_rate}];
          var newTemperatureDataPoints = [...this.state.TemperatureDataPoints, {x:new Date(), y:response.data.temperature}];
          var newHumidityDataPoints = [...this.state.HumidityDataPoints, {x:new Date(), y:response.data.humidity}];
          if (this.state.HeartDataPoints.length >= 50){
            newHeartDataPoints.shift();
            newTemperatureDataPoints.shift();
            newHumidityDataPoints.shift();
          }
  
          this.setState({HeartDataPoints:newHeartDataPoints, 
                         TemperatureDataPoints:newTemperatureDataPoints, 
                         HumidityDataPoints:newHumidityDataPoints})
         
        })
        .catch(error => {
          console.log(error);
        });
    }, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.intervalId);
  }
  
  handleReturn(){
    this.props.toggle();
  }

  async startStopMusic(startStop){
    try {
      this.setState({songDownloaded:0});
      await axios.post('http://localhost:9000/Popup/startStop', {startStop});
      console.log('Music: Start/Stop Instruction sent successfully:', {startStop});
    } 
    catch (error) {
      console.error(error);
    }
  }

  async submitMusic(song){
    try {
      await axios.post('http://localhost:9000/Popup/music', {Name: song});
      console.log('Music: Name Instruction sent successfully');
    } 
    catch (error) {
      console.error(error);
    }
  }
  
  async rockCradle(checked){
    try {
      await axios.post('http://localhost:9000/Popup/cradle', {checked});
      console.log('Cradle: Instruction sent successfully');
    } 
    catch (error) {
      console.error(error);
    }
  }
  handleHistory(){
    this.setState({
      ViewHistory: !this.state.ViewHistory
    })
  }

  handleSubmit = (event) => {
    event.preventDefault();
    console.log("Submitted value:", this.state.songName);
    event.target.reset();
    this.submitMusic(this.state.songName);
    this.setState({songLoading:true, songName:"", songDownloaded:0});
  }

render() {
  const HeartChartOptions = {
    theme: "dark2",
    title: {
      text: 'Heart Rate History Plot',
      fontSize:15
    },
    axisX:{
      title: "Time",
      // gridThickness: 2,
      // interval:2, 
      // intervalType: "hour",        
      valueFormatString: "hh:mm:ss", 
      labelAngle: -20
    },
    axisY:{
      title : "BPM"
    },
    width: 350, 
    height: 250,
    data: [{
      type: 'line',
      dataPoints: this.state.HeartDataPoints,
      lineColor: "#DA70D6",
      markerColor: "#BA55D3"
    }]

  };

  const TemperatureHumidityChartOptions = {
    theme: "dark2",
    // backgroundColor: "dark green",
    title: {
      text: 'Temperature and Humidity History Plot',
      fontSize:15,
      // fontFamily:"verdana",
      // fontWeight:"bold",

    },
    axisX:{
      title: "Time",        
      valueFormatString: "hh:mm:ss", 
      labelAngle: -20,
    },

    width: 350, 
    height: 250,
    legend:{
      cursor:"pointer",
      verticalAlign: "bottom",
      horizontalAlign: "center",
      dockInsidePlotArea: true,
      // itemclick: toogleDataSeries
    },
    data: [{
      type: 'line',
      dataPoints: this.state.TemperatureDataPoints,
      showInLegend: true,
      name: 'Temperature (Deg)',
      lineColor: "#DA70D6",
      markerColor: "#BA55D3"
    },
    {
      type: 'line',
      dataPoints: this.state.HumidityDataPoints,
      showInLegend: true,
      name: 'Humidity (%)'
    }]
  };

  
  return (
    <div class="popup_window">
      
      <div class= "close" onClick={()=>this.handleReturn()}>  
        <img style={{ height: 20 }} src={require('../assets/imgs/cross_icon.png')}>
        </img>
      </div>
      <div class="status_title"> <span>{window.babyinfo[window.index].name}'s Status</span> </div>
      
      <div class="window_section"> 
        <div class="baby_condition">
          {window.babyinfo[window.index].gender == "girl" ? 
            <div class="subtitle" id="borderimg"> How is my girl? </div>:
            <div class="subtitle"> How is my boy? </div>
          }
          <div class="info_detail">
            <span> On bed</span>
            <img style={{ height: 30 }} src={require('../assets/imgs/cradle.png')}></img>
            {this.state.onbed == null ? <span>: Loading</span> : (this.state.onbed == true ? <span>: Yes</span> : <span>: No</span>)} 
            <br/>

            <span> Crying</span>
            <img style={{ height: 30 }} src={require('../assets/imgs/crying.png')}></img>
            {this.state.onbed == null ? <span>: Loading</span> : (this.state.crying == true ? <span>: Yes</span> : <span>:No</span>)} <br/>

            <span> Awake</span>
            <img style={{ height: 30 }} src={require('../assets/imgs/awake.png')}></img>
            {this.state.onbed == null ? <span>: Loading</span> : (this.state.awake == true ? <span>: Yes</span> : <span>: No</span>)} <br/>

            <span onMouseEnter = {() => this.setState({HeartChart:true})} onMouseLeave={() => this.setState({HeartChart:false})}> Heartrate: </span> 
            <img style={{ height: 30 }} src={require('../assets/imgs/heartrate.png')}></img>
            <span>: {this.state.heart_rate} BPM</span>

            {this.state.HeartChart ? <CanvasJSChart options={HeartChartOptions}/> : null}
            {/* <br/> <span> {this.state.HeartChart && <span> Here will be replaced by chart </span> } </span> */}
          </div>
        </div>

        <div class="interact">
        {window.babyinfo[window.index].gender == "girl" ? 
            <div class="subtitle"> Interact with my girl </div>:
            <div class="subtitle"> Interact with my boy </div>
        }
        <div class="info_detail">
          <div class = "play_music_title">
            <span> 
              Play music
            </span>
            <img style={{ height: 30 }} src={require('../assets/imgs/music.png')}></img> 
            :
            <br/>
          </div>
          <div class = "musicform">
            <form  onSubmit={this.handleSubmit}>
              <input
                type="text"
                placeholder="Search for music"
                onChange={(e) => {this.setState({songName:e.target.value});}}
              />
              &nbsp;
              <button type="submit" class="music_button">Find</button>
            </form>
          </div>

          {this.state.songLoading ? 
            <div class="downloading">
              <ReactLoading class="spinning" type="spinningBubbles" height={'10%'} width={'10%'} />
              <span>&nbsp;&nbsp;&nbsp; Downloading </span> 
            </div> 
            : 
            <div class="downloading"> </div>
          }
          {
            this.state.songDownloaded ?
            <div class="downloading">
              <img style={{ height: 30 }} src={require('../assets/imgs/tick.png')}></img> 
              <span> Downloaded </span> 
            </div> 
            : 
            <div class="downloading"> </div>
          }
    
          <div class = "play_music_buttons">
            <img style={{ height: 30 }} src={require('../assets/imgs/start.png')} onClick={() => this.startStopMusic(1)}></img>
            &nbsp;&nbsp;&nbsp;
            <img style={{ height: 30 }} src={require('../assets/imgs/stop.png')} onClick={() => this.startStopMusic(0)}></img>
          </div>
{/* 
          <span><b>
              <br/> off <Switch onChange={(checked) => this.playMusic(checked)}/> on
          </b></span>
          <br/> */}
          <div class="rock_cradle">
            <span> Rock the cradle</span>
            <img style={{ height: 30 }} src={require('../assets/imgs/swing.png')}></img> 
            <span><b>
                : <br/> off <Switch onChange={(checked) => this.rockCradle(checked)}/> on
            </b></span>
            <br/>
          </div>
        </div>

        </div>
        <div class="room_condition">
          {window.babyinfo[window.index].gender == "girl" ? 
            <div class="subtitle"> Is her room comfy? </div>:
            <div class="subtitle"> Is his room comfy? </div>
          }
          <div class="info_detail">
            <span onMouseEnter = {() => this.setState({TemperatureChart:true})} onMouseLeave={() => this.setState({TemperatureChart:false})}> Room temperature </span> 
            <img style={{ height: 30 }} src={require('../assets/imgs/temperature.png')}></img> 
            {this.state.temperature == 0 ? <span>: Loading</span> : <span>: {this.state.temperature} &#8451; </span>} <br/>

            <span onMouseEnter = {() => this.setState({TemperatureChart:true})} onMouseLeave={() => this.setState({TemperatureChart:false})}> Room humidity </span> 
            <img style={{ height: 30 }} src={require('../assets/imgs/humidity.png')}></img> 
            {this.state.humidity == 0 ? <span>: Loading</span> : <span>: {this.state.humidity} % </span>} <br/>
            {this.state.TemperatureChart ? <CanvasJSChart options={TemperatureHumidityChartOptions}/> : null}
          </div>
        </div>
        <img class="unicorn_image" style={{ height: 140 }} src={require('../assets/imgs/unicorn.png')}>
        </img>
      </div>
      <div>
          <button class='historybutton' onClick={() => this.handleHistory()}>View History</button>
      </div>
    {this.state.ViewHistory ? <History toggle={() => this.setState({ViewHistory:!this.state.ViewHistory})} /> : null}
    
    

    </div>
    
  );
 }
}
export default PopUp;