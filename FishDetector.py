import torch
import numpy as np
import cv2


class FishSpy:
    def __init__(self, path_to_model: str, mode: str = 'GPU', batch_size: int = 32, min_contour_area: int = 10) -> None:
        self.batch_size = batch_size
        self.min_contour_area = min_contour_area
        self.model = torch.load(path_to_model)
        self.model.eval()
        self.mode = mode

        if mode == 'GPU':
            if torch.cuda.is_available():
                self.model = self.model.cuda()
            else:
                raise Exception("GPU isn't available")
        elif mode == 'CPU':
            pass
        else:
            raise Exception("Unknown unit: " + mode)

    def detect_fish_batch(self, img: np.ndarray, video_resolution: tuple = (1280, 720)) -> np.ndarray:
        img = img.reshape((len(img), video_resolution[1], video_resolution[0], 3))

        if self.mode == 'GPU':
            img_tensor = torch.tensor(img, dtype=torch.float32, device='cuda')
        else:
            img_tensor = torch.tensor(img, dtype=torch.float32, device='CPU')

        img_tensor = img_tensor.permute(0, 3, 1, 2)
        pred = self.model(img_tensor).cpu().detach().numpy().reshape(len(img), video_resolution[1], video_resolution[0]).astype(
            'uint8')

        answer = np.zeros((self.batch_size, 4))

        for i, mask in enumerate(pred):
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            large_contours = [cnt for cnt in contours if
                              cv2.contourArea(cnt) > self.min_contour_area]

            if len(large_contours) > 0:
                correct_cnt = np.argmax([cv2.contourArea(cnt) for cnt in large_contours])
                answer[i] = cv2.boundingRect(large_contours[correct_cnt])
            else:
                answer[i] = [-1, -1, -1, -1]

        return answer

    def detect_fish(self, img: np.ndarray, video_resolution: tuple = (1280, 720)):
        img = img.reshape((1, video_resolution[1], video_resolution[0], 3))

        if self.mode == 'GPU':
            img_tensor = torch.tensor(img, dtype=torch.float32, device='cuda')
        else:
            img_tensor = torch.tensor(img, dtype=torch.float32, device='CPU')

        img_tensor = img_tensor.permute(0, 3, 1, 2)
        pred = self.model(img_tensor).cpu().detach().numpy().reshape(video_resolution[1], video_resolution[0]).astype(
            'uint8')

        contours, hierarchy = cv2.findContours(pred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        large_contours = [cnt for cnt in contours if
                          cv2.contourArea(cnt) > self.min_contour_area]

        correct_cnt = np.argmax([cv2.contourArea(cnt) for cnt in large_contours])

        return cv2.boundingRect(large_contours[correct_cnt])
