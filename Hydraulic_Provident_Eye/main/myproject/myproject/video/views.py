from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from SwimmingDetector import SwimmingDetector  # Đảm bảo đường dẫn đúng

class VideoProcessView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        video_file = request.FILES.get('video')
        if not video_file:
            return Response({'error': 'No video uploaded'}, status=400)

        # Lưu video tạm thời
        temp_video_path = f'/tmp/{video_file.name}'
        with open(temp_video_path, 'wb+') as f:
            for chunk in video_file.chunks():
                f.write(chunk)

        # Khởi tạo và sử dụng SwimmingDetector
        detector = SwimmingDetector()
        result = detector.detect(temp_video_path)

        # Xóa video tạm thời nếu cần

        return Response({'message': 'Video processed successfully', 'result': result}, status=200)
