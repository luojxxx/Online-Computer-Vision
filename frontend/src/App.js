import React, { Component } from 'react';
import startImg from './smallpic.jpg';
import './App.css';
import {Button } from 'react-bootstrap';
import 'whatwg-fetch';
import Dropzone from 'react-dropzone';
import InputRange from './InputRange';

class App extends Component {
  constructor(props) {
      super(props);
      this.state = {
        img: startImg,
        edgeImg: null,
        lineImg: null,
        cornerImg: null,
        edgeMinVal: 5,
        edgeMaxVal: 25,
        lineRho: 1,
        lineTheta: (3.14/180),
        lineThreshold: 100,
        lineMinLength: 100,
        lineMaxGap: 10,
        cornerBlockSize: 2,
        cornerKSize: 3,
        cornerK: 0.04,
      };
      this.debounce = this.debounce.bind(this);
      this.getBase64Image = this.getBase64Image.bind(this);
      this.onDZDrop = this.onDZDrop.bind(this);
      this.onDZClick = this.onDZClick.bind(this);
      this.getFormInfo = this.getFormInfo.bind(this);
      this.onUpdate = this.onUpdate.bind(this);
      this.postApi = this.postApi.bind(this);
      this.postApi = this.debounce(this.postApi, 1000);
  }

  componentDidMount() {
    document.getElementById('minVal').value = this.state.edgeMinVal;
    document.getElementById('maxVal').value = this.state.edgeMaxVal;
    document.getElementById('rho').value = this.state.lineRho;
    document.getElementById('theta').value = this.state.lineTheta;
    document.getElementById('threshold').value = this.state.lineThreshold;
    document.getElementById('line minLength').value = this.state.lineMinLength;
    document.getElementById('line maxGap').value = this.state.lineMaxGap;
    document.getElementById('block size').value = this.state.cornerBlockSize;
    document.getElementById('k size').value = this.state.cornerKSize;
    document.getElementById('k').value = this.state.cornerK;
  }

  debounce(fn, delay) {
    var timer = null;
    return function () {
      var context = this, args = arguments;
      clearTimeout(timer);
      timer = setTimeout(function () {
        fn.apply(context, args);
      }, delay);
    };
  }

  getBase64Image() {
      var imgElem = document.getElementById("mainImg");
      var canvas = document.createElement("canvas");
      canvas.width = imgElem.clientWidth;
      canvas.height = imgElem.clientHeight;
      var ctx = canvas.getContext("2d");
      ctx.drawImage(imgElem, 0, 0);
      var dataURL = canvas.toDataURL("image/png");
      return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
  }

  onDZDrop(files) {
      var imgSrc = URL.createObjectURL(files[0]);
      this.setState({ img:imgSrc });
  }

  onDZClick(evt) {
      evt.preventDefault();
      this.dropzone.open();
  }

  getFormInfo() {
     return {
          edgeMinVal: document.getElementById('minVal').value,
          edgeMaxVal: document.getElementById('maxVal').value,
          lineRho: document.getElementById('rho').value,
          lineTheta: document.getElementById('theta').value,
          lineThreshold: document.getElementById('threshold').value,
          lineMinLength: document.getElementById('line minLength').value,
          lineMaxGap: document.getElementById('line maxGap').value,
          cornerBlockSize: document.getElementById('block size').value,
          cornerKSize: document.getElementById('k size').value,
          cornerK: document.getElementById('k').value,
        }
  }

  onUpdate(evt) {
    // evt.preventDefault();
    this.setState(this.getFormInfo());
    this.postApi();
  }

  postApi() {
    const allData = Object.assign({}, this.getFormInfo(), {'imgData': this.getBase64Image()} );

    fetch('https://imagefeaturewebapp.herokuapp.com/api/v1/featureprocessing', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(allData)
    }).then( (response) => {
      return response.json();

    }).then( (json) => {
      this.setState({ 
        edgeImg: 'data:image/png;base64,' + json.edgeImg,
        lineImg: 'data:image/png;base64,' + json.lineImg,
        cornerImg: 'data:image/png;base64,' + json.cornerImg });
    })
  }

  render() {
    return (
      <div className="App">

        <div className='header'>
          <h1>Terminator Vision - Search Mode</h1>
        </div>

        <div className='contentContainer'>

          <div className='imageContainer'>
            <Dropzone 
            ref={(node) => { this.dropzone = node; }} 
            onDrop={this.onDZDrop}
            className='dropzone'>
            <img id='mainImg' src={this.state.img}  />
            <img id='mainImg' src={this.state.edgeImg}  />
            <img id='mainImg' src={this.state.lineImg}  />
            <img id='mainImg' src={this.state.cornerImg}  />
            </Dropzone>
          </div>

          <div className='controlsContainer'>

            <h2>Canny Edge Settings</h2>
            <div className='settingsContainer'>
              
              <InputRange label='minVal' value={this.state.edgeMinVal} callBack={this.onUpdate}
              min='0' max='100' step='0.1' />
              <InputRange label='maxVal' value={this.state.edgeMaxVal} callBack={this.onUpdate}
              min='0' max='100' step='0.1' />
              
            </div>

            <h2>Hough Line Settings</h2>
            <div className='settingsContainer'>
              
              <InputRange label='rho' value={this.state.lineRho} callBack={this.onUpdate}
              min='0' max='100' step='0.1' />
              <InputRange label='theta' value={this.state.lineTheta} callBack={this.onUpdate}
              min='0' max='100' step='0.0001' />
              <InputRange label='threshold' value={this.state.lineThreshold} callBack={this.onUpdate}
              min='0' max='100' step='1' />
              <InputRange label='line minLength' value={this.state.lineMinLength} callBack={this.onUpdate}
              min='0' max='100' step='0.1' />
              <InputRange label='line maxGap' value={this.state.lineMaxGap} callBack={this.onUpdate}
              min='0' max='100' step='0.1' />
              
            </div>

            <h2>Harris Corner Settings</h2>
            <div className='settingsContainer'>
              
              <InputRange label='block size' value={this.state.cornerBlockSize} callBack={this.onUpdate}
              min='0' max='100' step='1' />
              <InputRange label='k size' value={this.state.cornerKSize} callBack={this.onUpdate}
              min='1' max='31' step='2' />
              <InputRange label='k' value={this.state.cornerK} callBack={this.onUpdate}
              min='0' max='1' step='0.01' />
              
            </div>

            <br />
            <Button onClick={this.postApi}> Send to api </Button>
          </div>
        </div>

      </div>
    );
  }
}

export default App;