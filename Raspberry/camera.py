from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.rotation=180

camera.start_preview()
sleep(1)
camera.capture('test.jpg')
camera.stop_preview()

