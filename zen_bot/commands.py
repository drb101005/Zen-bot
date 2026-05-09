import cv2
import threading

camera_active = False
camera_thread = None

def open_camera():
    global camera_active, camera_thread
    if not camera_active:
        camera_active = True
        camera_thread = threading.Thread(target=_run_camera, daemon=True)
        camera_thread.start()
        return "Camera opened."

def close_camera():
    global camera_active
    camera_active = False
    if camera_thread:
        camera_thread.join()
    return "Camera closed."

def _run_camera():
    cap = cv2.VideoCapture(0)
    while camera_active:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Zen Bot Camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

def sleep():
    # This will be handled in main.py
    return "Going to sleep."