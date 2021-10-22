# -*- coding: utf-8 -*-
import cv2
import numpy as np

video_path = 'redvelvet.mp4'
cap = cv2.VideoCapture(video_path) #  ���� �б�

# output_size = (375, 667) # ������ ������ �ڵ��� ������� 
# ������ ������ ������ �� �� �ִ�.
output_size = (187,333)

# ���� ����
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
out = cv2.VideoWriter('%s_output.mp4' %(video_path.split('.')[0]), fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)
# cv2.VideoWriter : ���� ��� ��� �ʱ�ȭ

if not cap.isOpened():
    exit()

#1
tracker = cv2.TrackerCSRT_create() 

ret, img = cap.read()
cv2.namedWindow('Select Window') 
cv2.imshow('Select Window', img)

# 2. setting ROI
rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
# ROI �����ϰ� ������ ����
cv2.destroyWindow('Select Window')
# ���콺�巡�׷� ROI ���� �ϰ� �����̽��� ������ ROI�� �����ż� ROI ������ rect�� ����ȴ�.

# 3. initialize tracker
tracker.init(img, rect) # rect�� ������ �κ��� Ʈ��ŷ�ϸ� �ȴٰ� �ν��ϰ� �ȴ�.

while True:
    ret, img = cap.read() # video �о img�� ����

    if not ret: # �߸� �о���, �Ǵ� ������ �����ٸ� ret�� false�� �ȴ�.
        exit() # ���α׷� ����

    success, box = tracker.update(img) # img���� rect�� ������ �̹����� ����� ��ü�� ��ġ�� ã�� ��ȯ�Ѵ�.
    # success : ���� �ߴ��� ���ߴ��� boolean����, box : ROI���� �� ��ó�� rec ������ �����ͷ�

    left, top, w, h = [int(v) for v in box] # �ѹ� �������� v�� ���� int�� ��ȯ�� ������ ����,������ �� ����
    
    center_x = left + w/2
    center_y = top + h/2

    result_top = int(center_y - output_size[1] / 2)
    result_bottom = int(center_y + output_size[1] / 2)
    result_left = int(center_x - output_size[0] / 2)
    result_right = int(center_x + output_size[0] / 2)

    result_img = img[result_top:result_bottom, result_left:result_right].copy()

    out.write(result_img)

    # �簢�� �׸���
    cv2.rectangle(img, pt1=(left, top), pt2=(left + w, top + h), color=(255, 255, 255), thickness=3)

    cv2.imshow('result_img', result_img)
    cv2.imshow('img', img) # �̹��� �����ֱ�
    if cv2.waitKey(1)==ord('q'): # 1 ms ���� ��ٸ���. �� ���־�� �Ѵ�.
        break
