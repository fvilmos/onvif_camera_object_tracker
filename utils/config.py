####################################################
# Onvif camera calss, hadles snapshots and snapshots
#
# Author: fvilmos
# https://github.com/fvilmos
####################################################

class Config:
    DEBUG = True
    MIN_POS_THRESHOLD = -1.0  # minimum accuracy threshold for object detection
    MAX_POS_THRESHOLD = 1.0  # maximum threshold for object detection
    IP=""               # Camera IP address, leave empty for auto-discovery
    PORT=6688           # Port, default is 80
    USER=""        # Username, fill it if no anonymous access is allowed
    PASS=""       # Password, fill it if no anonymous access is allowed

    MIN_POS_THRESHOLD = -1.0  # minimum accuracy threshold for object detection
    MAX_POS_THRESHOLD = 1.0  # maximum threshold for object detection

    GUARDIAN = False  # use guardian mode, set to True to enable guardian mode

    # NOTE: check the stram url for your camera, this is for SP028 / SP030 (SriHome)
    rtsp_url = f"rtsp://{USER}:{PASS}@{IP}:8554/profile0"   # RTSP URL for the camera stream, high quality
    USE_RTSP = True  # use RTSP stream, set to False to use HTTP stream
    STREAM_RESIZE_TO = (640, 480)  # resize the stream to this resolution
    COCO_90_LABEL_TO_DETECT = {1:"person", 16:"bird", 17:"cat", 18:"dog", }  # COCO labels to detect, 0 is the index for 'person'
    MODEL = './data/frozen_inference_graph.pb'  # path to the model file
    PROTO = './data/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'  # path to the prototxt file
    CONFIDENCE = 0.4  # confidence threshold for object detection

# COCO labels to detect, these are the labels that the model can detect
# source, credits for the list: https://gist.github.com/aallan/fbdf008cffd1e08a619ad11a02b74fa8
# 1 person
# 2 bicycle
# 3 car
# 4 motorcycle
# 5 airplane
# 6 bus
# 7 train
# 8 truck
# 9 boat
# 10 traffic light
# 11 fire hydrant
# 13 stop sign
# 14 parking meter
# 15 bench
# 16 bird
# 17 cat
# 18 dog
# 19 horse
# 20 sheep
# 21 cow
# 22 elephant
# 23 bear
# 24 zebra
# 25 giraffe
# 27 backpack
# 28 umbrella
# 31 handbag
# 32 tie
# 33 suitcase
# 34 frisbee
# 35 skis
# 36 snowboard
# 37 sports ball
# 38 kite
# 39 baseball bat
# 40 baseball glove
# 41 skateboard
# 42 surfboard
# 43 tennis racket
# 44 bottle
# 46 wine glass
# 47 cup
# 48 fork
# 49 knife
# 50 spoon
# 51 bowl
# 52 banana
# 53 apple
# 54 sandwich
# 55 orange
# 56 broccoli
# 57 carrot
# 58 hot dog
# 59 pizza
# 60 donut
# 61 cake
# 62 chair
# 63 couch
# 64 potted plant
# 65 bed
# 67 dining table
# 70 toilet
# 72 tv
# 73 laptop
# 74 mouse
# 75 remote
# 76 keyboard
# 77 cell phone
# 78 microwave
# 79 oven
# 80 toaster
# 81 sink
# 82 refrigerator
# 84 book
# 85 clock
# 86 vase
# 87 scissors
# 88 teddy bear
# 89 hair drier
# 90 toothbrush
