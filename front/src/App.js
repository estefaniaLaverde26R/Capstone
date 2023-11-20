import React, { useState, useEffect } from 'react';
import "./App.css";
import { HeaderApp } from "./componentes/HeaderApp";
import axios from "axios";

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedImageCompare, setCompareImage] = useState(null);
  const [imgSend, setImg] = useState(null);
  const [imgSend2, setImg2] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImg(file);

    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result);
      };
      reader.readAsDataURL(file);
      console.log(file.name);

      document.title = `Análisis de imagen - ${file.name}`;
    }
  };

  const handleImageChange2 = (e) => {
    const file = e.target.files[0];
    setImg2(file);

    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setCompareImage(reader.result);
      };
      reader.readAsDataURL(file);
      console.log(file.name);
    }
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append('image', imgSend);
    formData.append('image2', imgSend2);

    axios.post('http://localhost:5000/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
      .then(response => {
        console.log('Upload successful:', response.data);
      })
      .catch(error => {
        console.error('Error uploading image:', error);
      });
  };

  return (
    <div className="App">
      <HeaderApp />
      <div className="content">
        <label htmlFor="foto">Seleccione la primera imagen: 
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
        <label htmlFor="foto">Seleccione la segunda imagen: 
          <input
            type="file"
            id="foto"
            accept="image/png, image/gif, image/jpeg"
            onChange={handleImageChange2}
          />
        </label>
        {selectedImageCompare && (
          <img
            src={selectedImageCompare}
            alt="selectedImage"
            className="capturedImage"
          />
        )}
        <div className='container-buttons'>
          <button className="button" onClick={handleUpload}>
            <span className="buttonText">Procesar imagenes</span>
          </button>
        </div>
        {/* {processedImage && (
          <div>
            <h2>Imagen procesada:</h2>
            <p>{processedImage.message}</p>
          </div>
        )} */}
      </div>
    </div>
  );
}

export default App;
