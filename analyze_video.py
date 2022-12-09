import cv2
import numpy as np
from collections import deque 
import os
# from discord_api import send_message

"""HOW MUCH OF THE PIXELS SHOULD CHANGE TO BE CONSIDERED CHANGED"""
# THRESHOLD = 25
# if camera is very grainy make this higher 
THRESHOLD = 50
"""ISLAND SIZE IS THE AMOUNT OF PIXELS THAT HAVE CHANGED THAT YOU WOULD CONSIDER DRAWING A RECTANGLE AROUND AND ALERTING """
# ISLAND_SIZE = 25
# if you care about small stuff being detected make this smaller
ISLAND_SIZE = 50
"""OPTIMIZER (>) | SAVES THE FIRST IMAGE THEN SKIP FRAMES AND COMPARE"""
# Skips n amount of frames and compares first and last frame 
FRAME_SKIP = 6
"""OPTIMIZE (>) | CHECK EVERY 16 PIXELS SPACED APART IN AN IMAGE"""
# checks every 16 pixels of the image make smaller if you want to detect small objects 
GRID = 16
"""OPTIMIZE (>) | HOW MANY PIXELS TO SKIP WHEN DOING DFS"""
# make smaller if you want to detect small objects 
DFS_SKIP = 2

def outOfBound(matrix, pixel_x, pixel_y):
    return (pixel_x > len(matrix[0]) - 1 or pixel_y > len(matrix) - 1 or pixel_x < 0 or pixel_y < 0)

def dfs(matrix, x, y, visited, og, frame_num):
    if outOfBound(matrix, x, y) or matrix[y][x] < THRESHOLD or f"{x},{y}" in visited:
        return 0 

    queue = deque()
    queue.append([x, y])
    count: int = 0
    
    # For drawing A rectangle
    top_left = [float('inf'), float('inf')]
    bottom_right = [0, 0]



    while queue:
        pixel_x, pixel_y = queue.popleft()

        if outOfBound(matrix, pixel_x, pixel_y) or matrix[pixel_y][pixel_x] < THRESHOLD or f"{pixel_x},{pixel_y}" in visited:
            continue

        top_left = [min(top_left[0], pixel_x), min(top_left[1], pixel_y)]
        bottom_right = [max(bottom_right[0], pixel_x), max(bottom_right[1], pixel_y)]
        og[pixel_y][pixel_x] = [0, 0, 255]
        count += 1
        visited.add(f"{pixel_x},{pixel_y}")

        queue.append([pixel_x + DFS_SKIP, pixel_y])
        queue.append([pixel_x - DFS_SKIP, pixel_y])
        queue.append([pixel_x, pixel_y + DFS_SKIP])
        queue.append([pixel_x, pixel_y - DFS_SKIP])

        
    top_left[0] -= 20
    top_left[1] -= 20
    bottom_right[0] += 20
    bottom_right[1] += 20
    if count > ISLAND_SIZE:
        cv2.rectangle(og, top_left, bottom_right, (0, 0, 255), thickness=1, lineType=cv2.LINE_8)  
        print(f"found change in frame {frame_num} at ({x}, {y}) with island size: {count} ")
        # send_message(f"found change in frame {frame_num} at ({x}, {y}) with island size: {count} ")
        # annot_img(og, x, y, str(count))

    return count

def annot_img(image, x, y, text):
    # cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness= 3, lineType=cv2.LINE_8) 
    cv2.putText(image, text, (x, y), fontFace = cv2.FONT_HERSHEY_TRIPLEX, fontScale = 1, color = (0, 0, 255))
    # cv2.imshow('Motion Camera', image)
    # cv2.waitKey(0)


def process_image(compare, img, count, og, label: str):
    img = img.astype('int16')
    compare = compare.astype('int16')
    change = compare - img
    change = np.abs(change)

    visited = set()
    total_changed_pixels = 0

    # DFS
    for y in range(0, len(change), GRID):  # Optimized 
        for x in range(0, len(change[0]), GRID): # Optimized
            total_changed_pixels += dfs(change, x, y, visited, og, frame_num=count)

    if total_changed_pixels >= ISLAND_SIZE:
        annot_img(og, 30, 30, f"{total_changed_pixels} pixels displaced")
        path = f'security/trigger/{label}'
        if not os.path.exists(path):
            os.mkdir(path)
        cv2.imwrite(f"{path}/frame_{count}_{total_changed_pixels}.jpg", og)     # save frame as JPEG file      
        # send_message(f":alarm_clock: MOTION DETECTED of size {total_changed_pixels} px! :alarm_clock:")
    # cv2.imwrite(f"change/frame_{count}.jpg", change)     # save frame as JPEG file      

def read_vid(video_label: str):
    vidcap = cv2.VideoCapture(f"security/video/{video_label}.mp4")
    success,image = vidcap.read()
    base = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite(f"security/trigger/{video_label}/base.jpg", base)     # save frame as JPEG file      

    frame_count = 0
    while success:
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Optimization Only
        if frame_count % FRAME_SKIP == FRAME_SKIP - 1:
            process_image(compare=base, img=img, count=frame_count, og=image, label=video_label)
        if frame_count % FRAME_SKIP == 0:
            # Reset the comparer image 
            base = img

        success,image = vidcap.read()
        frame_count += 1

    print("processed job")

# def main():
#     for filename in os.listdir('security/video'):
#         # BAD 
#         if filename == '.DS_Store':
#             continue
#         read_vid(filename[:-4], f'security/video/{filename}')

# if __name__ == "__main__":
    # main()