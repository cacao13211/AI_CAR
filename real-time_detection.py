import os
import threading
import time
import mycamera
import cv2


# Pretrained class in the model
classNames = {
    1: 'person',
    2: 'bicycle',
    3: 'car',
    4: 'motorcycle',
    5: 'airplane',
    6: 'bus',
    7: 'train',
    8: 'truck',
    9: 'boat',
    10: 'traffic light',
    11: 'fire hydrant',
    12: 'stop sign',
    13: 'parking meter',
    14: 'bench',
    15: 'bird',
    16: 'cat',
    17: 'dog',
    18: 'horse',
    19: 'sheep',
    20: 'cow',
    21: 'elephant',
    22: 'bear',
    23: 'zebra',
    24: 'giraffe',
    25: 'backpack',
    26: 'umbrella',
    27: 'handbag',
    28: 'tie',
    29: 'suitcase',
    30: 'frisbee',
    31: 'skis',
    32: 'snowboard',
    33: 'sports ball',
    34: 'kite',
    35: 'baseball bat',
    36: 'baseball glove',
    37: 'skateboard',
    38: 'surfboard',
    39: 'tennis racket',
    40: 'bottle',
    41: 'wine glass',
    42: 'cup',
    43: 'fork',
    44: 'knife',
    45: 'spoon',
    46: 'bowl',
    47: 'banana',
    48: 'apple',
    49: 'sandwich',
    50: 'orange',
    51: 'broccoli',
    52: 'carrot',
    53: 'hot dog',
    54: 'pizza',
    55: 'donut',
    56: 'cake',
    57: 'chair',
    58: 'couch',
    59: 'potted plant',
    60: 'bed',
    61: 'dining table',
    62: 'toilet',
    63: 'tv',
    64: 'laptop',
    65: 'mouse',
    66: 'remote',
    67: 'keyboard',
    68: 'cell phone',
    69: 'microwave',
    70: 'oven',
    71: 'toaster',
    72: 'sink',
    73: 'refrigerator',
    74: 'book',
    75: 'clock',
    76: 'vase',
    77: 'scissors',
    78: 'teddy bear',
    79: 'hair drier',
    80: 'toothbrush'
}


def id_class_name(class_id, classes):
    for key, value in classes.items():
        if class_id == key:
            return value

camera = mycamera.MyPiCamera(640, 480)

_, image = camera.read()
image = cv2.flip(image, -1)
image_dnn = image
image_ok = 0
image_find_ok = 0

def opencvDnn_thread():
    global image, image_dnn
    global image_ok, image_find_ok
    
    model_path = os.path.expanduser("~/AI_CAR/OpencvDnn/models")
    model = cv2.dnn.readNetFromTensorflow(
        os.path.join(model_path, "frozen_inference_graph.pb"),
        os.path.join(model_path, "ssd_mobilenet_v2_coco_2018_03_29.pbtxt")
    )

    while True:
        if image_ok == 1:
            image_dnn = image
            
            image_height, image_width, _ = image_dnn.shape
            
            model.setInput(cv2.dnn.blobFromImage(image_dnn, size=(300, 300), swapRB = True))
            output = model.forward()
            
            for detection in output[0, 0, :, :]:
                confidence = detection[2]
                if confidence > .5:
                    class_id = detection[1]
                    class_name = id_class_name(class_id, classNames)
                    print(f"class ID : {class_id}  confidence: {detection[2]}  class name: {class_name}")
                    box_x = detection[3] * image_width
                    box_y = detection[4] * image_height
                    box_width = detection[5] * image_width
                    box_height = detection[6] * image_height
                    cv2.rectangle(image_dnn, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (23, 230, 210), thickness=1)
                    cv2.putText(image_dnn, class_name, (int(box_x), int(box_y + .05 * image_height)), cv2.FONT_HERSHEY_SIMPLEX, (.005 * image_width), (0, 0, 255))
                    image_find_ok = 1
    

def main():
    global image, image_dnn
    global image_ok, image_find_ok
    
    try :
        while True:
            
            keyValue = cv2.waitKey(1)
            
            if keyValue == ord('q') :
                break
            
            image_ok = 0
            _, image = camera.read()
            image = cv2.flip(image, -1)
            image_ok = 1
            cv2.imshow('image', image)
            if image_find_ok == 1:
                cv2.imshow('image dnn ', image_dnn)
                image_find_ok = 0
                
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    task1 = threading.Thread(target = opencvDnn_thread)
    task1.start()
    main()
    cv2.destroyAllWindows()

