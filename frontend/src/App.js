import React, { Component } from 'react';
import startImg from './smallpic.jpg';
import './App.css';
import {Button} from 'react-bootstrap';
import 'whatwg-fetch';
import Dropzone from 'react-dropzone';

class App extends Component {
  constructor(props) {
      super(props);
      this.state = {
        img: startImg,
      };
      this.getBase64Image = this.getBase64Image.bind(this);
      this.onDZDrop = this.onDZDrop.bind(this);
      this.onDZClick = this.onDZClick.bind(this);
      this.postApi = this.postApi.bind(this);
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

  postApi() {
    fetch('https://imagefeaturewebapp.herokuapp.com/api/v1/featureprocessing', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          imgData: this.getBase64Image(),
        })
    }).then( (response) => {
      return response.blob();

    }).then( (blob) => {
      this.setState({ img: URL.createObjectURL(blob) });
  })
  }

  render() {
    return (
      <div className="App">

        <div className='header'>
          <h1>Computer Vision Feature Analysis</h1>
        </div>

        <div className='contentContainer'>

          <div className='imageContainer'>
            <Dropzone 
            ref={(node) => { this.dropzone = node; }} 
            onDrop={this.onDZDrop}
            className='dropzone'>
            
            <img id='mainImg' src={this.state.img}   alt="img" />

            </Dropzone>
          </div>

          <div className='controlsContainer'>
            <Button onClick={this.postApi}> Send to api </Button>
          </div>
        </div>

      </div>
    );
  }
}

export default App;


        // <div className="App-header">
        //   <img src={logo} className="App-logo" alt="logo" />
        //   <h2>Welcome to React</h2>
        // </div>
        // <p className="App-intro">
        //   To get started, edit <code>src/App.js</code> and save to reload.
        // </p>
        // <Button> Super text</Button>