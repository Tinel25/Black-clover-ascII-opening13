import cv2
import numpy as np
import os

def video_to_ascii(video_path, output_dir, frames_per_second=10):
    
    ascii_chars = "@%#*+=-:. "

    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return

    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps / frames_per_second)
    frame_count = 0
    ascii_frames = []

    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            # Fond gris
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Yeniden boyutlandır (daha küçük boyut, daha hızlı işlem)
            height, width = gray_frame.shape
            new_width = 550
            new_height = int(new_width * (height / width) / 2)
            resized_frame = cv2.resize(gray_frame, (new_width, new_height))

            # Image en ascii
            ascii_frame = ""
            for row in resized_frame:
                for pixel in row:
                    ascii_frame += ascii_chars[pixel // 32]
                ascii_frame += "\n"
            ascii_frames.append(ascii_frame)

        frame_count += 1

    cap.release()

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "ascii_frames.js"), "w") as f:
        f.write("const frames = [\n")
        for frame in ascii_frames:
            f.write(f"    `{frame}`,\n")
        f.write("];\n")

    print(f"ASCII frames have been saved to {output_dir}/ascii_frames.js")

video_path = "clover_opening13.mp4"  #lien du dossier
output_dir = "./output" 
video_to_ascii(video_path, output_dir)
