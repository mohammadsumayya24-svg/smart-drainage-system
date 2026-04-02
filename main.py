import cv2
import time
from waste_detection import detect_waste

# bin settings
bin_level = 0
MAX_LEVEL = 5
WARNING_LEVEL = int(0.8 * MAX_LEVEL)

last_detection_time = 0
DETECTION_DELAY = 2  # seconds

# IMPORTANT: force correct camera backend
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Trying another camera...")
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: Camera not opening")
    exit()

print("Camera started successfully!")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error reading frame")
        break

    waste = detect_waste(frame)

    current_time = time.time()

    # delay-based detection
    if waste and (current_time - last_detection_time > DETECTION_DELAY) and bin_level < MAX_LEVEL:
        bin_level += 1
        last_detection_time = current_time

    # display detection
    if waste:
        cv2.putText(frame, "Waste Detected!", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    else:
        cv2.putText(frame, "No Waste", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    # show bin level
    cv2.putText(frame, f"Bin Level: {bin_level}/{MAX_LEVEL}", (50,100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

    # 80% warning
    if bin_level >= WARNING_LEVEL and bin_level < MAX_LEVEL:
        cv2.putText(frame, "BIN 80% FULL!", (50,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,165,255), 3)

    # full alert
    if bin_level >= MAX_LEVEL:
        cv2.putText(frame, "BIN FULL!", (50,200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        print("Alert: Dustbin Full! Inform Municipal Office")

        cv2.imshow("Smart Drainage System", frame)
        cv2.waitKey(3000)
        break

    cv2.imshow("Smart Drainage System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()