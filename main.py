import pyrealsense2 as rs
import numpy as np
import cv2
from AzureVisionLocal import detect_image
from module.object_monitor import ObjectMonitor
import time
# Camera Configuration
img_width=640
img_height=480
cam_fps=30
half_detection_width=150
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, img_width, img_height, rs.format.z16, cam_fps)
config.enable_stream(rs.stream.color, img_width, img_height, rs.format.bgr8, cam_fps)
pipeline.start(config)

debug_mode=True
om=ObjectMonitor(img_width, half_detection_width, debug_mode=debug_mode)
tmp_filename='current.jpg'

while True:
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    if not depth_frame or not color_frame:
        continue

    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    cv2.imwrite(tmp_filename,color_image)
    bboxes=detect_image(tmp_filename)
    if debug_mode:
        print(bboxes)
        print(om.process_bboxes(depth_image,bboxes))
        # Stack both images horizontally
        #images = np.hstack((color_image, depth_colormap))
        #print(depth_image[240,320])
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', color_image)
        cv2.waitKey(1)

    time.sleep(5)
    # Show images

# Stop streaming
pipeline.stop()