import cv2

# try multiple camera indexes
for i in range(3):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera working on index {i}")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("Camera Test", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        break
else:
    print("No camera found!")