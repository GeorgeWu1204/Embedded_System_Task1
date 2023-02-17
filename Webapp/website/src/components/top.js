import React, { Component } from 'react';
import './top.css';
import {Link} from 'react-router'
import {Battery} from 'react-little-icon'
import {  Row, InputNumber  } from 'antd';
class Top extends Component {
    constructor(props){
        super(props)
        this.state={
            menudata:[
                {name:'Home',path:'/',icon:'iconfont icon-shouye'},
                {name:'My Babies',path:'/Baby',icon:'iconfont icon-dingxiang'},
            ],
            e:props.e,
            dl:80
        }
    }

    // btnClick(val,e){
    //     this.setState({
    //         e
    //     })
    //     this.props.router.push(val.path)
    // }
    render() {
        return (
            <div class='tops'>
                <div class='center'>
                    <div class='menus'>
                        {this.state.menudata.map((item, index) => {
                            return <div 
                            class={['list',index==this.state.e?'active':null].join(' ')}
                            key={index}>
                                    <Link to={item.path}>
                                    <span class={item.icon}>  {item.name} </span></Link></div>
                        })}
                    </div>
                </div>
            </div>
        );
    }
}

export default Top;
