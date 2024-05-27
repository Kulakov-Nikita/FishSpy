import cv2
import numpy as np
from FishDetector import FishSpy
from SectorController import SectorController
from SectorMarker import SectorMarker


class VideoProcessor:
    def __init__(self, fishDetector: FishSpy, sectorMarker: SectorMarker, sectorController: SectorController):
        self.fishDetector: FishSpy = fishDetector
        self.sectorMarker: SectorMarker = sectorMarker
        self.sectorController: SectorController = sectorController

    def get_demo(self, path_to_input_video: str, video_resolution: tuple = (1280, 720), fps: int = 30):
        cap = cv2.VideoCapture(path_to_input_video)

        if not cap.isOpened():
            raise Exception("Error opening video file: " + path_to_input_video)

        ret, frame = cap.read()
        if ret:
            sectorMarker.draw_sectors(frame)
            return frame

    def process_video(self, path_to_input_video: str, batch_size: int = 32,
                     video_duration_frames: int = None, video_resolution: tuple = (1280, 720), fps: int = 30):

        frames = np.zeros((batch_size, video_resolution[1], video_resolution[0], 3)).astype('uint8')
        cap = cv2.VideoCapture(path_to_input_video)

        counter: int = 0
        in_batch_counter: int = 0
        batch_counter: int = 0
        rectangles = np.zeros((video_duration_frames, 4))

        if not cap.isOpened():
            raise Exception("Error opening video file: " + path_to_input_video)
        while cap.isOpened() and counter < video_duration_frames:
            ret, frame = cap.read()
            if ret:
                frames[in_batch_counter] = frame
                in_batch_counter += 1
                counter += 1

                if in_batch_counter == batch_size:
                    in_batch_counter = 0

                    rectangles[batch_counter*batch_size:(batch_counter+1)*batch_size] = (
                        self.fishDetector.detect_fish_batch(frames, video_resolution))

                    batch_counter += 1
                    print(f"Progress: {batch_counter}/{video_duration_frames//batch_size} batches processed")

        rectangle_corners = [SectorController.rect_to_point_array(rectangle[0], rectangle[1], rectangle[2], rectangle[3]) for rectangle in rectangles]

        rectangle_sectors = [self.sectorMarker.rect_to_sector_array(rectangle) for rectangle in rectangle_corners]


        for rectangle in rectangle_sectors:
            self.sectorController.new_frame(rectangle)


        #return rectangle_sectors

#fishDetector = FishSpy("D:/FishSpy/models/tmp/torch_eight_19.pth", min_contour_area=100)
#fishDetector = FishSpy("models/torch_eight.pth", min_contour_area=100)

#sectorMarker = SectorMarker((700, 395), 45)
#sectorMarker.set_line_angles((10, 40, 65, 100, 130, 165, 195, 225, 250, 280, 310, 340))
#sectorController = SectorController(ignore_frames_before=90)

#videoProcessor = VideoProcessor(fishDetector, sectorMarker, sectorController)

#import matplotlib.pyplot as plt
#plt.imshow(videoProcessor.get_demo('D:/FishSpy/videos/intakt_10.mp4'))
#plt.show()

#print(videoProcessor.process_video('D:/FishSpy/videos/intakt_10.mp4', video_duration_frames=3200))
#print(videoProcessor.process_video('D:/FishSpy/videos/fenibut_2.mp4', video_duration_frames=3200))
#videoProcessor.process_video('input/fenibut_2.mp4', video_duration_frames=6400)
#sectorController.print_info()


