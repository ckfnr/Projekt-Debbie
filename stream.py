from flask import Flask, Response, render_template_string  # type: ignore[import-untyped]
from picamera2 import Picamera2  # type: ignore
import cv2
from cv2 import COLOR_RGB2GRAY
from typing import Generator

app = Flask(__name__)
picam2: Picamera2 = Picamera2()

def configure_camera() -> None:
    """Stops and reconfigures the camera for video streaming."""
    picam2.stop()
    picam2.configure(
        picam2.create_video_configuration(
            main={"size": (640, 480), "format": "RGB888"},
            controls={"FrameRate": 30}
        )
    )
    picam2.start()

def generate_frames() -> Generator[bytes, None, None]:
    """Yields JPEG-encoded frames for streaming."""
    while True:
        frame = picam2.capture_array()
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        frame = cv2.cvtColor(frame, COLOR_RGB2GRAY)
        _, buffer = cv2.imencode('.jpg', frame)
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            buffer.tobytes() +
            b'\r\n'
        )

@app.route('/video_feed')
def video_feed() -> Response:
    """Video stream route."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index() -> str:
    """Root page with embedded stream."""
    return render_template_string('''
    <html>
    <head>
        <style>
            body { margin: 0; overflow: hidden; background-color: black; }
            img  { width: 100vw; height: 100vh; object-fit: cover; display: block; }
        </style>
    </head>
    <body>
        <img src='/video_feed' />
    </body>
    </html>
    ''')

if __name__ == '__main__':
    configure_camera()
    app.run(host='0.0.0.0', port=5000, debug=False)
