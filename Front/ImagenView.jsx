import React from 'react';
import { View, Text, Image, TouchableOpacity, StyleSheet } from 'react-native';

const ImagenView = ({ route }) => {
  // const { capturedImage } = route.params;

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={[styles.rectangle, { backgroundColor: '#748CAB' }]} />
        <Image source={require('./logo.png')} style={styles.logo} />
        <View style={[styles.rectangle, { backgroundColor: '#F0EBD8' }]} />
      </View>
      <View style={styles.content}>
        {/* Display the captured image */}
        {/* <Image source={{ uri: capturedImage }} style={styles.capturedImage} /> */}
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>Reintentar imagen</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>Procesar imagen</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};
const styles = StyleSheet.create({
  container: {
    flex: 1,
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
    width: 300,
    height: 60,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  text_title: {
    color: '#748CAB',
    fontSize: 20,
    marginBottom: 10,
  },
  capturedImage: {
    width: 300,
    height: 200,
    resizeMode: 'cover',
    marginBottom: 20,
  },
});

export default ImagenView;
