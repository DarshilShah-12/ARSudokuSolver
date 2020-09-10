import numpy as np
import cv2
from read_digits import getPrediction
import sudoku

cap = cv2.VideoCapture(0)
cap.set(3,1080)
cap.set(4,1920)

loops = 0
while(True):
    ret, frame = cap.read()
    orig = np.copy(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 2
    )

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        ext = 0
        cv2.rectangle(frame, (x - ext, y - ext), (x + w + ext, y + h + ext), (255, 0, 0), 5)

        crop = 6
        res = 700
        M = cv2.getPerspectiveTransform(np.float32([[x + crop, y + crop], [x + crop, y + h - crop], [x + w - crop, y + crop], [x + w - crop, y + h - crop]]), np.float32([[0,0], [0, res], [res, 0], [res,res]]))
        dst = cv2.warpPerspective(thresh, M, (res, res))
        dst2 = cv2.warpPerspective(frame, M, (res, res))

        kern_size = int(res*0.03)
        kernel = np.ones((int(res*0.03),int(res*0.03)), np.uint8)
        erosion = cv2.erode(dst, kernel, iterations=3)
        dilation = cv2.dilate(dst,(kern_size,kern_size),iterations = 2)

        constant = res//9
        offset = 8
        y_offset = 2
        if (loops < 100):
            for i in range(9):
                x_offset = 1
                for j in range(9):
                    sub_image = dilation[constant*i + offset + y_offset: constant*(i + 1) - offset + y_offset, constant*j + offset + x_offset: constant*(j + 1) - offset + x_offset]
                    cv2.imwrite('save/' + str(i) + str(j) + '.jpg', sub_image)
                    cv2.rectangle(dilation, (constant*j + offset + x_offset, constant*i + offset + y_offset), (constant*(j + 1) - offset + x_offset, constant*(i + 1) - offset + y_offset), (66, 66, 66), 2)
                    if (x_offset < 6):
                        x_offset += 1
                y_offset += 1

        if (loops == 100):
            given = getPrediction()
            copy = ""
            for row in given:
                for col in row:
                    copy += str(col)
            print(copy)
            predicted = sudoku.call_from_main(copy)
            print(predicted)
        font = cv2.FONT_HERSHEY_SIMPLEX
        if (loops >= 100):
            y_offset = 48
            for i in range(9):
                x_offset = 3
                for j in range(9):
                    if (given[i][j] == 0):
                        cv2.putText(dst2, str(predicted[i][j]), (constant * j + offset + x_offset, constant * i + offset + y_offset), font, 2, (0,20,200), 2, cv2.LINE_AA)
                        if (j < 6):
                            x_offset += 3
                y_offset += 1
    loops += 1
    dst2 = cv2.resize(dst2, (w, h))
    # print(type(dst2))
    orig[y: y + h, x: x + w] = dst2
    cv2.imshow('frame', orig)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()