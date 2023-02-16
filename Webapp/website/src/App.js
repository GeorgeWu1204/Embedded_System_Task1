import React, { Component } from 'react';
import './App.css';
import Top from './components/top'
import background from "./assets/imgs/background.png";
import axios from "axios";

window.index = 0;
// window.babyinfo = [{id:0, name:"Mengyuan", month:1, gender:"girl"},{id:1, name:"George", month:8, gender:"boy"},{id:2, name:"Cathy", month:3, gender:"girl"},{id:3, name:"Jeffery", month:6, gender:"boy"}]
window.babyinfo = []

class App extends Component {
    constructor(props){
        super(props)
        this.state={
            username:"",
            password:"",
            error: false
        }
    }
    
    handleUsername(username){
        this.setState({error:false, username: username})
    }
    handlePassword(password){
        this.setState({password: password})
    }

    submitUser(user){
        try {
            axios
                .post('http://localhost:9000/Id', user)
                .then(response=>{
                    console.log(response);
                    if (response.data === "No matching user found"){
                        console.log("nonoon"); 
                        this.setState({error: true})}
                    else{
                        // response = JSON.parse(response);
                        console.log(response);
                        window.babyinfo = response.data.babies; 
                        window.location.href = 'http://localhost:3000/#/Baby';
                        console.log(response.data.babies);
                        console.log(window.babyinfo);
                    }   
        })}
        catch (error) {
            console.error(error);
        }
      }
      
    handleSubmitUser = (event) => {
        event.preventDefault();
        event.target.reset();
        var user = {username: this.state.username, password: this.state.password};
       this.submitUser(user);
    }
    render() {
            return (
                <div class='bg' style={{ backgroundImage: `url(${background})`  }} >
                    <div className="App">
                        <Top e='0' />
                            <div class="bird">
                                <img class='image' src={require("./assets/imgs/bird.png")}>
                                </img>
                            </div>
                            <div class="goldcrest">
                                <img class='image' src={require("./assets/imgs/goldcrest.png")}>
                                </img>
                            </div>
                            <div class="technology">
                                <img class='image' src={require("./assets/imgs/technology.png")}>
                                </img>
                            </div>
                            <div class='textout'>
                                {/* <span class="main_title">SMART CRADLE</span>
                                <br/>
                                <span class="slogan">A SAFE SLEEP FOR YOUR LITTLE ONE</span> */}

                                <div class="login_window">
                                    <form onSubmit={this.handleSubmitUser}>
                                        <label>
                                        <div class="username">
                                            Username: &nbsp;
                                            <input type="username" onChange={(event) => this.handleUsername(event.target.value)} />
                                        </div>
                                        </label>
                                        <br />
                                        <label>
                                        <div class="password">
                                            Password: &nbsp;
                                            <input  type="password" onChange={(event) => this.handlePassword(event.target.value)} />
                                        </div>
                                        </label>
                                        <br />
                                        <button type="submit" class="login_button">Login</button>
                                    </form>
                                    {this.state.error ? 
                                        <div class="mismatch">
                                            <span> Username or password is not found </span> 
                                        </div> 
                                        : 
                                        <div class="mismatch"> </div>
                                    }
                                </div>
                            </div>
                    </div>
                </div>
            );
        }
    }

export default App;


