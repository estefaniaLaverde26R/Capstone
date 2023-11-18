// App.js
import React, { useState, useRef } from 'react';
import { View, Text, Image, TouchableOpacity, StyleSheet } from 'react-native';
import { RNCamera } from 'react-native-camera';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import ImagenView from './ImagenView';
import RNFS from 'react-native-fs';

const Stack = createStackNavigator();

const App = ({ navigation }) => {
  const cameraRef = useRef(null);
  const [isCameraOpen, setCameraOpen] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);

  const openCamera = () => {
    setCameraOpen(true);
  };

  const closeCamera = () => {
    setCameraOpen(false);
  };

  const takePicture = async () => {
    if (cameraRef.current) {
      const options = { quality: 0.5, base64: true };
      const data = await cameraRef.current.takePictureAsync(options);
      console.log(data.uri);

      // Save the image using react-native-fs
      const destinationPath = RNFS.DocumentDirectoryPath + '/capturedImage.jpg';
      await RNFS.moveFile(data.uri, destinationPath);

      setCapturedImage(destinationPath);
      closeCamera();

      // Navigate to ImagenView with the captured image URI
      navigation.navigate('ImagenView', { capturedImage: destinationPath });
    }
  };

  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Home"
          component={() => (
            <View style={styles.container}>
              {isCameraOpen ? (
                <RNCamera
                  ref={cameraRef}
                  style={styles.camera}
                  type={RNCamera.Constants.Type.back}
                  captureAudio={false}
                >
                  <TouchableOpacity style={styles.closeButton} onPress={closeCamera}>
                    <Text style={styles.closeButtonText}>Cerrar cámara</Text>
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.captureButton} onPress={takePicture}>
                    <Text style={styles.captureButtonText}>Tomar foto</Text>
                  </TouchableOpacity>
                </RNCamera>
              ) : (
                <>
                  <View style={styles.header}>
                    <View style={[styles.rectangle, { backgroundColor: '#748CAB' }]} />
                    <Image
                      source={require('./logo.png')}
                      style={styles.logo}
                    />
                    <View style={[styles.rectangle, { backgroundColor: '#F0EBD8' }]} />
                  </View>
                  <View style={styles.content}>
                    <TouchableOpacity
                      style={styles.button}
                      onPress={() => navigation.navigate('ImagenView', { capturedImage })}
                    >
                      <Text style={styles.buttonText}>Conectar</Text>
                    </TouchableOpacity>
                    <Text style={styles.text_title}>Estado:</Text>
                    <Text style={styles.text_estado}>Your text 2</Text>
                    <TouchableOpacity style={styles.button_camara} onPress={openCamera}>
                      <Text style={styles.buttonText_camara}>Abrir cámara</Text>
                    </TouchableOpacity>
                  </View>
                </>
              )}
            </View>
          )}
        />
        <Stack.Screen name="ImagenView" component={ImagenView} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF', // Set your background color
  },
  header: {
    flexDirection: 'column',
    justifyContent: 'space-between',
    alignItems: 'center',
    width: '100%',
  },
  rectangle: {
    width: '100%',
    height: 60,
  },
  logo: {
    width: '90%',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#D9D9D9',
  },
  button: {
    backgroundColor: '#1D2D44',
    borderRadius: 100,
    paddingVertical: 15,
    paddingHorizontal: 30,
    marginBottom: 20,
    width: 150,
    height: 150,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  button_camara: {
    backgroundColor: '#1D2D44',
    borderRadius: 100,
    paddingVertical: 15,
    paddingHorizontal: 30,
    marginTop: 20,
    height: 50,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  buttonText_camara: {
    color: 'white',
    fontSize: 10,
    fontWeight: 'bold',
  },
  text_title: {
    color: '#748CAB',
    fontSize: 20,
    marginBottom: 10,
  },
  camera: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center',
  },
  captureButton: {
    alignSelf: 'center',
    margin: 20,
    backgroundColor: 'white',
    borderRadius: 5,
    padding: 15,
  },
  captureButtonText: {
    fontSize: 20,
    color: 'black',
  },
  closeButton: {
    position: 'absolute',
    top: 20,
    left: 20,
    backgroundColor: 'white',
    borderRadius: 5,
    padding: 10,
  },
  closeButtonText: {
    fontSize: 16,
    color: 'black',
  },
});

export default App;
