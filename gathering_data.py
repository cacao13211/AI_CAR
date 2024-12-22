import os
import mycamera
import cv2
import ctypes
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

speedSet = 0.5

def main():
    camera = mycamera.MyPiCamera(640, 480)
    filepath = os.path.expanduser("~/AI_CAR/video")
    i = 0
    carState = "stop"
    while camera.isOpened():
        keyValue = cv2.waitKey(10)
        #print(str(keyValue))
        
        if keyValue == ord('q'):
            break
       
        elif keyValue == 82:  # Up arrow key
            print("go")
            carState = "go"
            motor_go(speedSet)
        elif keyValue == 84:  # Down arrow key
            print("stop")
            carState = "stop"
            motor_stop()
        elif keyValue == 81:  # Left arrow key
            print("left")
            carState = "left"
            motor_left(speedSet)
        elif keyValue == 83:  # Right arrow key
            print("right")
            carState = "right"
            motor_right(speedSet)
                
        _, image = camera.read()
        image = cv2.flip(image, -1)
        cv2.imshow('Original', image)
        
        height, _, _ = image.shape
        save_image = image[int(height/2):,:,:]
        save_image = cv2.cvtColor(save_image, cv2.COLOR_BGR2YUV)
        save_image = cv2.resize(save_image, (200, 66))
        save_image = cv2.GaussianBlur(save_image, (5,5), 0)
        _, save_image = cv2.threshold(save_image, 205, 255, cv2.THRESH_BINARY_INV)
        
        cv2.imshow('Processed', save_image)
        
       if carState == "left":
            filename = f"{os.path.join(filepath, 'train')}_{i:05d}_045.png"
            cv2.imwrite(filename, save_image)
            i += 1
        elif carState == "right":
            filename = f"{os.path.join(filepath, 'train')}_{i:05d}_135.png"
            cv2.imwrite(filename, save_image)
            i += 1
        elif carState == "go":
            filename = f"{os.path.join(filepath, 'train')}_{i:05d}_090.png"
            cv2.imwrite(filename, save_image)
            i += 1
        
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
