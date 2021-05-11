#!/usr/bin/env python3

import depthai as dai

pipeline = dai.Pipeline()

# Nodes
colorCam = pipeline.create(dai.node.ColorCamera)
colorCam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
monoCam = pipeline.create(dai.node.MonoCamera)
monoCam2 = pipeline.create(dai.node.MonoCamera)
ve1 = pipeline.create(dai.node.VideoEncoder)
ve2 = pipeline.create(dai.node.VideoEncoder)
ve3 = pipeline.create(dai.node.VideoEncoder)

ve1Out = pipeline.create(dai.node.XLinkOut)
ve2Out = pipeline.create(dai.node.XLinkOut)
ve3Out = pipeline.create(dai.node.XLinkOut)

# Properties
monoCam.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoCam2.setBoardSocket(dai.CameraBoardSocket.RIGHT)
ve1Out.setStreamName('ve1Out')
ve2Out.setStreamName('ve2Out')
ve3Out.setStreamName('ve3Out')

# Setting to 26fps will trigger error
ve1.setDefaultProfilePreset(1280, 720, 25, dai.VideoEncoderProperties.Profile.H264_MAIN)
ve2.setDefaultProfilePreset(3840, 2160, 25, dai.VideoEncoderProperties.Profile.H265_MAIN)
ve3.setDefaultProfilePreset(1280, 720, 25, dai.VideoEncoderProperties.Profile.H264_MAIN)

# Link nodes
monoCam.out.link(ve1.input)
colorCam.video.link(ve2.input)
monoCam2.out.link(ve3.input)

ve1.bitstream.link(ve1Out.input)
ve2.bitstream.link(ve2Out.input)
ve3.bitstream.link(ve3Out.input)


# Connect and start the pipeline
with dai.Device(pipeline) as dev:

    # Prepare data queues
    outQ1 = dev.getOutputQueue('ve1Out', maxSize=30, blocking=True)
    outQ2 = dev.getOutputQueue('ve2Out', maxSize=30, blocking=True)
    outQ3 = dev.getOutputQueue('ve3Out', maxSize=30, blocking=True)

    # Processing loop
    with open('mono1.h264', 'wb') as fileMono1H264, open('color.h265', 'wb') as fileColorH265, open('mono2.h264', 'wb') as fileMono2H264:
        print("Press Ctrl+C to stop encoding...")
        while True:
            try:
                # Empty each queue
                while outQ1.has():
                    outQ1.get().getData().tofile(fileMono1H264)

                while outQ2.has():
                    outQ2.get().getData().tofile(fileColorH265)

                while outQ3.has():
                    outQ3.get().getData().tofile(fileMono2H264)
            except KeyboardInterrupt:
                break

    print("To view the encoded data, convert the stream file (.h264/.h265) into a video file (.mp4), using commands below:")
    cmd = "ffmpeg -framerate 25 -i {} -c copy {}"
    print(cmd.format("mono1.h264", "mono1.mp4"))
    print(cmd.format("mono2.h264", "mono2.mp4"))
    print(cmd.format("color.h265", "color.mp4"))
