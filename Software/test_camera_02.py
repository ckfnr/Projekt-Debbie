from flask import Flask, Response, render_template_string
from picamera2 import Picamera2  #type:ignore
import cv2
import threading

app = Flask(__name__)
picam2 = Picamera2()

# Standardauflösung
resolutions = {
    "low": (320, 240),
    "medium": (640, 480),
    "high": (1280, 720),
    "ultra": (1920, 1080)
}
current_resolution = "medium"

def configure_camera(res):
    picam2.stop()
    picam2.configure(picam2.create_video_configuration(main={"size": resolutions[res], "format": "RGB888"}, controls={"FrameRate": 30}))
    picam2.start()

def generate_frames():
    while True:
        frame = picam2.capture_array()
        frame = cv2.rotate(frame, cv2.ROTATE_180)  # Bild um 180 Grad drehen
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_resolution/<res>')
def set_resolution(res):
    global current_resolution
    if res in resolutions:
        current_resolution = res
        threading.Thread(target=configure_camera, args=(res,)).start()
    return render_template_string('''
    <html>
    <head>
        <style>
            body { text-align: center; background-color: black; color: white; font-family: Arial, sans-serif; }
            img { width: 80%; border: 2px solid white; }
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
        <h1>Live Camera Stream Debbie</h1>
        <div class='buttons'>
            <button onclick="location.href='/set_resolution/low'">320x240</button>
            <button onclick="location.href='/set_resolution/medium'">640x480</button>
            <button onclick="location.href='/set_resolution/high'">1280x720</button>
            <button onclick="location.href='/set_resolution/ultra'">1920x1080</button>
        </div>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    configure_camera(current_resolution)
    app.run(host='0.0.0.0', port=5000, debug=False)
