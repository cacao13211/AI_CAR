#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <wiringPi.h>
#include <softPwm.h>
#include <stdlib.h>

// GPIO 핀 정의 (BCM GPIO 번호 기준)
#define AIN1 22
#define AIN2 27
#define PWMA 18

#define BIN1 25
#define BIN2 24
#define PWMB 23

#define BUZZER 12

// 모터 상태를 나타내는 enum
typedef enum {
    MOTOR_STOP = 0,
    MOTOR_GO,
    MOTOR_BACK,
    MOTOR_LEFT,
    MOTOR_RIGHT
} MotorState;

// 전역 상태
static MotorState current_state = MOTOR_STOP;
static double current_speed = 0.0;
static pthread_mutex_t state_lock = PTHREAD_MUTEX_INITIALIZER;

// 모터 상태를 설정하는 함수
void set_motor_state(MotorState state, double speed) {
    // 속도를 0~1 범위로 가정하고, PWM은 0~100으로 변환
    int pwm_val = (int)(speed * 100);
    if (pwm_val < 0) pwm_val = 0;
    if (pwm_val > 100) pwm_val = 100;

    switch(state) {
        case MOTOR_STOP:
            digitalWrite(AIN1, LOW);
            digitalWrite(AIN2, LOW);
            softPwmWrite(PWMA, 0);
            digitalWrite(BIN1, LOW);
            digitalWrite(BIN2, LOW);
            softPwmWrite(PWMB, 0);
            break;
        case MOTOR_GO:
            digitalWrite(AIN1, LOW);
            digitalWrite(AIN2, HIGH);
            softPwmWrite(PWMA, pwm_val);
            digitalWrite(BIN1, LOW);
            digitalWrite(BIN2, HIGH);
            softPwmWrite(PWMB, pwm_val);
            break;
        case MOTOR_BACK:
            digitalWrite(AIN1, HIGH);
            digitalWrite(AIN2, LOW);
            softPwmWrite(PWMA, pwm_val);
            digitalWrite(BIN1, HIGH);
            digitalWrite(BIN2, LOW);
            softPwmWrite(PWMB, pwm_val);
            break;
        case MOTOR_LEFT:
            digitalWrite(AIN1, HIGH);
            digitalWrite(AIN2, LOW);
            softPwmWrite(PWMA, 0);
            digitalWrite(BIN1, LOW);
            digitalWrite(BIN2, HIGH);
            softPwmWrite(PWMB, pwm_val);
            break;
        case MOTOR_RIGHT:
            digitalWrite(AIN1, LOW);
            digitalWrite(AIN2, HIGH);
            softPwmWrite(PWMA, pwm_val);
            digitalWrite(BIN1, HIGH);
            digitalWrite(BIN2, LOW);
            softPwmWrite(PWMB, 0);
            break;
        default:
            // Unknown state
            break;
    }
}

// 모터 상태를 관리하는 쓰레드 함수
void* motor_control_thread(void* arg) {
    while(1) {
        pthread_mutex_lock(&state_lock);
        MotorState state = current_state;
        double speed = current_speed;
        pthread_mutex_unlock(&state_lock);

        set_motor_state(state, speed);

        usleep(100000); // 100ms delay
    }
    return NULL;
}

// 초기화 함수
void init_motor_control() {
    if (wiringPiSetupGpio() < 0) {
        printf("Unable to setup wiringPi\n");
        exit(1);
    }

    pinMode(AIN1, OUTPUT);
    pinMode(AIN2, OUTPUT);
    pinMode(BIN1, OUTPUT);
    pinMode(BIN2, OUTPUT);
    pinMode(PWMA, PWM_OUTPUT);
    pinMode(PWMB, PWM_OUTPUT);
    pinMode(BUZZER, OUTPUT);

    softPwmCreate(PWMA, 0, 100);
    softPwmCreate(PWMB, 0, 100);

    // 초기 상태 설정 (정지)
    set_motor_state(MOTOR_STOP, 0.0);

    // 모터 제어 쓰레드 시작
    pthread_t tid;
    pthread_create(&tid, NULL, motor_control_thread, NULL);
    pthread_detach(tid);
}

// 외부에서 호출할 수 있는 함수들
void motor_go_c(double speed) {
    pthread_mutex_lock(&state_lock);
    current_state = MOTOR_GO;
    current_speed = speed;
    pthread_mutex_unlock(&state_lock);
}

void motor_back_c(double speed) {
    pthread_mutex_lock(&state_lock);
    current_state = MOTOR_BACK;
    current_speed = speed;
    pthread_mutex_unlock(&state_lock);
}

void motor_left_c(double speed) {
    pthread_mutex_lock(&state_lock);
    current_state = MOTOR_LEFT;
    current_speed = speed;
    pthread_mutex_unlock(&state_lock);
}

void motor_right_c(double speed) {
    pthread_mutex_lock(&state_lock);
    current_state = MOTOR_RIGHT;
    current_speed = speed;
    pthread_mutex_unlock(&state_lock);
}

void motor_stop_c() {
    pthread_mutex_lock(&state_lock);
    current_state = MOTOR_STOP;
    current_speed = 0.0;
    pthread_mutex_unlock(&state_lock);
}

// C 함수들을 외부에 노출
__attribute__((visibility("default"))) void init_motor() {
    init_motor_control();
}

__attribute__((visibility("default"))) void motor_go_py(double speed) {
    motor_go_c(speed);
}

__attribute__((visibility("default"))) void motor_back_py(double speed) {
    motor_back_c(speed);
}

__attribute__((visibility("default"))) void motor_left_py(double speed) {
    motor_left_c(speed);
}

__attribute__((visibility("default"))) void motor_right_py(double speed) {
    motor_right_c(speed);
}

__attribute__((visibility("default"))) void motor_stop_py() {
    motor_stop_c();
}
