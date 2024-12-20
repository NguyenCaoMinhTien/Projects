import React, { useState, useCallback, useEffect, useRef  } from "react";
import { View, Text, TouchableOpacity, StyleSheet, Button, SafeAreaView } from 'react-native';
import { Camera } from 'expo-camera';
import { Video } from 'expo-av';
import { shareAsync } from 'expo-sharing';
import * as MediaLibrary from 'expo-media-library';

const LiveScreen = () => {
  let cameraRef = useRef(); // Tham chiếu tới camera, dùng để truy cập các phương thức camera.
  const [hasCameraPermission, setHasCameraPermission] = useState(null); // Trạng thái quyền camera.
  const [hasMicrophonePermission, setHasMicrophonePermission] = useState(null); // Trạng thái quyền microphone.
  const [hasMediaLibraryPermission, setHasMediaLibraryPermission] = useState(null); // Trạng thái quyền truy cập thư viện media.
  const [isRecording, setIsRecording] = useState(false); // Trạng thái ghi hình.
  const [video, setVideo] = useState(null); // Đối tượng video được ghi lại.

  useEffect(() => {
    (async () => {
      // Yêu cầu các quyền truy cập cần thiết.
      const cameraPermission = await Camera.requestCameraPermissionsAsync();
      const microphonePermission = await Camera.requestMicrophonePermissionsAsync();
      const mediaLibraryPermission = await MediaLibrary.requestPermissionsAsync();

      // Lưu trạng thái quyền truy cập.
      setHasCameraPermission(cameraPermission.status === "granted");
      setHasMicrophonePermission(microphonePermission.status === "granted");
      setHasMediaLibraryPermission(mediaLibraryPermission.status === "granted");
    })();
  }, []); // useEffect chỉ chạy một lần khi component được mount.

  // Xử lý khi chưa xác định được quyền truy cập hoặc không được cấp quyền.
  if (hasCameraPermission === undefined || hasMicrophonePermission === undefined) {
    // Hiển thị thông báo đang yêu cầu quyền truy cập.
    return <View style={styles.text1}><Text style={{fontSize: 20 }}>Đang gửi yêu cầu...</Text></View>
  } else if (!hasCameraPermission) {
    // Hiển thị thông báo không thể truy cập camera.
    return <View style={styles.text1}><Text style={{fontSize: 20 }}>Không thể truy cập vào camera</Text></View>
  }

  // Hàm bắt đầu ghi hình.
  let recordVideo = async () => {
    setIsRecording(true); // Đặt trạng thái đang ghi hình.
    let options = {
      quality: "1080p", // Chất lượng video.
      mute: true, // Tắt tiếng trong video.
    };
    cameraRef.current.recordAsync(options).then((recordedVideo) => {
      // Lưu video vào state sau khi ghi xong.
      setVideo(recordedVideo);
      setIsRecording(false); // Tắt trạng thái ghi hình.
    });
  };

  // Hàm dừng ghi hình.
  let stopRecording = async () => {
    setIsRecording(false); // Tắt trạng thái ghi hình.
    cameraRef.current.stopRecording(); // Gọi hàm dừng ghi của camera.
  }

  // Xử lý khi video đã được ghi.
  if (video) {
    let shareVideo = async () => {
      // Chia sẻ video.
      shareAsync(video.uri).then(() => {
        setVideo(undefined); // Xóa video sau khi chia sẻ.
      });
    }

    let saveVideo = () => {
      // Lưu video vào thư viện media.
      MediaLibrary.saveToLibraryAsync(video.uri).then(() => {
        setVideo(undefined); // Xóa video khỏi state sau khi lưu.
      });
    };

    return (
      <SafeAreaView style={styles.container}>
        <Video
          style={styles.video}
          source={{uri: video.uri}} // Đường dẫn của video đã ghi.
          useNativeControls
          resizeMode="contain"
          isLooping
        /> 
        <Button title="Share" onPress={shareVideo}/> {/* Nút chia sẻ video */}
        {hasMediaLibraryPermission ? <Button title="Save" onPress={saveVideo} /> : undefined} {/* Nút lưu video */}
        <Button title="Discard" onPress={() => setVideo(undefined)}/> {/* Nút xóa video */}
      </SafeAreaView>
    );
  }

  return (
    <Camera style={styles.container} 
      ref={cameraRef} // Tham chiếu camera để gọi các phương thức.
    >
      <View style={styles.overlay}>
        <Button title={isRecording ? "Stop Recording" : "Record Video"} onPress={isRecording ? stopRecording : recordVideo} /> {/* Nút bắt đầu/dừng ghi hình */}
      </View>
    </Camera>
  );
};
const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  centered: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#fff",
  },
  text: {
    fontSize: 20,
    textAlign: "center",
  },
  camera: {
    flex: 1,
  },
  overlay: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  overlayText: {
    color: "#fff",
    fontSize: 18,
  },
});

export default LiveScreen;