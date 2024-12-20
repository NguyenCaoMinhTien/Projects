const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const { exec } = require("child_process"); // Thêm child_process để chạy file Python

const app = express();
const PORT = 3000;

// Đường dẫn đến thư mục lưu trữ video
const mediaDir = path.join(__dirname,"myproject", "myproject", "video");

// Kiểm tra và tạo thư mục nếu chưa tồn tại
if (!fs.existsSync(mediaDir)) {
  fs.mkdirSync(mediaDir, { recursive: true });
  console.log(`Created directory: ${mediaDir}`);
}

// Cấu hình lưu trữ video với tên cố định
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, mediaDir); // Thư mục lưu video
  },
  filename: (req, file, cb) => {
    cb(null, "uploaded_video.mp4");
  },
});

const upload = multer({ storage });

// API để upload video và chạy file main.py
app.post("/upload", upload.single("video"), (req, res) => {
  console.log("processing uploaded video");
  if (!req.file) {
    console.log("error no file");
    return res.status(400).send("No file uploaded.");
  }
  console.log("successfully uploaded")
  return res.status(200).send("Video uploaded successfully");
  // Chạy file main.py
  // const pythonScript = path.join(__dirname,"myproject",  "myproject","video", "process.py");
  // exec(`python ${pythonScript}`, (error, stdout, stderr) => {
  //   if (error) {
  //     console.error(`Error running Python script: ${error.message}`);
  //     return res.status(500).send("Error running main.py");
  //   }
  //   if (stderr) {
  //     console.error(`Python stderr: ${stderr}`);
  //   }
  //   console.log(`Python stdout: ${stdout}`);
  //   return res.status(200).json({
  //     message: "File uploaded successfully and main.py executed!",
  //     filename: "uploaded_video.mp4",
  //   });
  // });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
