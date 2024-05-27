import cv2
import numpy as np

class SectorMarker:
    def __init__(self, center_pos: tuple[int, int], central_zone_radius: float):
        self.center_pos: np.ndarray[int, int] = np.asarray(center_pos)
        self.central_zone_radius: float = central_zone_radius
        self.middle_zone_radius: float = central_zone_radius * 2.85
        self.full_zone_radius: float = central_zone_radius * 5
        self.line_angles_deg: tuple = (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330)

    def set_line_angles(self, line_angles_deg):
        self.line_angles_deg = line_angles_deg

    def get_line(self, angle_rad: float):
        return (
            # Start point
            self.center_pos + np.asarray((self.central_zone_radius * np.cos(angle_rad),
                                          self.central_zone_radius * np.sin(angle_rad))).astype('int'),
            # End point
            self.center_pos + np.asarray((self.full_zone_radius * np.cos(angle_rad),
                                          self.full_zone_radius * np.sin(angle_rad))).astype('int'))

    def draw_sectors(self, img: np.ndarray):
        img = cv2.circle(img, self.center_pos, 45, (0, 255, 0), thickness=2)
        img = cv2.circle(img, self.center_pos, 128, (0, 255, 0), thickness=2)
        img = cv2.circle(img, self.center_pos, 225, (0, 255, 0), thickness=2)

        for i in self.line_angles_deg:
            start_point, end_point = self.get_line(i / 180 * np.pi)
            cv2.line(img, start_point, end_point, (0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

        return img

    def rect_to_sector_array(self, rectangle: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]):
        return np.asarray([self.map_to_sector(point) for point in rectangle])

    def map_to_sector(self, point: np.ndarray):
        # Определяем полярные координады точки
        pos = point - self.center_pos
        dist_from_center = np.linalg.norm(pos)
        theta = np.arctan(pos[1] / pos[0]) / np.pi * 180

        if pos[1] >= 0:
            if pos[0] >= 0:
                pass  # [0; 90]
            else:
                theta += 180  # (90; 180]
        else:
            if pos[0] <= 0:
                theta += 180  # (180; 270]
            else:
                theta += 360  # (270; 360]

        #print(f"dist: {dist_from_center} | theta: {theta}")

        # Определение круга
        if dist_from_center <= self.central_zone_radius:
            return 0
        elif dist_from_center <= self.middle_zone_radius:
            # Если угол больше 0, но меньше угла нулевой линии
            if theta < self.line_angles_deg[0]:
                return 6
            # Находим сектора, следующие по часовой стрелке (включая текущий)
            next_sectors = [i//2 for i, ang in enumerate(self.line_angles_deg) if theta >= ang]
            return next_sectors[-1] + 1
        elif dist_from_center <= self.full_zone_radius:
            # Если угол больше 0, но меньше угла нулевой линии
            if theta < self.line_angles_deg[0]:
                return 18
            # Находим сектора, следующие по часовой стрелке (включая текущий)
            next_sectors = [i for i, ang in enumerate(self.line_angles_deg) if theta >= ang]
            return next_sectors[-1] + 7
        else:
            if theta < self.line_angles_deg[0]:
                return 19
            # Все сектора от 19 до 31 считаются однин сектором - перефирией
            next_sectors = [i for i, ang in enumerate(self.line_angles_deg) if theta >= ang]
            return next_sectors[-1] + 19
