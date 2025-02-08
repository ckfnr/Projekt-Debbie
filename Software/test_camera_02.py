from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import io

app = Flask(__name__)
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, controls={"FrameRate": 30}))
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

@app.route('/resources')
def resources():
    return "Framerate: 30, Resolution: 640x480"

@app.route('/')
def index():
    return """
    <html>
    <head>
        <style>
            body {
                margin: 0;
                background-color: black;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                overflow: hidden;
            }
            img {
                width: 100vw;
                height: 100vh;
                object-fit: cover;
            }
        </style>
    </head>
    <body>
        <img src='/video_feed' />
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
