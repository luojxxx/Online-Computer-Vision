import React, { Component } from 'react';

class InputRange extends Component {
    constructor(props){
        super(props);
        this.updateSlider = this.updateSlider.bind(this);
    }

    updateSlider(){
        document.getElementById(this.props.label).value = document.getElementById(this.props.label+'box').value;
        this.props.callBack();
    }

    render() {
      return (
        <div className='setting'>
          <h5>{this.props.label}: </h5>
          <input id={this.props.label+'box'} type='number' value={this.props.value} onChange={this.updateSlider}
          min={this.props.min} max={this.props.max} step={this.props.step} /> 
          <input id={this.props.label} type='range' onChange={this.props.callBack} 
          min={this.props.min} max={this.props.max} step={this.props.step} />
        </div>
      );
    }

}

export default InputRange;