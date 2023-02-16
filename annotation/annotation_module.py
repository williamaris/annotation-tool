import os
import cv2
import json
from enum import Enum


class AnnotationModule:
    def __init__(self):

        self.frames = []
        self.annotations = {}
        self.frame_index = 0
        self.filename = None
        self.file_index = None
        self.n_files = None

        self.frame_jump = 5

        self.red = (0, 0, 255)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)

        cv2.namedWindow('Annotation Tool')
        cv2.setMouseCallback('Annotation Tool', self.annotate_frame)

    def load_item(self, video, annotations = None):
        
        self.clear()

        self.filename = os.path.basename(video)
        video_capture = cv2.VideoCapture(video)

        while True:
            success, frame = video_capture.read()

            if not success:
                break

            self.frames.append(frame)

        if annotations is not None:
            with open(annotations, 'r') as f:
                data = json.load(f)
                self.annotations = {int(k): data[k] for k in data}


        self.draw_frame()

    def draw_frame(self):
        img = self.frames[self.frame_index].copy()
        
        self.write_to_screen(img, self.filename, 'tl')
        self.write_to_screen(img, f'Frame jump: {self.frame_jump}', 'bl')
        self.write_to_screen(img, f'Frame: {self.frame_index + 1} of {len(self.frames)}', 'br')

        annotated_frame, pos = self.get_frame_annotation()

        if annotated_frame is not None:
            if annotated_frame == self.frame_index:
                cv2.circle(img, (pos[0], pos[1]), 2, self.red, -1)
            else:
                cv2.circle(img, (pos[0], pos[1]), 2, self.green, -1)

        cv2.imshow('Annotation Tool', img)

    def get_next_frame(self):
        self.frame_index += self.frame_jump

        if self.frame_index >= len(self.frames):
            self.frame_index = len(self.frames) - 1

        self.draw_frame()

    def get_previous_frame(self):
        self.frame_index -= self.frame_jump

        if self.frame_index < 0:
            self.frame_index = 0

        self.draw_frame()

    def increase_frame_jump(self):
        self.frame_jump += 1
        self.draw_frame()

    def decrease_frame_jump(self):
        self.frame_jump -= 1

        if self.frame_jump < 1:
            self.frame_jump = 1

        self.draw_frame()

    def annotate_frame(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.annotations[self.frame_index] = [x, y]

        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.annotations.get(self.frame_index) is not None:
                del self.annotations[self.frame_index]
        
        self.draw_frame()

    def get_annotations(self):
        return self.annotations

    def clear(self):
        self.frames = []
        self.annotations = {}
        self.frame_index = 0
        self.filename = None
        self.file_index = None
        self.n_files = None

    def write_to_screen(self, img, text, corner):
        if corner == 'tl':
            position = (10, 18)
        
        elif corner == 'tr':
            size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            width, _ = size
            position = (img.shape[1] -10 - width, 18)
        
        elif corner == 'bl':
            position = (10, img.shape[0] - 10)
        
        elif corner == 'br':
            size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            width, _ = size
            position = (img.shape[1] -10 - width, img.shape[0] - 10)

        else:
            return

        cv2.putText(
            img,
            text,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            self.white,
            1,
            cv2.LINE_AA)

    def get_frame_annotation(self):
        if self.annotations.get(self.frame_index) is not None:
            return (self.frame_index, self.annotations.get(self.frame_index))

        else:
            annotated_frames = sorted(self.annotations.keys())

            for annotated_frame in reversed(annotated_frames):
                if annotated_frame < self.frame_index:
                    return (annotated_frame, self.annotations.get(annotated_frame))

            return (None, None)

    def draw_circle(self, img, pos, color):
        cv2.circle(img, (pos[0], pos[1]), 2, color, -1)
