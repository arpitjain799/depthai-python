#!/usr/bin/env python3

import cv2
import depthai as dai
import numpy as np

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
colorCam = pipeline.create(dai.node.ColorCamera)
colorCam.setBoardSocket(dai.CameraBoardSocket.RGB)
colorCam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
colorCam.setVideoSize(1920, 1080)

# Create output
xoutVideo = pipeline.create(dai.node.XLinkOut)
xoutVideo.setStreamName("video")
xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

colorCam.video.link(xoutVideo.input)

# Connect and start the pipeline
with dai.Device(pipeline) as device:

    video = device.getOutputQueue(name="video", maxSize=1, blocking=False)

    while True:
        # Get preview and video frames
        videoIn = video.get()

        # Get BGR frame from NV12 encoded video frame to show with opencv
        # Visualizing the frame on slower hosts might have overhead
        cv2.imshow("video", videoIn.getCvFrame())

        if cv2.waitKey(1) == ord('q'):
            break
