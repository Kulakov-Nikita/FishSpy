# FishSpy
 Проект предназначен для анализа поведения рыбок на видеозаписи эксперимента.
 Для определения положения рыбок используется нейросеть автоэнкодер.
 Программа способна вычеслять следующие значения:
 * количество пересеченных секторов
 * время проведённое на периферии
 * время проведённое в центральной зоне
 * время проведённое в неподвижном состоянии

# main.py
 Видео для обработки необходимо загрузить в папку input в рабочей директории. Видео должно быть в формате .mp4<p>
 Перед запуском видео стоит подобрать параметры: расположение секторов, момент начала протоколирования, длительность видео.
 Это можно сделать с помощью скрипта targeting.py<p>
 После подготовки парметров, их необходимо ввести в консоль. Параметры будут запрошены при запуске main.py<p>
 При желании можно использовать параметры, предложенные программой, введя только положение центра исследуемой области и радиус центрального сектора.<p>
 После ввода параметров начнётся процесс обратоки видео. Программа попытается запуститься на GPU для более быстрого процесса обработки. Если это будет не возможно, то программа будет запущена CPU.
 После обработки видео в консоль будут выведены рассчитаные значения.

# targeting.py
Данный скрипт используется для помощи в подборе параметров. На каждой итерации цикла подбора параметров пользователь вводит параметры (положение центра исследуемой области, радиус центрального сектора, углы границ секторв)
после чего программа демострирует графическое представление полученных секторов.<p> Если пользователя всё устраевает, он может получить параметры для запуска обработки видео в main.py<p>
Если пользователю текущие параметры не подходят, то он может попробовать другие в следующей итерации цикла.
