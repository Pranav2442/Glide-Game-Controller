import cv2 as cv,mediapipe as mp,pyautogui as p

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands
cap = cv.VideoCapture(0)
points = [4, 8, 12, 16, 20]
loc_x = None
loc_y = None

lead_pos = [0,1,0]
center_pos = 1
start = None
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    with mp_holistic.Holistic(min_detection_confidence=0.5,min_tracking_confidence=0.5) as holistic:
        while True:
            ret, frame = cap.read()
            frame = cv.flip(frame, 1)
            frame = cv.resize(frame, (440,330))
            h, w, c = frame.shape
            img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results_hol_process = holistic.process(img)
            results_hol_processands = hands.process(img)
            img = cv.cvtColor(img,cv.COLOR_RGB2BGR)
            w_m = int(w/2)
            h_m = int(h/2)
            
            if results_hol_process.pose_landmarks:
                right_x_cor = int(results_hol_process.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x * w)-7
                right_y_cor = int(results_hol_process.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y * h)
                
                left_x_cor = int(results_hol_process.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x * w)+7
                left_y_cor = int(results_hol_process.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y * h)
                
                mid_x_cor = left_x_cor + int(abs(right_x_cor - left_x_cor) / 2)
                mid_y_cor = int(abs(right_y_cor + left_y_cor) / 2)
                if start != None:
                    if right_x_cor < w_m and center_pos > 0 and lead_pos[center_pos-1] == 0:
                            lead_pos[center_pos] = 0
                            lead_pos[center_pos-1] = 1
                            if lead_pos==[0,1,0]:
                                p.keyDown('up')
                                p.keyUp('left')

                            p.keyUp('right')
                            p.keyDown('left')
                            p.keyDown('up')
                            center_pos -= 1
                            print("Left key")
                            print(center_pos)
                    if left_x_cor > w_m and center_pos < 2 and lead_pos[center_pos+1] == 0:
                            print("Right key")
                            lead_pos[center_pos] = 0
                            lead_pos[center_pos+1] = 1
                            if lead_pos==[0,1,0]:
                                p.keyDown('up')
                                p.keyUp('left')

                            p.keyUp('left')
                            p.keyDown('right')
                            p.keyDown('up')
                            center_pos += 1
                            print(lead_pos)
                    if right_x_cor > w_m and left_x_cor < w_m and center_pos == 0:
                            lead_pos[center_pos] = 0
                            lead_pos[center_pos +1] = 1
                            center_pos += 1
                            if lead_pos==[0,1,0]:
                                p.keyDown('up')

                            p.keyUp('right')
                            print(lead_pos)
                            print('back to orignal position')
                            if lead_pos==[0,1,0]:
                                p.keyDown('up')
                                p.keyUp('left')

                    if right_x_cor > w_m and left_x_cor < w_m and center_pos == 2:
                            lead_pos[center_pos] = 0
                            lead_pos[center_pos -1] = 1
                            center_pos -= 1
                            if lead_pos==[0,1,0]:
                                p.keyDown('up')

                            p.keyUp('left')
                            print('back tp orignal position')
                            print(lead_pos)
                            if lead_pos==[0,1,0]:
                                p.keyDown('up')
                                p.keyUp('right')

            Rhandcorl = []
            Lhandcorl = []
            Rfingers = []
            Lfingers = []
            hand1 = None
            hand2 = None
            try:
                hand1 = results_hol_processands.multi_handedness[0].classification[0].label
                hand2 = results_hol_processands.multi_handedness[1].classification[0].label
                for handnum, hand_landmarks in enumerate(results_hol_processands.multi_hand_landmarks):
                    if handnum == 0:
                        if hand1 == 'Left':
                            for id, lm in enumerate(hand_landmarks.landmark):
                                cx, cy = int(lm.x * w), int(lm.y * h)
                                Lhandcorl.append([id,cx,cy])
                        elif hand1 == 'Right':
                            for id, lm in enumerate(hand_landmarks.landmark):
                                cx, cy = int(lm.x * w), int(lm.y * h)
                                Rhandcorl.append([id,cx,cy])
                    if handnum == 1:
                        if hand2 == 'Left':
                            for id, lm in enumerate(hand_landmarks.landmark):
                                cx, cy = int(lm.x * w), int(lm.y * h)
                                Lhandcorl.append([id,cx,cy])
                        elif hand2 == 'Right':
                            for id, lm in enumerate(hand_landmarks.landmark):
                                cx, cy = int(lm.x * w), int(lm.y * h)
                                Rhandcorl.append([id,cx,cy])
                if Rhandcorl != []:
                    if Rhandcorl[points[0]][1] < Rhandcorl[points[0] - 1][1]:
                        Rfingers.append(1)
                    else:
                        Rfingers.append(0)

                    for id in range(1, 5):
                        if Rhandcorl[points[id]][2] < Rhandcorl[points[id] - 2][2]:
                            Rfingers.append(1)
                        else:
                            Rfingers.append(0)
                    totalFingers_right = Rfingers.count(1)

                if Lhandcorl != []:
                    if Lhandcorl[points[0]][1] > Lhandcorl[points[0] - 1][1]:
                        Lfingers.append(1)
                    else:
                        Lfingers.append(0)

                    for id in range(1, 5):
                        if Lhandcorl[points[id]][2] < Lhandcorl[points[id] - 2][2]:
                            Lfingers.append(1)
                        else:
                            Lfingers.append(0)
                    totalFingers_left = Lfingers.count(1)
            except:
                pass
            if Rfingers==[1,1,1,1,1] and Lfingers==[1,1,1,1,1]:
                loc_x = left_x_cor + int(abs(right_x_cor - left_x_cor) / 2)
                loc_y = int(abs(right_y_cor + left_y_cor) / 2)
                start = 35
                p.press('space')

            if loc_y is not None:
                if (mid_y_cor- loc_y) <= -24:
                    p.keyDown('up')
                    print('up')
                elif (mid_y_cor - loc_y) >= 40:
                    p.keyDown('down')
                    print('down')
            if Rfingers==[0,1,1,0,0]:
                p.click(button='left')
            if Rfingers==[0,1,1,1,0]:
                    p.click(button='right', clicks=10 )
            cv.imshow('Gesture Recognition based game controler',img)
            if cv.waitKey(1)==27:
                break
            