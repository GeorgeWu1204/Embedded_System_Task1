import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
// import registerServiceWorker from './registerServiceWorker';
// import List from './list'
import Baby from './components/Baby'
import { Router, Route, hashHistory } from 'react-router';

ReactDOM.render((
    <Router history={hashHistory}>
        <Route path='/' component={App}></Route>
        <Route path='/Baby' component={Baby}></Route>
        {/* <Route path='/list' component={List}></Route> */}
    </Router>
), document.getElementById('root1'));
// registerServiceWorker();
