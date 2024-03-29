# ROI-ball-tracking
Single object tracking with ROI selection and OpenCV built-in trackers
### Built With
I plan to use TensorFlow to optimize the model a bit better.
* [Python](https://www.python.org/)
* [NumPy](https://numpy.org/)
* [OpenCV](https://opencv.org/)
* [Imutils](https://pypi.org/project/imutils/)


Typical command to run the program:
```
python roi_selection.py -- video trial.mp4 --output test0.avi csrt
```
Select the ball by pressing the key "s" in the trial video.

Cancel the selection process by pressing c button

Available built-in trackers in OpenCV:
```
 "csrt": cv2.legacy.TrackerCSRT_create,
 "kcf": cv2.legacy.TrackerKCF_create,
 "boosting": cv2.legacy.TrackerBoosting_create,
 "mil": cv2.legacy.TrackerMIL_create,
 "tld": cv2.legacy.TrackerTLD_create,
 "medianflow": cv2.legacy.TrackerMedianFlow_create,
 "mosse": cv2.legacy.TrackerMOSSE_create
```
CSRT is recommended for ball-tracking in the sample videos since it provides higher accuracy despite the lower FPS


The results with object tracking is recorded in test0.avi file in the same repository
