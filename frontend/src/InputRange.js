import React, { Component } from 'react';

class InputRange extends Component {
    constructor(props){
        super(props);
        this.updateInputBox = this.updateInputBox.bind(this);
        this.updateSlider = this.updateSlider.bind(this);
    }

    updateInputBox(){
        document.getElementById(this.props.label).value = document.getElementById(this.props.label+'slider').value;
        this.props.callBack();
    }

    updateSlider(){
        document.getElementById(this.props.label+'slider').value = document.getElementById(this.props.label).value;
        this.props.callBack();
    }

    render() {
      return (
        <div className='setting'>
          <h5>{this.props.label}: </h5>
          
          <input className='inputBoxes' id={this.props.label} type='number' 
          value={this.props.value} onChange={this.updateSlider}
          min={this.props.min} step={this.props.step} /> 

          <input className='inputSliders' id={this.props.label+'slider'} type='range' 
          value={this.props.value}  onChange={this.updateInputBox} 
          min={this.props.min} max={this.props.max} step={this.props.step} />
        </div>
      );
    }

}

export default InputRange;