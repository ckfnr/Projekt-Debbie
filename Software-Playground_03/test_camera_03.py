from flask import Flask, Response, render_template_string  #type:ignore[import-untyped]
from picamera2 import Picamera2  #type:ignore
import cv2
import threading

app = Flask(__name__)
picam2 = Picamera2()

def configure_camera():
    picam2.stop()
    picam2.configure(picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, controls={"FrameRate": 30}))
    picam2.start()

def generate_frames():
    while True:
        frame = picam2.capture_array()
        frame = cv2.rotate(frame, cv2.ROTATE_180)  # Turn image 180°
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template_string('''
    <html>
    <head>
        <style>
            body { text-align: center; background-color: black; color: white; font-family: Arial, sans-serif; }
            img { width: 50%; border: 2px solid white; }
            .buttons { margin-top: 20px; }
            button { margin: 5px; padding: 10px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>Live Camera Stream</h1>
        <img src='/video_feed' />
    </body>
    </html>
    ''')

if __name__ == '__main__':
    configure_camera()
    app.run(host='0.0.0.0', port=5000, debug=False)
