import React, { useState, useEffect } from 'react';
import { HeaderApp } from "./../componentes/HeaderApp";
import base from "../images/resultado_preliminar_colores.png";
import comparison from "../images/resultado_comparacion_colores.png";
import axios from "axios";

export const Analisis = () => {
  
    const [processedImage, setProcessedImage] = useState(null);

    useEffect(() => {
      // You can fetch and display the image when the component mounts
      axios.get('http://localhost:5000/analisis', {
        responseType: 'arraybuffer',
      })
        .then(response => {
          const base64Image = Buffer.from(response.data, 'binary').toString('base64');
          setProcessedImage(`data:image/png;base64,${base64Image}`);
        })
        .catch(error => {
          console.error('Error fetching image:', error);
        });
    }, []);
  
    return (
      <div className="App">
        <HeaderApp />
        <img src={base}/>
        <img src={comparison}/>
        <div className="content">
        <h1>Resultado de comparación</h1>
        
        </div>
      </div>
    );
  };
