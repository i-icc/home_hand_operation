import cv2
from hand import HandDetector
import argparse
from command import Cmd

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--draw', action="store_true",
                    help="draw hand")
parser.add_argument('-cam', '--camera', type=int,
                    help="Use camera number")
args = parser.parse_args()

def main():
    cmd = Cmd()
    cap = cv2.VideoCapture(int(args.camera))

    handDetector = HandDetector()
    pre_pose = -1

    while True:
        ret, frame = cap.read()

        handDetector.findHands(frame, args.draw)
        pose = handDetector.find_pose(frame)
        if pose == pre_pose:
            cmd.put_pose(pose)
        pre_pose = pose
        print(cmd.get_cmd())
        if pose == -1:
            print("None")
        elif pose == 11:
            print("Fox")
        else:
            print(pose)

        # cv2.imshow('camera' , frame)

        key =cv2.waitKey(10)
        if key == 113:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
