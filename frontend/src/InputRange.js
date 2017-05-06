import React, { Component } from 'react';

class InputRange extends Component {
  render() {
    return (
      <div className='setting'>
        <h5>{this.props.label}: {this.props.value}</h5>
        <input id={this.props.label} type='range' onChange={this.props.callBack} 
        min={this.props.min} max={this.props.max} step={this.props.step} />
      </div>
    );
  }
}

export default InputRange;