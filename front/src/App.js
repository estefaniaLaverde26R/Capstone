import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Index } from './vistas/index';
import { Analisis } from './vistas/analisis';
import "./App.css";
import { HeaderApp } from "./componentes/HeaderApp";
import axios from "axios";

function App() {

  return (
    <Router>
      <Routes>
        <Route index element={<Analisis />} />
        <Route path='/analisis' element={<Analisis />} />
        {/* <Route path='/analisis' element={<Analisis />} /> */}
      </Routes>
    </Router>
  );
}

export default App;
