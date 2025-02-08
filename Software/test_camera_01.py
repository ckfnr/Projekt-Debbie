import cv2
import time
from flask import Flask, Response

app = Flask(__name__)

# Set up the camera (0 for the default camera, or change it to the desired camera index)
camera = cv2.VideoCapture(0)
fps = 60  # Desired FPS
delay = 1 / fps  # Time delay between frames

# Set the camera FPS
camera.set(cv2.CAP_PROP_FPS, fps)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Rotate the frame 180 degrees
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # Yield the frame in a format that Flask can use for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        time.sleep(delay)  # Maintain the desired FPS

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