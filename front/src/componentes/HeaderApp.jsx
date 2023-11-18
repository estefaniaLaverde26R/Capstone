// import logo from "./../logo.png";
import React from 'react'

export const HeaderApp = () => {
  return (
    <div className="header">
      <div className="rectangle" style={{ backgroundColor: "#748CAB" }} />
      <img src={require('../logo.png')} alt="logo" className="logo" />
      <div className="rectangle" style={{ backgroundColor: "#F0EBD8" }} />
    </div>
  );
}
