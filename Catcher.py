import torch
import numpy as np
import cv2


class Catcher:
    def __init__(self, path_to_model: str, min_contour_area: int = 10, device: str = 'GPU', batch_size: int = 32):
        self.batch_size: int = batch_size
        self.min_contour_area: int = min_contour_area
        self.model = torch.load(path_to_model)
        self.model.eval()
        self.device: str = device

        if device == 'GPU':
            if torch.cuda.is_available():
                self.model = self.model.cuda()
            else:
                raise Exception("GPU isn't available")
        elif device == 'CPU':
            pass
        else:
            raise Exception("Unknown unit: " + device)

    def detect_fish_batch(self, img: np.ndarray, video_resolution: tuple = (1280, 720)) -> np.ndarray:
        img = img.reshape((len(img), video_resolution[1], video_resolution[0], 3))
        out_img = img.copy()

        if self.device == 'GPU':
            img_tensor = torch.tensor(img, dtype=torch.float32, device='cuda')
        else:
            img_tensor = torch.tensor(img, dtype=torch.float32, device='CPU')

        img_tensor = img_tensor.permute(0, 3, 1, 2)
        pred = self.model(img_tensor).cpu().detach().numpy().reshape(len(img), video_resolution[1],
                                                                     video_resolution[0]).astype('uint8')


        for pic, mask in zip(out_img, pred):
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            large_contours = [cnt for cnt in contours if
                              cv2.contourArea(cnt) > self.min_contour_area]

            if len(large_contours) > 0:
                correct_cnt = np.argmax([cv2.contourArea(cnt) for cnt in large_contours])
                pic = cv2.drawContours(pic, large_contours[correct_cnt], -1, (0, 255, 0), thickness=2)

        return out_img

    def process_video(self, path_to_input_video: str, path_to_output_video: str, batch_size: int = 32,
                     video_duration_sec: int = None, video_resolution: tuple = (1280, 720), fps: int = 30):

        frames = np.zeros((batch_size, video_resolution[1], video_resolution[0], 3)).astype('uint8')
        cap = cv2.VideoCapture(path_to_input_video)
        #writer = cv2.VideoWriter(path_to_output_video, cv2.VideoWriter_fourcc(*"MJPG"), fps, video_resolution)
        writer = cv2.VideoWriter(path_to_output_video, cv2.VideoWriter_fourcc(*"mp4v"), fps, video_resolution)

        counter: int = 0
        in_batch_counter: int = 0
        batch_counter: int = 0
        video_duration_frames: int = video_duration_sec * fps

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

                    for pic in self.detect_fish_batch(frames, video_resolution=video_resolution):
                        writer.write(pic)

                    batch_counter += 1
                    print(f"Progress: {batch_counter}/{video_duration_frames // batch_size} batches processed")

            else:
                cap.release()
        writer.release()


path_to_model: str = "models/torch_eight.pth"
min_contour_area: int = 100
path_to_input_video: str = "../videos/intakt_10.mp4"
path_to_output_video: str = "../videos__result/intakt_10.mp4"

catcher: Catcher = Catcher(path_to_model, min_contour_area)
catcher.process_video(path_to_input_video, path_to_output_video, video_duration_sec=300)
