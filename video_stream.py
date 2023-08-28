from flask import Flask, Response
import cv2

app = Flask(__name__)

# Open the video camera. No arguments means the default camera (0).
vc = cv2.VideoCapture(0)


def gen():
    while True:
        # Read a video frame.
        rval, frame = vc.read()

        # Encode the frame as JPEG.
        _, jpeg = cv2.imencode('.jpg', frame)

        # Yield the frame data as a byte string.
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')


@app.route('/')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
