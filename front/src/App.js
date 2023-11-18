import React, { useState, useEffect } from 'react';
import "./App.css";
import { HeaderApp } from "./componentes/HeaderApp";

function App() {
  const [selectedImage, setSelectedImage] = useState(null);

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

  useEffect(() => {
    // Set a default title when no image is selected
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
          <button className="button">
            <span className="buttonText">Procesar imagen</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
