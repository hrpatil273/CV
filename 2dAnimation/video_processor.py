import cv2
import pandas as pd
import os


def annotate_video(video_name, output_path: str) -> str:
    video_labels = pd.read_csv('data/train_labels.csv')
    VIDEO_CODEC = "MP4V"
    HELMET_COLOR = (0, 0, 0)  # Black
    IMPACT_COLOR = (0, 0, 255)  # Red
    data_path = 'data/train'
    video_path = f'{data_path}/{video_name}'
    video_name = os.path.basename(video_path)

    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*VIDEO_CODEC), fps, (width, height))
    frame = 0
    while True:
        it_worked, img = vidcap.read()
        if not it_worked:
            break

        # We need to add 1 to the frame count to match the label frame index that starts at 1
        frame += 1

        # Let's add a frame index to the video so we can track where we are
        img_name = f"{video_name}_frame{frame}"
        cv2.putText(img, img_name, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, HELMET_COLOR, thickness=2)

        # Now, add the boxes
        boxes = video_labels.query("video == @video_name and frame == @frame")
        for box in boxes.itertuples(index=False):
            if box.impact == 1 and box.confidence > 1 and box.visibility > 0:  # Filter for definitive head impacts and turn labels red
                color, thickness, duration = IMPACT_COLOR, 20, 5000
            else:
                color, thickness, duration = HELMET_COLOR, 1, 1
            # Add a box around the helmet
            cv2.rectangle(img, (box.left, box.top), (box.left + box.width, box.top + box.height), color,
                          thickness=thickness)
            cv2.putText(img, box.label, (box.left, max(0, box.top - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color,
                        thickness=1)

        # Add a delay to make the impact boxes stay on screen longer
        duration = duration if duration else 1
        for i in range(duration):
            output_video.write(img)

    output_video.release()


# video_labels = pd.read_csv('data/train_labels.csv')
# filename = video_labels['video'][3]
# # output_path = 'static/labeled_' + filename
#
# video_name = filename
# output_path = 'labeled_' + video_name
# annotate_video(video_name, output_path)