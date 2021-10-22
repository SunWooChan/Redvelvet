# -*- coding: utf-8 -*-
import cv2
import numpy as np

video_path = 'redvelvet.mp4'
cap = cv2.VideoCapture(video_path) #  비디오 읽기

# output_size = (375, 667) # 저장할 영상을 핸드폰 사이즈로 
# 영상이 작으면 에러가 날 수 있다.
output_size = (187,333)

# 영상 저장
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
out = cv2.VideoWriter('%s_output.mp4' %(video_path.split('.')[0]), fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)
# cv2.VideoWriter : 비디오 출력 모듈 초기화

if not cap.isOpened():
    exit()

#1
tracker = cv2.TrackerCSRT_create() 

ret, img = cap.read()
cv2.namedWindow('Select Window') 
cv2.imshow('Select Window', img)

# 2. setting ROI
rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
# ROI 설정하고 윈도우 닫자
cv2.destroyWindow('Select Window')
# 마우스드래그로 ROI 지정 하고 스페이스바 누르면 ROI가 지정돼서 ROI 정보가 rect에 저장된다.

# 3. initialize tracker
tracker.init(img, rect) # rect로 설정한 부븐을 트래킹하면 된다고 인식하게 된다.

while True:
    ret, img = cap.read() # video 읽어서 img에 저장

    if not ret: # 잘못 읽었다, 또는 비디오가 끝났다면 ret이 false가 된다.
        exit() # 프로그램 종료

    success, box = tracker.update(img) # img에서 rect로 설정한 이미지와 비슷한 물체의 위치를 찾아 반환한다.
    # success : 성공 했는지 안했는지 boolean으로, box : ROI설정 한 것처럼 rec 형태의 데이터로

    left, top, w, h = [int(v) for v in box] # 한번 돌때마다 v의 값을 int로 변환한 다음에 왼쪽,오른쪽 다 넣자
    
    center_x = left + w/2
    center_y = top + h/2

    result_top = int(center_y - output_size[1] / 2)
    result_bottom = int(center_y + output_size[1] / 2)
    result_left = int(center_x - output_size[0] / 2)
    result_right = int(center_x + output_size[0] / 2)

    result_img = img[result_top:result_bottom, result_left:result_right].copy()

    out.write(result_img)

    # 사각형 그리기
    cv2.rectangle(img, pt1=(left, top), pt2=(left + w, top + h), color=(255, 255, 255), thickness=3)

    cv2.imshow('result_img', result_img)
    cv2.imshow('img', img) # 이미지 보여주기
    if cv2.waitKey(1)==ord('q'): # 1 ms 동안 기다린다. 꼭 써주어야 한다.
        break
