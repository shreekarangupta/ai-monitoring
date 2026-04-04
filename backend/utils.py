import cv2

def is_frame_changed(prev_frame, curr_frame, threshold=5000):
    # ✅ Convert to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

    # ✅ Blur to remove noise (VERY IMPORTANT)
    prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)
    curr_gray = cv2.GaussianBlur(curr_gray, (21, 21), 0)

    # ✅ Frame difference
    diff = cv2.absdiff(prev_gray, curr_gray)

    # ✅ Threshold (binary image)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    # ✅ Remove small noise (morphological operation)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # ✅ Count changed pixels
    change = cv2.countNonZero(thresh)

    return change > threshold