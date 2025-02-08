from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import io

app = Flask(__name__)
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}, controls={"FrameRate": 60}))
picam2.start()


def generate_frames():
    while True:
        frame = picam2.capture_array()
        frame = cv2.rotate(frame, cv2.ROTATE_180)  # Rotate 180 degrees

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "<h1>Raspberry Pi Camera Stream</h1><img src='/video_feed' width='640' height='480'/>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
