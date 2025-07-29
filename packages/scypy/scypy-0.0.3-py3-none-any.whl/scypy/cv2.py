
def cv2(number):
        if number == 0:
            return'''
            1 -  улучшение изображения(инверсия, гамма, логарифмическое, степенное...)
            2 - афинные преобразование
            3 - все фильтры
            4 - морфологические операции
            5 -  преобразования фурье
            6 - трекинг(deepsort/sort)
            7 -  images/sign_language.zip + разные conv
            8 - images/eng_handwritten.zip + ранняя остановка
            9 - images/clothes_multi.zip + разные лейблы
            10 - images/chars.zip + аугментация'''
        elif number == 1:
            return '''import cv2
import numpy as np
import matplotlib.pyplot as plt

def enhance_image_all_methods(image_path):
    # Загружаем изображение в градациях серого
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Ошибка загрузки изображения")
        return

    methods = {}

    # 1. Инверсия изображения
    inverted = 255 - img
    methods['Inversion'] = inverted

    # 2. Степенное преобразование (гамма-коррекция)
    gamma = 2.2
    gamma_corrected = np.array(255 * (img / 255) ** gamma, dtype='uint8')
    methods[f'Gamma Correction (γ={gamma})'] = gamma_corrected

    # 3. Логарифмическое преобразование
    c = 255 / np.log(1 + np.max(img))
    log_transformed = np.array(c * np.log(1 + img), dtype='uint8')
    methods['Log Transformation'] = log_transformed

    # 4. Эквализация гистограммы
    hist_eq = cv2.equalizeHist(img)
    methods['Histogram Equalization'] = hist_eq

    # 5. Адаптивное выравнивание гистограммы с ограничением контраста (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(img)
    methods['CLAHE'] = clahe_img

    # 6. Контрастное растяжение
    min_val, max_val = np.min(img), np.max(img)
    contrast_stretched = np.array(255 * (img - min_val) / (max_val - min_val), dtype='uint8')
    methods['Contrast Stretching'] = contrast_stretched

    # 7. Сигмоидальная коррекция
    gain = 10
    cutoff = 128
    sigmoid = 255 / (1 + np.exp(-gain * ((img - cutoff) / 255.0)))
    sigmoid_corrected = np.array(sigmoid, dtype='uint8')
    methods['Sigmoid Correction'] = sigmoid_corrected

    # Вывод результатов
    n = len(methods)
    plt.figure(figsize=(14, 3 * n))
    
    for i, (title, result) in enumerate(methods.items()):
        # Изображение
        plt.subplot(n, 2, 2*i + 1)
        plt.imshow(result, cmap='gray')
        plt.title(title)
        plt.axis('off')

        # Гистограмма
        plt.subplot(n, 2, 2*i + 2)
        plt.hist(result.ravel(), bins=256, range=(0, 256), color='black')
        plt.title(f'{title} Histogram')
        plt.tight_layout()

    plt.show()

    # Выводы
    print("\nВыводы по методам:")
    print("- Инверсия меняет яркое на тёмное и наоборот.")
    print("- Гамма-коррекция регулирует освещенность: γ>1 делает темнее, γ<1 — светлее.")
    print("- Логарифмическое преобразование усиливает темные детали.")
    print("- Эквализация гистограммы улучшает контраст на изображениях с узким динамическим диапазоном.")
    print("- CLAHE работает локально и полезен при неравномерном освещении.")
    print("- Контрастное растяжение расширяет интенсивности на весь диапазон (0–255).")
    print("- Сигмоидальная коррекция улучшает контраст в средней зоне, сглаживая крайние значения.")

# Пример использования:
# enhance_image_all_methods('path_to_your_image.jpg')
'''
        elif number == 2:
            return '''
            import cv2
import numpy as np
import matplotlib.pyplot as plt

def affine_transformations(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Ошибка загрузки изображения")
        return

    rows, cols = img.shape[:2]
    methods = {}

    # 1. Перенос (сдвиг)
    dx, dy = 50, 30
    M_translate = np.float32([[1, 0, dx], [0, 1, dy]])
    translated = cv2.warpAffine(img, M_translate, (cols, rows))
    methods['Translation (dx=50, dy=30)'] = translated

    # 2. Вращение
    angle = 45
    center = (cols // 2, rows // 2)
    M_rotate = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M_rotate, (cols, rows))
    methods['Rotation (45°)'] = rotated

    # 3. Масштабирование (увеличение)
    scale_factor = 1.5
    scaled = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    methods['Scaling 1.5x (Bilinear)'] = scaled

    # 4. Интерполяции (уменьшение)
    half_size = (cols // 2, rows // 2)

    resized_nearest = cv2.resize(img, half_size, interpolation=cv2.INTER_NEAREST)
    methods['Resize 0.5x (Nearest)'] = resized_nearest

    resized_bilinear = cv2.resize(img, half_size, interpolation=cv2.INTER_LINEAR)
    methods['Resize 0.5x (Bilinear)'] = resized_bilinear

    resized_bicubic = cv2.resize(img, half_size, interpolation=cv2.INTER_CUBIC)
    methods['Resize 0.5x (Bicubic)'] = resized_bicubic

    # Отображение изображений + гистограмм
    n = len(methods)
    plt.figure(figsize=(12, 4 * n))

    for i, (title, result) in enumerate(methods.items()):
        # Преобразование в градации серого для гистограммы
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

        # Изображение
        plt.subplot(n, 2, 2 * i + 1)
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        plt.title(title)
        plt.axis('off')

        # Гистограмма яркости
        plt.subplot(n, 2, 2 * i + 2)
        plt.hist(gray.ravel(), bins=256, range=(0, 256), color='black')
        plt.title(f'{title} - Histogram')

    plt.tight_layout()
    plt.show()

    # Выводы
    print("\nВыводы:")
    print("- Аффинные преобразования сохраняют прямые линии и параллельность.")
    print("- Перенос просто сдвигает изображение, гистограмма почти не меняется.")
    print("- Вращение и масштабирование могут изменить распределение яркости, особенно если происходит обрезка.")
    print("- Интерполяции влияют на гладкость: Bicubic — самая мягкая, Nearest — грубая.")
    print("- При сильном масштабировании bicubic может давать наилучший визуальный результат.")
'''
        elif number == 3:
            return '''
            import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

def all_filters(image_path):
    # Загрузка изображения
    img = cv2.imread(image_path)
    if img is None:
        print("Ошибка загрузки изображения")
        return

    # Перевод в градации серого (упрощает обработку фильтрами)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Словарь для хранения результатов
    methods = {}

    # === 1. Гауссов фильтр ===
    # Сглаживает изображение, устраняет мелкий шум
    # ksize=(5,5) — размер ядра, sigmaX — стандартное отклонение по X
    gaussian = cv2.GaussianBlur(gray, (5, 5), sigmaX=1)
    methods['Gaussian Blur'] = gaussian

    # === 2. Фильтр среднего (усреднение) ===
    # Каждый пиксель заменяется средним значением соседей
    mean = cv2.blur(gray, (5, 5))
    methods['Mean Filter'] = mean

    # === 3. Медианный фильтр ===
    # Хорошо справляется с шумом «соль-перец»
    # ksize=5 — размер окна 5x5
    median = cv2.medianBlur(gray, 5)
    methods['Median Filter'] = median

    # === 4. Билатеральный фильтр ===
    # Сохраняет края, сглаживая шум
    # d — диаметр области, sigmaColor — фильтрация по цвету, sigmaSpace — по пространству
    bilateral = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
    methods['Bilateral Filter'] = bilateral

    # === 5. Фильтр Собеля (градиенты) ===
    # Вычисляет производные по x и y, усиливает границы
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)  # по X
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)  # по Y
    sobel = cv2.magnitude(sobelx, sobely)                # итоговая амплитуда градиента
    sobel = np.uint8(np.clip(sobel, 0, 255))
    methods['Sobel Filter (Edges)'] = sobel

    # === 6. Лапласиан ===
    # Второй производный оператор, подчеркивает быстрые изменения
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian = np.uint8(np.clip(np.abs(laplacian), 0, 255))
    methods['Laplacian Filter'] = laplacian

    # === 7. Unsharp Masking (маска резкости) ===
    # Повышает резкость изображения путём вычитания размытой копии
    blurred = cv2.GaussianBlur(gray, (9, 9), 10.0)
    unsharp = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)
    # gray * 1.5 - blurred * 0.5
    methods['Unsharp Masking'] = unsharp

    # === 8. Фильтр Прюитта (Prewitt) ===
    # Похож на Собеля, но проще по вычислениям
    kernelx = np.array([[1, 0, -1],
                        [1, 0, -1],
                        [1, 0, -1]], dtype=np.float32)  # по X

    kernely = np.array([[1,  1,  1],
                        [0,  0,  0],
                        [-1, -1, -1]], dtype=np.float32)  # по Y

    prewitt_x = ndimage.convolve(gray.astype(np.float32), kernelx)
    prewitt_y = ndimage.convolve(gray.astype(np.float32), kernely)
    prewitt = np.hypot(prewitt_x, prewitt_y)  # вычисляем амплитуду градиента
    prewitt = np.uint8(np.clip(prewitt, 0, 255))
    methods['Prewitt Filter (Edges)'] = prewitt

    # === 9. Детектор границ Кэнни (Canny) ===
    # Мощный алгоритм с порогами, подавлением немаксимумов
    # Пороговые значения 100 и 200
    canny = cv2.Canny(gray, 100, 200)
    methods['Canny Edge Detector'] = canny

    # === Визуализация изображений и гистограмм ===
    n = len(methods)
    plt.figure(figsize=(12, 4 * n))

    for i, (title, result) in enumerate(methods.items()):
        # Отображение результата фильтра
        plt.subplot(n, 2, 2 * i + 1)
        plt.imshow(result, cmap='gray')
        plt.title(title)
        plt.axis('off')

        # Гистограмма яркости
        plt.subplot(n, 2, 2 * i + 2)
        plt.hist(result.ravel(), bins=256, range=(0, 256), color='black')
        plt.title(f'{title} - Histogram')

    plt.tight_layout()
    plt.show()

    # === Выводы ===
    print("\nВыводы:")
    print("- Gaussian, Median, Mean — убирают шум. Median особенно хорош при шуме 'соль-перец'.")
    print("- Bilateral — уникален: сглаживает, но сохраняет края.")
    print("- Sobel и Prewitt — градиентные фильтры, полезны для поиска направлений границ.")
    print("- Laplacian — выделяет быстрые изменения интенсивности.")
    print("- Unsharp Masking — улучшает резкость за счёт вычитания размытой копии.")
    print("- Canny — мощный фильтр, надёжно выделяет границы с подавлением шумов.")
'''
        elif number == 4:
            return '''
            import cv2
import numpy as np
import matplotlib.pyplot as plt

def morphological_operations(image_path):
    # Загрузка изображения
    img = cv2.imread(image_path)
    if img is None:
        print("Ошибка загрузки изображения")
        return

    # Перевод в оттенки серого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Бинаризация изображения для морфологических операций
    # (лучше работает на чётком черно-белом)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Создание структурирующего элемента (ядра)
    # 3x3 квадрат, можно изменить на другие формы и размеры
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # === 1. Эрозия ===
    # Уменьшает яркие области, "съедает" границы
    erosion = cv2.erode(binary, kernel, iterations=1)

    # === 2. Расширение ===
    # Увеличивает яркие области, "расширяет" границы
    dilation = cv2.dilate(binary, kernel, iterations=1)

    # === 3. Открытие ===
    # Последовательность: эрозия → расширение
    # Удаляет мелкие объекты/шум, сохраняет крупные формы
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # === Отображение результатов ===
    images = {
        "Исходное (бинарное)": binary,
        "Эрозия": erosion,
        "Расширение": dilation,
        "Открытие": opening
    }

    plt.figure(figsize=(10, 10))

    for i, (title, result) in enumerate(images.items()):
        # Показываем изображение
        plt.subplot(len(images), 2, 2 * i + 1)
        plt.imshow(result, cmap='gray')
        plt.title(title)
        plt.axis('off')

        # Гистограмма
        plt.subplot(len(images), 2, 2 * i + 2)
        plt.hist(result.ravel(), bins=256, range=(0, 256), color='black')
        plt.title(f'{title} - Histogram')

    plt.tight_layout()
    plt.show()

    # === Выводы ===
    print("\nВыводы:")
    print("- Эрозия удаляет мелкие объекты и уменьшает яркие участки.")
    print("- Расширение заполняет пробелы, увеличивает яркие области.")
    print("- Открытие удаляет шум, сохраняя форму более крупных объектов.")
    print("- Подходит для предобработки перед выделением контуров или OCR.")
'''
        elif number == 5:
            return '''
            import cv2
import numpy as np
import matplotlib.pyplot as plt

def fourier_transform_analysis(image_path):
    # Загрузка изображения в градациях серого
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Ошибка загрузки изображения")
        return

    # === 1. Прямое 2D-преобразование Фурье ===
    f = np.fft.fft2(img)  # комплексное 2D FFT
    fshift = np.fft.fftshift(f)  # перенос нуля частот в центр
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)  # лог-масштаб амплитуды

    # === 2. Обратное преобразование Фурье ===
    f_ishift = np.fft.ifftshift(fshift)  # сдвиг обратно
    img_back = np.fft.ifft2(f_ishift)  # обратное FFT
    img_back = np.abs(img_back)  # берем только действительную часть

    # === Отображение результатов ===
    images = {
        "Исходное изображение": img,
        "Амплитудный спектр (лог)": magnitude_spectrum,
        "Обратное преобразование": img_back
    }

    plt.figure(figsize=(12, 8))

    for i, (title, image) in enumerate(images.items()):
        # Показываем изображение
        plt.subplot(len(images), 2, 2 * i + 1)
        plt.imshow(image, cmap='gray')
        plt.title(title)
        plt.axis('off')

        # Гистограмма яркости
        plt.subplot(len(images), 2, 2 * i + 2)
        plt.hist(image.ravel(), bins=256, range=(0, 256), color='black')
        plt.title(f"{title} - Histogram")

    plt.tight_layout()
    plt.show()

    # === Выводы ===
    print("\nВыводы:")
    print("- Преобразование Фурье переводит изображение в частотную область.")
    print("- Центр спектра — низкие частоты (фон), края — высокие (детали, шум).")
    print("- Логарифмическое усиление помогает увидеть слабые частоты.")
    print("- Обратное преобразование восстанавливает изображение с высокой точностью.")
    print("- Частотный анализ полезен для фильтрации, выделения текстур и восстановления.")
'''
        elif number == 6:
            return '''
            from ikomia.dataprocess.workflow import Workflow
import cv2
import collections
import os

def run_tracking_workflow(
    input_video_path: str,
    output_video_path: str,
    tracker_type: str = "deepsort",  # "deepsort", "sort", "ocsort"
    detection_model: str = "infer_yolo_v7",  # см. список моделей ниже
    categories_to_track: str = "person,car"
):
    """
    Запуск пайплайна отслеживания объектов с использованием Ikomia Workflow.

    Аргументы:
    ----------
    input_video_path : str
        Путь к входному видеофайлу.
    output_video_path : str
        Путь для сохранения выходного видео.
    tracker_type : str
        Тип алгоритма трекинга:
            - "deepsort" (точный, appearance-based)
            - "sort" (простой и быстрый, без appearance)
            - "ocsort" (современный, устойчивый к окклюзии)

    detection_model : str
        Название модели для детекции объектов. Поддерживаются:
            - "infer_yolo_v7"
            - "infer_yolo_v5"
            - "infer_yolo_v8"
            - "infer_yolox"
            - "infer_yolo_nas"
            - "infer_efficientdet"
            - "infer_ssd"
            - "infer_torchvision_frcnn"  (Faster R-CNN)
            - "infer_torchvision_retinanet"

        Если модель не установлена — установить через:
            from ikomia.utils import ik
            ik.install("название_модуля")

    categories_to_track : str
        Классы объектов, которые нужно отслеживать, через запятую.
        Пример: "person,car,dog"
    """

    if not os.path.exists(input_video_path):
        print(f"Файл не найден: {input_video_path}")
        return

    wf = Workflow()

    # Добавление детектора объектов
    detector = wf.add_task(name=detection_model, auto_connect=True)
    detector.set_parameters({})  # можно задать параметры при необходимости

    # Выбор трекера
    tracker_plugins = {
        "deepsort": "infer_deepsort",
        "sort": "infer_sort",
        "ocsort": "infer_ocsort"
    }

    if tracker_type.lower() not in tracker_plugins:
        print(f"Ошибка: неизвестный трекер '{tracker_type}'")
        return

    tracking = wf.add_task(name=tracker_plugins[tracker_type.lower()], auto_connect=True)

    # Общие параметры
    common_params = {
        "categories": categories_to_track,
        "iou_threshold": "0.3"
    }

    if tracker_type == "deepsort":
        common_params.update({
            "conf_thres": "0.5",
            "max_age": "50",
            "min_hits": "3",
            "cosine_threshold": "0.2",
            "nn_budget": "100",
            "use_cuda": "True"
        })

    tracking.set_parameters(common_params)

    # Работа с видео
    stream = cv2.VideoCapture(input_video_path)
    if not stream.isOpened():
        print("Ошибка: не удалось открыть видео.")
        return

    frame_width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = stream.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (frame_width, frame_height))

    frame_count = 0

    while True:
        ret, frame = stream.read()
        if not ret:
            print("Видео завершено или ошибка чтения.")
            break

        wf.run_on(array=frame)

        image_out = tracking.get_output(0)
        obj_detect_out = tracking.get_output(1)

        img_out = image_out.get_image_with_graphics(obj_detect_out)
        img_res = cv2.cvtColor(img_out, cv2.COLOR_RGB2BGR)

        # Подсчёт объектов
        class_counts = collections.defaultdict(int)
        for detection in obj_detect_out.get_objects():
            class_counts[detection.label] += 1

        # Отображение статистики на кадре
        y_offset = 30
        for class_name, count in class_counts.items():
            cv2.putText(img_res, f"{class_name}: {count}", (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            y_offset += 30

        out.write(img_res)
        frame_count += 1

    stream.release()
    out.release()
    print(f"\nОбработка завершена. Видео сохранено в: {output_video_path}")
'''
        elif number == 7:
            return '''
            import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import transforms, datasets
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
from zipfile import ZipFile

# Разархивация датасета
zip_path = "images/sign_language.zip"
data_dir = "sign_language"
if not os.path.exists(data_dir):
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("images")


# 1. Загрузка данных и предобработка
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

dataset = datasets.ImageFolder(data_dir, transform=transform)
num_classes = len(dataset.classes)

# Разделение данных на обучающее и тестовое множества
train_size = int(0.7 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64)

# 2. Сверточная нейронная сеть
class CNN(nn.Module):
    def __init__(self, num_blocks, num_classes):
        super(CNN, self).__init__()
        layers = []
        in_channels = 3

        for _ in range(num_blocks):
            layers.extend([
                nn.Conv2d(in_channels, 32, kernel_size=3, stride=1, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2, stride=2)
            ])
            in_channels = 32

        self.conv = nn.Sequential(*layers)
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * (64 // (2 ** num_blocks))**2, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

# 3. Функция обучения
def train_model(model, train_loader, num_epochs=10):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(num_epochs):
        model.train()
        for images, labels in train_loader:

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

# 4. Функция оценки
def evaluate_model(model, test_loader):
    model.eval()
    y_true, y_pred = [], []

    with torch.no_grad():
        for images, labels in test_loader:

            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            y_true.extend(labels.cpu().numpy())
            y_pred.extend(preds.cpu().numpy())

    micro_f1 = f1_score(y_true, y_pred, average='micro')
    return micro_f1

# 5. Проведение экспериментов
results = []

for num_blocks in range(1, 5):  # Перебираем количество сверточных блоков
    print(f"Training with {num_blocks} convolutional blocks...")
    model = CNN(num_blocks, num_classes)
    train_model(model, train_loader)
    micro_f1 = evaluate_model(model, test_loader)
    results.append((num_blocks, micro_f1))
    print(f"Micro F1 for {num_blocks} blocks: {micro_f1:.4f}")

# 6. Визуализация результатов
blocks, scores = zip(*results)
plt.plot(blocks, scores, marker='o', label="Micro F1 Score")
plt.title("Micro F1 vs Number of Convolutional Blocks")
plt.xlabel("Number of Convolutional Blocks")
plt.ylabel("Micro F1 Score")
plt.grid()
plt.legend()
plt.show()
'''
        elif number == 8:
            return '''
            import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split, Subset
from torchvision import transforms, datasets
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
from tqdm import tqdm
from zipfile import ZipFile

# Разархивация датасета
zip_path = "images/eng_handwritten.zip"
data_dir = "eng_handwritten"
if not os.path.exists(data_dir):
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("images")

# 1. Загрузка данных и предобработка
transform = transforms.Compose([
    transforms.CenterCrop((32, 32)),  # Обрезка центральной области
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

dataset = datasets.ImageFolder(data_dir, transform=transform)
num_classes = len(dataset.classes)

# Разделение данных: 70% - обучающая выборка, 15% - валидационная, 15% - тестовая
train_size = int(0.7 * len(dataset))
val_size = int(0.15 * len(dataset))
test_size = len(dataset) - train_size - val_size
train_dataset, val_dataset, test_dataset = random_split(dataset, [train_size, val_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=128)
test_loader = DataLoader(test_dataset, batch_size=128)

# 2. Сверточная нейронная сеть
class CNN(nn.Module):
    def __init__(self, num_classes):
        super(CNN, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * (32 // 8)**2, 128),  # 128 // 8 - уменьшение после трех MaxPool2d
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

# 3. Обучение модели с ранней остановкой
def train_model_with_early_stopping(model, train_loader, val_loader, patience=5, num_epochs=50):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    best_f1 = 0.0
    best_model_state = None
    patience_counter = 0

    for epoch in tqdm(range(num_epochs)):
        # Обучение
        model.train()
        for images, labels in train_loader:

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        # Валидация
        model.eval()
        y_true, y_pred = [], []
        with torch.no_grad():
            for images, labels in val_loader:
                outputs = model(images)
                _, preds = torch.max(outputs, 1)
                y_true.extend(labels.cpu().numpy())
                y_pred.extend(preds.cpu().numpy())

        val_f1 = f1_score(y_true, y_pred, average='micro')
        print(f"Epoch {epoch + 1}: Validation Micro F1 = {val_f1:.4f}")

        # Проверка ранней остановки
        if val_f1 > best_f1:
            best_f1 = val_f1
            best_model_state = model.state_dict()
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print("Early stopping triggered")
                break

    # Возврат лучшей модели
    model.load_state_dict(best_model_state)
    return model

# 4. Оценка модели
def evaluate_model(model, test_loader):
    model.eval()
    y_true, y_pred = [], []

    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            y_true.extend(labels.numpy())
            y_pred.extend(preds.numpy())

    micro_f1 = f1_score(y_true, y_pred, average='micro')
    return micro_f1

# 5. Запуск эксперимента
model = CNN(num_classes)
model = train_model_with_early_stopping(model, train_loader, val_loader, patience=3, num_epochs=20)
test_f1 = evaluate_model(model, test_loader)

print(f"Final Test Micro F1: {test_f1:.4f}")
'''
        elif number == 9:
            return '''
            import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import f1_score
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm
from zipfile import ZipFile

# Разархивация датасета
zip_path = "clothes_multi.zip"
data_dir = "clothes_multi"
if not os.path.exists(data_dir):
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("images")

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

dataset = datasets.ImageFolder(root=data_dir, transform=transform)

class_names = dataset.classes
color_to_idx = {}
item_to_idx = {}
colors = set()
items = set()

for class_name in class_names:
    color, item = class_name.split('_')
    colors.add(color)
    items.add(item)

color_to_idx = {color: idx for idx, color in enumerate(sorted(colors))}
item_to_idx = {item: idx for idx, item in enumerate(sorted(items))}

def get_color_and_item_labels(target):
    class_name = class_names[target]
    color, item = class_name.split('_')
    return color_to_idx[color], item_to_idx[item]

class MultiLabelDataset(torch.utils.data.Dataset):
    def __init__(self, dataset):
        self.dataset = dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        img, target = self.dataset[idx]
        color_label, item_label = get_color_and_item_labels(target)
        return img, torch.tensor([color_label, item_label])

multi_label_dataset = MultiLabelDataset(dataset)

train_size = int(0.8 * len(multi_label_dataset))
test_size = len(multi_label_dataset) - train_size
train_dataset, test_dataset = random_split(multi_label_dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)


# Модель для многозадачной классификации
class MultiTaskModel(nn.Module):
    def __init__(self, num_color_classes, num_clothing_classes):
        super(MultiTaskModel, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc_color = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 32 * 32, 128),
            nn.ReLU(),
            nn.Linear(128, num_color_classes)
        )
        self.fc_clothing = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 32 * 32, 128),
            nn.ReLU(),
            nn.Linear(128, num_clothing_classes)
        )

    def forward(self, x):
        features = self.conv(x)
        color_output = self.fc_color(features)
        clothing_output = self.fc_clothing(features)
        return color_output, clothing_output

# Функция вычисления micro F1
def calculate_micro_f1(y_true, y_pred):
    return f1_score(y_true, y_pred, average='micro')

# Логика обучения модели
def train_model(model, train_loader, num_epochs):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in tqdm(range(num_epochs)):
        model.train()
        train_loss = 0
        for imgs, labels in train_loader:
            color_labels, item_labels = labels[:, 0], labels[:, 1]

            optimizer.zero_grad()
            color_out, item_out = model(imgs)

            loss = criterion(color_out, color_labels) + criterion(item_out, item_labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {train_loss:.4f}")

# Функция тестирования
def evaluate_model(model, data_loader):
    model.eval()
    true_color, true_item = [], []
    pred_color, pred_item = [], []

    with torch.no_grad():
        for imgs, labels in data_loader:
            color_labels, item_labels = labels[:, 0], labels[:, 1]

            color_out, item_out = model(imgs)
            true_color.extend(color_labels.numpy())
            true_item.extend(item_labels.numpy())

            pred_color.extend(color_out.argmax(1).numpy())
            pred_item.extend(item_out.argmax(1).numpy())

    f1_color = calculate_micro_f1(true_color, pred_color)
    f1_item = calculate_micro_f1(true_item, pred_item)
    micro_f1 = (f1_color + f1_item) / 2
    return micro_f1

# Основной процесс
num_colors = len(color_to_idx)
num_items = len(item_to_idx)
model = MultiTaskModel(num_colors, num_items)

# Обучение модели
train_model(model, train_loader, num_epochs=10)

# Оценка модели
train_f1 = evaluate_model(model, train_loader)
test_f1 = evaluate_model(model, test_loader)

print(f"F1 на обучающем множестве: {train_f1:.4f}")
print(f"F1 на тестовом множестве: {test_f1:.4f}")
'''
        elif number == 10:
            return '''
            import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import transforms, datasets
from sklearn.metrics import f1_score
from zipfile import ZipFile

# Разархивация датасета
zip_path = "images/chars.zip"
data_dir = "chars"
if not os.path.exists(data_dir):
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("images")

# 1. Загрузка и предобработка данных
basic_transform = transforms.Compose([
    transforms.Resize((64, 64)),  # Изменяем размер изображений
    transforms.ToTensor(),  # Преобразуем в тензор
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Нормализация
])

augment_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(degrees=15),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

dataset = datasets.ImageFolder(data_dir, transform=basic_transform)
num_classes = len(dataset.classes)

# Разделение данных на обучающее (70%) и тестовое (30%) множество
train_size = int(0.7 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

# Датасет с аугментацией
augmented_train_dataset = datasets.ImageFolder(data_dir, transform=augment_transform)
augmented_train_dataset = torch.utils.data.Subset(augmented_train_dataset, train_dataset.indices)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64)
augmented_train_loader = DataLoader(augmented_train_dataset, batch_size=64, shuffle=True)

# 2. Сверточная нейронная сеть
class CNN(nn.Module):
    def __init__(self, num_classes):
        super(CNN, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * (64 // 8)**2, 128),  # Учитываем уменьшение размера после MaxPool2d
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

# 3. Функция обучения модели
def train_model(model, train_loader, num_epochs=10):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(num_epochs):
        model.train()
        for images, labels in train_loader:
            outputs = model(images)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch + 1}/{num_epochs} complete.")

    return model

# 4. Функция оценки модели
def evaluate_model(model, test_loader):
    model.eval()
    y_true, y_pred = [], []

    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            y_true.extend(labels.numpy())
            y_pred.extend(preds.numpy())

    micro_f1 = f1_score(y_true, y_pred, average='micro')
    return micro_f1

# 5. Обучение и оценка
# Базовый набор данных
model_basic = CNN(num_classes)
model_basic = train_model(model_basic, train_loader, num_epochs=10)
f1_basic = evaluate_model(model_basic, test_loader)
print(f"Micro F1 Score (basic dataset): {f1_basic:.4f}")

# Расширенный набор данных (с аугментацией)
model_augmented = CNN(num_classes)
model_augmented = train_model(model_augmented, augmented_train_loader, num_epochs=20)
f1_augmented = evaluate_model(model_augmented, test_loader)
print(f"Micro F1 Score (augmented dataset): {f1_augmented:.4f}")
'''