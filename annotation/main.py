import os
import cv2
import json
import argparse

from annotation_module import AnnotationModule

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, help="Input directory")

root = parser.parse_args().input

if not os.path.isdir(root):
    print("Input directory doesn't exist or is not a directory")
    exit()

# Input dir filtering
files_to_remove = []
files = sorted(os.listdir(root))

for file in files:
    if not file.endswith('.mp4'):
        files_to_remove.append(file)

for file in files_to_remove:
    files.remove(file)


# Output dir
output_dir = os.path.join(root, 'annotations')

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

idx = 0
should_run = True
annotation_module = AnnotationModule()

annotation_module.load_item(os.path.join(root, files[0]))

while idx < len(files):

    if not should_run:
        break

    print(f'Processing file {idx + 1} of {len(files)}')

    video_file = os.path.join(root, files[idx])
    annotations_file = os.path.join(output_dir, files[idx].replace('.mp4', '.json'))

    if not os.path.exists(annotations_file):
        annotation_module.load_item(video_file)

    else:
        annotation_module.load_item(video_file, annotations_file)

    while True:
        key = cv2.waitKey(1)

        if key == 27:
            should_run = False
            break

        elif key == ord('a'):
            annotation_module.get_previous_frame()
        
        elif key == ord('d'):
            annotation_module.get_next_frame()

        elif key == ord('1'):
            annotation_module.decrease_frame_jump()

        elif key == ord('2'):
            annotation_module.increase_frame_jump()

        elif key == ord('s') or key == ord(' '):

            annotations = annotation_module.get_annotations()

            with open(annotations_file, 'w') as f:
                json.dump(annotations, f, indent = 4)

            idx += 1
            
            break

        elif key == ord('w'):

            annotations = annotation_module.get_annotations()
            output_path = os.path.join(output_dir, files[0].replace('.mp4', '.json'))

            with open(output_path, 'w') as f:
                json.dump(annotations, f, indent = 4)
            
            idx -= 1

            if idx < 0:
                idx = 0

            break

cv2.destroyAllWindows()