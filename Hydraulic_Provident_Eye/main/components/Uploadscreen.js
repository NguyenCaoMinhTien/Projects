import React, { useState } from "react";
import { View, Button, Text, StyleSheet, ActivityIndicator } from "react-native";
import * as ImagePicker from "expo-image-picker";
import * as FileSystem from "expo-file-system";
import axios from "axios";
import { Video } from "expo-av"; // Using expo-av for video playback
import { Buffer } from "buffer";

const UploadScreen = () => {
  const [uploaded, setUploaded] = useState(false);
  const [videoUri, setVideoUri] = useState(null);
  const [loading, setLoading] = useState(false);
  const [processing, setProcessing] = useState(false);

  const pickAndUploadVideo = async () => {
    // Reset state cũ
    setUploaded(false);
    setVideoUri(null);
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permission.granted) {
      alert("Permission denied!");
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Videos,
    });

    if (!result.canceled) {
      const formData = new FormData();
      formData.append("video", {
        uri: result.assets[0].uri,
        name: "uploaded_video.mp4",
        type: "video/mp4",
      });

      try {
        setLoading(true);
        await axios.post("http://192.168.1.11:3000/upload", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        setLoading(false);
        console.log("Upload successful! Processing video...");
        fetchProcessedVideo();
      } catch (error) {
        setLoading(false);
        console.error("Upload error:", error);
        alert("Upload failed!");
      }
    }
  };
  
  const [progress, setProgress] = useState(0); // Thêm state để lưu tiến độ

  const fetchProcessedVideo = async () => {
    setProcessing(true);
    setProgress(0); // Khởi tạo tiến độ là 0%
  
    try {
      const videoResponse = await axios.get("http://192.168.1.11:5000/video", {
        responseType: "arraybuffer",
        onDownloadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setProgress(percentCompleted); // Cập nhật state tiến độ
        },
      });
  
      const localVideoUri = `${FileSystem.documentDirectory}processed_video.mp4`;
  
      await FileSystem.writeAsStringAsync(
        localVideoUri,
        Buffer.from(videoResponse.data, "binary").toString("base64"),
        { encoding: FileSystem.EncodingType.Base64 }
      );
  
      setVideoUri(localVideoUri);
      setUploaded(true);
    } catch (error) {
      console.error("Error fetching video:", error);
      alert("Failed to fetch processed video!");
    } finally {
      setProcessing(false);
    }
  };

  return (
    <View style={styles.container}>
      <Button title="Upload Video" onPress={pickAndUploadVideo} color='black'/>
      {loading && <ActivityIndicator size="large" color="#0000ff" />}
      {processing && (
        <View style={{ width: "80%", marginVertical: 10 }}>
          <Text style={styles.text}>Processing: {progress}%</Text>
          <View style={{ height: 10, backgroundColor: "#e0e0e0", borderRadius: 5 }}>
            <View
              style={{
                width: `${progress}%`,
                height: "100%",
                backgroundColor: "#007BFF",
                borderRadius: 5,
              }}
            />
          </View>
        </View>
      )}
      {uploaded && videoUri ? (
        <>
          <Text style={styles.text}>Streaming Processed Video:</Text>
          <Video
            source={{ uri: videoUri }}
            style={styles.video}
            useNativeControls
            resizeMode="contain"
            shouldPlay
            isLooping
          />
        </>
      ) : (
        !loading &&
        !processing && (
          <Text style={styles.text}>Upload a video to start processing!</Text>
        )
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "white",
    padding: 20,
  },
  text: {
    fontSize: 16,
    fontWeight: "bold",
    marginVertical: 10,
    color: "#333",
    textAlign: "center",
  },
  video: {
    width: '105%',
    height: '40%',
    backgroundColor: "black",
    borderRadius: 10,
    marginTop: 10,
  },
});

export default UploadScreen;
