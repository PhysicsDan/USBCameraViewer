import cv2

def list_connected_cameras():
    # Iterate through camera indices until no more cameras are found
    camera_index = 0
    connected_cameras = []

    while True:
        cap = cv2.VideoCapture(camera_index)

        # Check if the camera is opened successfully
        if not cap.isOpened():
            break

        # Get camera properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Add camera information to the list
        camera_info = {
            'index': camera_index,
            'width': width,
            'height': height,
            'fps': fps,
        }
        connected_cameras.append(camera_info)

        # Release the camera capture object
        cap.release()

        # Move on to the next camera index
        camera_index += 1

    return connected_cameras

def main():
    # List connected cameras
    connected_cameras = list_connected_cameras()

    if not connected_cameras:
        print("No cameras found.")
    else:
        print("Connected cameras:")
        for camera in connected_cameras:
            print(f"Camera {camera['index']}: {camera['width']}x{camera['height']} at {camera['fps']} FPS")

if __name__ == "__main__":
    main()

