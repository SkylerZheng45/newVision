import pyrealsense2 as rs
import numpy as np
import cv2
from AzureVisionLocal import detect_image
# Camera Configuration
img_width=640
img_height=480
cam_fps=30
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, img_width, img_height, rs.format.z16, cam_fps)
config.enable_stream(rs.stream.color, img_width, img_height, rs.format.bgr8, cam_fps)
pipeline.start(config)

debug_mode=False
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
    if debug_mode:
        print(detect_image(tmp_filename))
        # Stack both images horizontally
        #images = np.hstack((color_image, depth_colormap))
        print(depth_image[240,320])
    # Show images
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', color_image)
    cv2.waitKey(1)

# Stop streaming
pipeline.stop()