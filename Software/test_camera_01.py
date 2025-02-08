import time
import io
from flask import Flask, Response
from picamera import PiCamera

app = Flask(__name__)

# Set up the PiCamera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60  # Desired FPS

def generate_frames():
    stream = io.BytesIO()
    for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
        stream.seek(0)
        frame = stream.read()
        stream.truncate(0)
        
        # Yield the frame in a format that Flask can use for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Live Video Stream</title>
    </head>
    <body>
        <h1>Live Video Stream</h1>
        <img src="/video_feed" width="640" height="480">
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)