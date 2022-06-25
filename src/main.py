import cv2
from hand import HandDetector

def main():
    cap = cv2.VideoCapture(1)

    handDetector = HandDetector()

    while True:
        ret, frame = cap.read()

        handDetector.findHands(frame)

        cv2.imshow('camera' , frame)

        key =cv2.waitKey(5)
        if key == 113:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()