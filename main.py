import pyrealsense2 as rs
import numpy as np
import cv2

# Camera Configuration
img_width=640
img_height=480
cam_fps=30
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, img_width, img_height, rs.format.z16, cam_fps)
config.enable_stream(rs.stream.color, img_width, img_height, rs.format.bgr8, cam_fps)
pipeline.start(config)

while True:
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    if not depth_frame or not color_frame:
        continue

    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    # Stack both images horizontally
    images = np.hstack((color_image, depth_colormap))
    print(depth_image[240,320])
    # Show images
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', images)
    cv2.waitKey(1)

# Stop streaming
pipeline.stop()