import React, { useState, useEffect } from 'react';
import "./App.css";
import { HeaderApp } from "./componentes/HeaderApp";
import axios from "axios";

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];

    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result);
      };
      reader.readAsDataURL(file);

      document.title = `Análisis de imagen - ${file.name}`;
    }
  };

  const handleProcessImage = async () => {
    if (!selectedImage) {
      console.error('No image selected');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await axios.post('http://localhost:5000/', formData);
      setProcessedImage(response.data.processedImage);
    } catch (error) {
      console.error('Error processing image:', error);
    }
  };

  useEffect(() => {
    document.title = 'Análisis de imagen';
  }, []);

  return (
    <div className="App">
      <HeaderApp />
      <div className="content">
        <label htmlFor="foto">Seleccione la imagen a analizar: 
          <input
            type="file"
            id="foto"
            accept="image/png, image/gif, image/jpeg"
            onChange={handleImageChange}
          />
        </label>
        {selectedImage && (
          <img
            src={selectedImage}
            alt="selectedImage"
            className="capturedImage"
          />
        )}
        <div className='container-buttons'>
          <button className="button" onClick={handleProcessImage}>
            <span className="buttonText">Procesar imagen</span>
          </button>
        </div>
        {processedImage && (
          <div>
            <h2>Imagen procesada:</h2>
            <p>{processedImage}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
