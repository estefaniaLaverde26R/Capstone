import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Index } from './vistas/index';
import "./App.css";
import { HeaderApp } from "./componentes/HeaderApp";
import axios from "axios";

function App() {

  return (
    <Router>
      <Routes>
        <Route index element={<Index />} />
        <Route path='/inicio' element={<Index />} />
        {/* <Route path='/analisis' element={<Analisis />} /> */}
      </Routes>
    </Router>
  );
}

export default App;
