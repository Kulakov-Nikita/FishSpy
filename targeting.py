from SectorMarker import SectorMarker
from VideoProcessor import VideoProcessor
import matplotlib.pyplot as plt

# Настраяеваем положение исследуемой области, используя стандартные параметры
center_pos_x = 700
center_pos_y = 935
center_zone_radius = 45
sectorMarker = SectorMarker((center_pos_x, center_pos_y), center_zone_radius)

# Инициализируем обработчик видео
videoProcessor = VideoProcessor(None, sectorMarker, None)

video_name = input("Введите название видео(Например: fenibut_2.mp4): ")

keep_targeting = True
while keep_targeting:
    center_pos_x = int(input("Укажите положение(в пикселях) центра исследуемой области по x: "))
    center_pos_y = int(input("Укажите положение(в пикселях) центра исследуемой области по y: "))
    sectorMarker.center_pos = (center_pos_x, center_pos_y)
    center_zone_radius = int(input("Укажите радиус(в пикселях) центрального сектора: "))
    sectorMarker.central_zone_radius = center_zone_radius

    print("Текущие углы границ сеторов:")
    print(f"{sectorMarker.line_angles_deg}\n")
    if input("Выбирите действие:\n[1] Использовать текущие углы\n[2] Ввести новые углы\n") == '2':
        angles = [int(angle) for angle in input("Введите углы(12шт): ").split(",")]
        sectorMarker.set_line_angles(angles)
        print(f"Установленны углы: {sectorMarker.line_angles_deg}")

    plt.imshow(videoProcessor.get_demo('input/'+video_name))
    plt.show()
    keep_targeting = input("Подтвердить текущее положение исследуемой области? [y/n]: ") == 'n'

print(f"Итог:\nКоординаты центра: (x: {sectorMarker.center_pos[0]}; y: {sectorMarker.center_pos[1]})\n"
      f"Радиус центрального сектора: {sectorMarker.central_zone_radius}\n"
      f"Углы границ секторов: {sectorMarker.line_angles_deg}")

