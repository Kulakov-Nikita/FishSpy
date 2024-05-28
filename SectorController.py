import numpy as np


class SectorController:
    prev_rect = (0, 0, 0, 0)

    def __init__(self, ignore_frames_before: int = 0, fps: int = 30):
        self.prev_sectors = np.asarray([])

        self.ignore_frames_before = ignore_frames_before
        self.frame_counter: int = 0
        self.fps = fps

        self.time_at_rest: int = 0  # Кол-во кадров, с рыбой в неподвижном состоянии
        self.time_on_periphery: int = 0  # Кол-во кадров, с рыбой на переферии
        self.time_in_center: int = 0  # Кол-во кадров, с рыбой  центральной зоне
        self.num_of_sector_intersections: int = 0  # Кол-во пересечений секторов

    @staticmethod
    def rect_to_point_array(x, y, w, h):
        if x == -1 and y == -1 and w == -1 and h == -1:
            return SectorController.prev_rect

        SectorController.prev_rect = np.asarray(((x, y), (x + w, y), (x, y + w), (x + w, y + h)))
        return SectorController.prev_rect

    def set_ignore_frames(self, ignore_frames):
        self.ignore_frames_before = ignore_frames

    def new_frame(self, sector_numbers: np.ndarray):
        is_on_periphery: bool = False
        intersect_periphery: bool = False
        self.frame_counter += 1
        if self.frame_counter < self.ignore_frames_before:
            return

        new_intersections: int = 0

        # Считаем кол-во пересечённых секторов
        for number in sector_numbers:
            if number in range(19):
                if number not in self.prev_sectors:  # Рыба не была в данном секторе ранее
                    self.num_of_sector_intersections += 1
                    new_intersections += 1
            else:
                intersect_periphery = True
                new_intersections += 1
                for i in range(19, 32):
                    if i not in self.prev_sectors:
                        intersect_periphery = False
        if intersect_periphery:
            self.num_of_sector_intersections += 1

        # Если рыба не пересекла ни один сектор, считаем её не подвижной в данном кадре
        if new_intersections == 0:
            self.time_at_rest += 1

        # Увеличиваем время пребывания на переферии, если рыба находится в 19..31 секторах
        for sector in sector_numbers:
            if sector in range(19, 32):
                is_on_periphery = True
        if is_on_periphery:
            self.time_on_periphery += 1

        # Увеличиваем время пребывания в центральной зоне, если рыба находится в секторе 0
        if 0 in sector_numbers:
            self.time_in_center += 1

        self.prev_sectors = sector_numbers

    def print_info(self):
        print(f"Кол-во пересечённых секторов: {self.num_of_sector_intersections}\n"
              f"Время в покое: {round(self.time_at_rest / self.fps)}\n"
              f"Время на переферии: {round(self.time_on_periphery / self.fps)}\n"
              f"Время в центре: {round(self.time_in_center / self.fps)}\n"
              f"Общее время: {round(self.frame_counter / self.fps)}")
