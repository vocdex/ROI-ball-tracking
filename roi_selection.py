#Implementation of object detection by ROI and tracking by built-in OpenCV trackers

import argparse
import cv2
import numpy as np
from imutils.video import FPS
import imutils
from collections import deque

# Argument input
parser= argparse.ArgumentParser() #creating a parser
parser.add_argument("-v", "--video",required=True, help="path to video")
parser.add_argument("-t", "--tracker", type=str,
                default="csrt", help="OpenCV tracker type")
parser.add_argument("-o", "--output", required=True, help="path to output")
args = vars(parser.parse_args()) #parsing arguments

# Process argument
print("[INFO] Start to process video")
vs = cv2.VideoCapture(args["video"])  # Initialize the video
writer = None
label = " "
fps = None
OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.legacy.TrackerCSRT_create,
    "kcf": cv2.legacy.TrackerKCF_create,
    "boosting": cv2.legacy.TrackerBoosting_create,
    "mil": cv2.legacy.TrackerMIL_create,
    "tld": cv2.legacy.TrackerTLD_create,
    "medianflow": cv2.legacy.TrackerMedianFlow_create,
    "mosse": cv2.legacy.TrackerMOSSE_create
}
tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()  # Initialize the tracker

box = None
position = deque()
print("[INFO] Initialization")
state = 0

video_frame_rate = vs.get(cv2.CAP_PROP_FPS)  # Obtain video frame rate

while True:
    (grabbed, frame) = vs.read()  # Loop frame by frame
    if frame is None:  # End if there is no frame left
        break
    # frame=frame[100:900,800:1900] Reshape frame if necessary

    (H, W) = frame.shape[:2]

    if writer is None:  # Initialize the writer
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(
            args["output"], fourcc, video_frame_rate, (W, H), True)

    if box is not None:  # If the initial position of object is given, the tracking is handled by tracker automatically
        (success, box) = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            # Draw a rectangle around the object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            position.appendleft((int(x + w / 2), int(y + h / 2)))
            for i in range(0, len(position)):
                if i + 1 < len(position):
                    # Draw the trajectory
                    cv2.line(frame, position[i], position[i + 1], (255, 0, 0), 2)

        # Count frame rate of tracker
        fps.update()
        fps.stop()

        # Print info in each frame
        info = [("Tracker", args["tracker"]), ("Success", "Yes" if success else "No"),
                ("FPS:", "{:.2f}".format(fps.fps())), ("Position", position[0])]
        for (i, (k, v)) in enumerate(info):
            text = "{}:{}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Slow down video until the object is chosen
    if state == 1:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
    else:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(100)

    # Press s to select position of object
    if key == ord("s"):
        state = 1
        box = cv2.selectROI(
            "Frame", frame, fromCenter=False, showCrosshair=True)
        tracker.init(frame, box)
        fps = FPS().start()
    elif key == ord("q"):
        break

    writer.write(frame)

if writer:
    writer.release()
vs.release()
cv2.destroyAllWindows()