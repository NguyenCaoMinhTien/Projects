import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, ImageBackground} from 'react-native';



const MainScreen = () => (
    <ImageBackground 
      source={require('./images/homebackground.jpg')}
      style={styles.homeBackground}
    >
      <Text style={styles.logo}>HP-EYE</Text>
      <View style={styles.LibContainer}>
          
      </View>
    </ImageBackground>
);

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#fff", // Thay đổi màu nền nếu cần
    },
    homeBackground:{
        flex: 1,
        resizeMode:'cover',
        justifyContent: 'top',
        alignItems: 'center',
      },
      LibContainer:{
        position:'absolute',
        backgroundColor:'white',
        height: '100%' ,
        width: '100%',
        marginTop: 100,
        borderRadius: 30,
      },
      logo: {
        marginTop: 50,
        fontFamily: 'times new roman',
        fontWeight: 'bold',
        fontSize: 25
      },
  });


export default MainScreen;