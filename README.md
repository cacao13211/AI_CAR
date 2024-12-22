# AI_CAR
9조 임베디드 프로젝트  
라즈베리파이를 활용한 자율주행 모형 자동차 구현 프로젝트
  
## 팀 소개

|   이름               |     학번     | 역할                |
|----------------------| --------------|---------------------|
| **이기원**          | 20170776      | 딥러닝 자율주행 모델 구축 및 학습, 학습 데이터 생성 |
| **강민재**          | 20221315      | 모형 자동차 제작, 원격 제어 기능 구현, 자료 조사, 부품 보급 |
| **이재찬**          | 20200894      | 딥러닝 자율주행 모델 적용 및 테스트,  원격 제어 기능 구현|
| **한성룡**          | 20221387      | 원격제어 기능 구헌, 발표자료 제작, 재료 및 부품 보급 |

    
## DEMO
### 자율주행 기능
- 좌회전
  
![Project Demo](assets/self-driving_left.gif)
  
- 우회전
  
![Project Demo](assets/self-driving_right.gif)
  
### 비상정지 기능 
- 카메라가 사람을 탐지하면 멈추는 기능을 구현함.
![Project Demo](assets/stop.gif)

### 수동조작 기능
![Project Demo](assets/manual_control.gif)
  
### 객체 탐지
- OpenCV DNN + MobileNet v2를 활용해서 객체탐지 기능을 구현함.
![Project Demo](assets/object_detection1.png)
![Project Demo](assets/object_detection2.png)
    
## 파일구조
파일 구조에 대한 설명

## 실행 파일

  
## 시스템 구조
![전체 시스템 구조](assets/project.png)
- `automated_driving_dnn.py`
  - 자율 주행 및 장애물 탑재 기능을 담당하는 소스 코드 파일
  - 차량 제어를 위해 `motor_contorl.c`에 등록된 함수를 호출하여 전역 변수 `carState`의 값을 변경함

- `motor_control.c`
  - DC 모터를 제어하는 함수
  - 멀티쓰레드를 실행하는 방식으로 함수를 호출함.
  - 전역 변수 `carState` 값에 따라 이동 여부 또는 이동 방향을 결정함.

- `automated_driving_dnn.py`에서 `motor_control.c` 호출하기
  - 파이썬의 표준 라이브러리 `ctypes`를 활용
  - `motor_contorl.c`를 컴파일하려 동적 라이브러리인 `libmotor.so`를 생성
  - 파이썬 파일에서 libmotor.so 객체를 생성하여 c 라이브러리를 로드함.
  ###### 컴파일 명령:
  ```bash
  gcc -shared -o libmotor.so -fPIC -motor_control.c -lwiringPi -lpthread
  ```


### 임베디드 파트
- DC 모터
  - 차량의 기본적인 움직임을 제어하는 용도로 사용.
  - 전진, 좌회전, 우회전 이동 가능.
- 카메라 모듈
  -  도로를 식별하고 장애물을 탐지하는 역할 담당. 주변 환경 인식
  
### 인공지능 파트
수동 조작 기능을 통해 학습 데이터를 생성하고 자율 주행 모델을 학습함.
- OpenCV
  - 학습 데이터를 생성하고 인공지능 모델의 성능 개선을 위해 이미지 전처리 작업 진행
  - 카메라로 획득한 이미지를 YUV 형식으로 변환
  - 이미지에 필터를 적용하여 도로의 경계선을 강조한 후 학습 데이터를 생성
  
#### 이미지 전처리 예
|    전처리 전         |     전처리 후        |
|----------------------|-----------------------|
| ![전처리 전 이미지]  | ![전처리 후 이미지]   |
  
- 자율주행 모델
  - [end to end learning for self-driving cars](https://developer.nvidia.com/blog/deep-learning-self-driving-cars/)에 소개된 CNN 모델 구조를 활용
  - 텐서플로우로 CNN 모델을 구현 후 학습 데이터로 모델을 학습시킴
  - 학습된 CNN 구조의 추론 기능을 활용해서 전진, 좌회전, 우회전인지 판단하는 기능을 구현
- 객체 탐지 모델
  - 효율적인 개발을 위해 사전에 훈련된 모델인 MobileNetV2를 사용함.
  - 경량화된 모델로 하드웨어 성능이 제한된 임베디드 환경에 적합함.
  - MobileNet의 추론 기능을 사용하기 위해 OpenCV DNN를 활용함

#### 이미지 전처리 작업

  
## 문제점 및 해결 방안



