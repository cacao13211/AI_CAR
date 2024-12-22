import os
import mycamera
import cv2
import ctypes
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from ctypes import c_double

# C 공유 라이브러리 로드
motor_lib = ctypes.CDLL('./libmotor.so')

# 모터 초기화
motor_lib.init_motor()

# 모터 제어 함수 정의
def motor_go(speed):
    motor_lib.motor_go_py(c_double(speed))

def motor_back(speed):
    motor_lib.motor_back_py(c_double(speed))

def motor_left(speed):
    motor_lib.motor_left_py(c_double(speed))

def motor_right(speed):
    motor_lib.motor_right_py(c_double(speed))

def motor_stop():
    motor_lib.motor_stop_py()

speedSet = 0.4

def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height/2):,:,:]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.resize(image, (200, 66))
    image = cv2.GaussianBlur(image, (5,5), 0)
    _, image = cv2.threshold(image, 205, 255, cv2.THRESH_BINARY_INV)
    image = image / 255
    return image

def main():
    camera = mycamera.MyPiCamera(640, 480)
    model_path = os.path.expanduser("~/AI_CAR/model/lane_navigation_model.keras")
    model = load_model(model_path)
    
    carState = "stop"
    while camera.isOpened():
        keyValue = cv2.waitKey(10)
        #print(str(keyValue))
        
        if keyValue == ord('q'):
            break
        elif keyValue == 82: # Up arrow key
            print("go")
            carState = "go"
        elif keyValue == 84: # Down arrow key
            print("stop")
            carState = "stop"
                
        _, image = camera.read()
        image = cv2.flip(image, -1)
        cv2.imshow('Original', image)
        
        preprocessed = img_preprocess(image)
        cv2.imshow('preprocessed', preprocessed)
        
        X = np.asarray([preprocessed])
        steering_angle = int(model.predict(X)[0])
        print("predict angle:", steering_angle)
        
        if carState == "go":
            if steering_angle >= 85 and steering_angle <= 105:
                print("go")
                speedSet = 0.4
                motor_go(speedSet)
            elif steering_angle > 110:
                speedSet = 0.4
                print("right")
                motor_right(speedSet)
            elif steering_angle < 85:
                speedSet = 0.4
                print("left")
                motor_left(speedSet)
        elif carState == "stop":
            motor_stop()
        
        
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

