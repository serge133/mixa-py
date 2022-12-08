import os
import cv2
from time import sleep
from datetime import datetime
import sys
from typing import Any
from analyze_video import read_vid
from collections import deque
import threading
# filename = 'security/video.mp4'
# fps = 24.0
# res = '720p'
# seconds = -1

def record(file_path='security/video.mp4', fps=25, res='480p', seconds=-1):
    # Set resolution for the video capture
    # Function adapted from https://kirr.co/0l6qmh
    def change_res(cap, width, height):
        cap.set(3, width)
        cap.set(4, height)

    # Standard Video Dimensions Sizes
    STD_DIMENSIONS =  {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "4k": (3840, 2160),
    }


    # grab resolution dimensions and set video capture to it.
    def get_dims(cap, res='1080p'):
        width, height = STD_DIMENSIONS["480p"]
        if res in STD_DIMENSIONS:
            width,height = STD_DIMENSIONS[res]
        ## change the current caputre device
        ## to the resulting resolution
        change_res(cap, width, height)
        return width, height

    # Video Encoding, might require additional installs
    # Types of Codes: http://www.fourcc.org/codecs.php
    VIDEO_TYPE = {
        'avi': cv2.VideoWriter_fourcc(*'XVID'),
        'mp4': cv2.VideoWriter_fourcc(*'H264'),
        # 'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    }

    def get_video_type(filename):
        filename, ext = os.path.splitext(filename)
        if ext in VIDEO_TYPE:
            return  VIDEO_TYPE[ext]
        return VIDEO_TYPE['avi']



    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(file_path, get_video_type(file_path), 25, get_dims(cap, res))

    total_frames = seconds * fps
    for _ in range(total_frames):
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    out.release()
    cv2.destroyAllWindows()


def get_params():
    params = {
        '--wait': 7,
        '--spv': -1, # Seconds Per Vid
        '--vid_num': 1 # How many videos to record
    }
    args: list[Any] = sys.argv[1:]
    for i in range(0, len(args), 2):
        params[args[i]] = args[i + 1]

    params['--wait'] = int(params['--wait'])
    params['--spv'] = int(params['--spv'])
    params['--vid_num'] = int(params['--vid_num'])

    return params

def arm(seconds_per_vid: int, number_of_vids: int):
    for vidnum in range(number_of_vids):
        vid_label=f'{vidnum}_{datetime.now().timestamp()}'
        vid_path=f'security/video/{vid_label}.mp4'
        record(
            file_path=vid_path,
            res='720p',
            seconds=seconds_per_vid,
            fps=25
        )
        # Create a new thread to process the vid 
        process_vid_thread = threading.Thread(target=read_vid, args=[vid_label])
        process_vid_thread.start()


    

if __name__ == "__main__":
    params = get_params()
    print(f"ARMING... {params['--wait']} seconds")
    sleep(params['--wait'])
    print("ARMED")
    


    # for vidnum in range(params['--vid_num']):
    #     vid_label=f'{vidnum}_{datetime.now().timestamp()}'
    #     vid_path=get_vid_path(vid_label)
        

    #     record(file_path=vid_path, res='720p', seconds=params['--spv'], fps=25)
    #     print('parsing video')

    arm(
        seconds_per_vid=params['--spv'],
        number_of_vids=params['--vid_num'],
    )
        # queue.append(vid_label)

        # while queue:

    print("DISARMED")