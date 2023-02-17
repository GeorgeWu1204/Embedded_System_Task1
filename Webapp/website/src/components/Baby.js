import React, { Component } from 'react';
import './Baby.css';
import Top from './top'
import { Row, Col, Switch, Input, Button } from 'antd';
import { Player } from 'video-react';
import background from "../assets/imgs/background.png";
import PopUp from "./Popup"; 
// import {Backdrop} from '@mui/material';
import Backdrop from "@material-ui/core/Backdrop";
// import Button from "@material-ui/core/Button";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";


class Baby extends Component {
  
    constructor(props) {
        super(props)
        this.state = {
            setButtonPopup:false,
            open:true
        }
    }
    // useStyles = makeStyles(() => ({
    //     backdrop: {
    //       zIndex: 5
    //     },
    // }));

    handleSelect(index){
        this.setState({
            setButtonPopup: !this.state.setButtonPopup
        })
        window.index = index
    }

    render() {
        return (
            
            <div>
            
            <div class='bg' style={{ backgroundImage: `url(${background})`  }} >
                <div>
                    <Top e='1' />
                        <div class = 'section'>
                            {window.babyinfo.map(item => (
                                <li key={item.id}>
                                    
                                    <div class={'profile'+ item.id}>
                                        <div class='babyimg'>
                                            <img class='image' src={require("../assets/imgs/baby"+item.id+".png")}>
                                            </img>
                                            <div class="babyhover">
                                                <div class='babybutton'>
                                                    <Button type="primary" size="large" onClick={() => this.handleSelect(item.id)}>Select</Button>
                                                </div>
                                            </div>
                                        </div>

                                        <div class='babyinfo'>
                                            <span>Name: {item.name} <br/> Age: {item.month} months <br/> Gender: {item.gender} </span>
                                        </div>  
                                    </div> 
                                </li>
                            ))}

                        </div>
                        
                </div>
            </div>
       
            <Backdrop
            // className={this.useStyles.backdrop}
            // sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
            open={this.state.setButtonPopup}
            style={{zIndex: 2}} 
            >
            {this.state.setButtonPopup ? <PopUp toggle={() => this.setState({setButtonPopup:!this.state.setButtonPopup})} /> : null}
            
            </Backdrop> 
            </div>
       
            
        );
    }
}

export default Baby;
