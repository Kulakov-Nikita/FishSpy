import numpy as np

from SectorController import SectorController
from SectorMarker import SectorMarker
from FishDetector import FishSpy
from VideoProcessor import VideoProcessor
import matplotlib.pyplot as plt
import cv2

# Загружаем нейросеть
fishDetector = FishSpy("models/torch_eight.pth", min_contour_area=100)

# Настраяеваем положение исследуемой области
center_pos_x = int(input("Укажите положение(в пикселях) центра исследуемой области по x: ")) #(700, 935)
center_pos_y = int(input("Укажите положение(в пикселях) центра исследуемой области по y: "))
center_zone_radius = int(input("Укажите радиус(в пикселях) центрального сектора: ")) #45
sectorMarker = SectorMarker((center_pos_x, center_pos_y), center_zone_radius)

# Настраиваем границы секторов
print("Стандартные углы границ сеторов:")
print("0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330\n")
if input("Выбирите действие:\n[1] Использовать стандартные углы\n[2] Ввести пользовательские углы\n") == '2':
    angles = [int(angle) for angle in input("Введите углы(12шт): ").split(",")]
    sectorMarker.set_line_angles(angles)


# Инициализируем обработчик пересечений
ignore_frames = int(input("Введите количество кадров, которые необходимо пропустить с начала видео: ")) #90
sectorController = SectorController(ignore_frames_before=ignore_frames)

# Инициализируем обработчик видео
videoProcessor = VideoProcessor(fishDetector, sectorMarker, sectorController)

# Запускаем обработку видео
video_name = input("Введите название видео(Например: fenibut_2.mp4): ")
video_duration = int(input("Введите длительность видео(в кадрах): "))
videoProcessor.process_video('input/'+video_name, video_duration_frames=video_duration)

# Печатаем результаты в консоль
sectorController.print_info()

