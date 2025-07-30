import pyperclip
import io
import tokenize
from openai import OpenAI
import re


class ClipboardHelper:
    def __init__(self):
        self.methods_info = {
            "lab1": "cv2/pillow, предобработка изображений",
            "lab2": "классификация",
            "lab4": "детекция, yolo",
            "lab5": "semantic segmentation",
            "lab6": "instance segmentation",
            "lab7": "object tracking",
        }

    def lab1(self, ind=0):
        """cv2/pillow, предобработка изображений"""
        if ind == 0:
            code = """
from PIL import Image
img_path = 'img.jpg'
img = Image.open(img_path)
# 1
img.convert('L')
# 2
import os
png_path = os.path.splitext(img_path)[0] + '.png'
# 3
img.thumbnail((150, 150))
# 4
img = Image.open(img_path)
box = (100, 150, 200, 300)
rg = img.crop(box)

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

img_2 = np.array(Image.open("img_2.png"))
fig, ax = plt.subplots()

ax.imshow(img_2)

rect = patches.Rectangle((150, 75), 100, 200, linewidth=1, edgecolor='r', facecolor='none')

ax.add_patch(rect)
plt.show()

def change_scaling(img: Image, x: int, y: int):
    changed = img.copy()

    return changed.resize((x, y))

change_scaling(img, 250, 250)

plt.gray()
plt.contour(Image.fromarray(img_2).convert("L"), origin="image")

plt.hist(img_2.flatten(), 255)
plt.show()

img_2 = np.array(Image.open("img_2.png"))
print(type(img_2))
plt.imshow(img_2)

# 2
im_s = img_2[:img_2.shape[0]//2, :]
im_s

img_2[img_2.shape[0]//2+1:, :] = im_s
plt.imshow(img_2)

# 3
img_2_inv = 255 - img_2
plt.imshow(img_2_inv)

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

im_interv = (150.0/255) * img_2 + 100 # [150,250]
im_interv

int_img = Image.fromarray(np.uint8(im_interv))
int_img

kv_img = Image.fromarray(np.uint8(im_kv))
kv_img

img_3 = np.array(Image.open("img.jpg").convert("L"))
img_3

im1, bin_edges = np.histogram(img_3, bins=256)
plt.plot(im1)

def image_histogram_equalization(im, number_bins=256):
  imhist, bins = np.histogram(im.flatten(), number_bins, density=True)
  cdf = imhist.cumsum()
  cdf = 255*cdf/cdf[-1]

  image_equalized = np.interp(im.flatten(), bins[:-1], cdf)
  return image_equalized.reshape(im.shape), cdf

img_3_corr, cdf = image_histogram_equalization(img_3)
img_3_corr

img_3_b, bin_edges = np.histogram(img_3_corr, bins=256)
plt.plot(img_3_b)

from scipy import ndimage

img_4 = np.array(Image.open('img_2.png').convert('L'))
img_4_filtered = ndimage.gaussian_filter(img_4 , 5)
img_4_filtered

Image.fromarray(np.uint8(img_4_filtered))

img_5 = np.array(Image.open('img.jpg'))
img_5_filtered = ndimage.gaussian_filter(img_5 , 2)
Image.fromarray(np.uint8(img_5_filtered))

import cv2
import matplotlib.pyplot as plt

image_path = 'img.jpg'
image = cv2.imread(image_path)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray_image, threshold1=100, threshold2=200)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title('Edges')
plt.imshow(edges, cmap='gray')
plt.axis('off')

plt.show()


import IPython.display as display
import time

video_path = 'example.gif'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Ошибка: не удалось открыть видео.")
    
else:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray_frame, threshold1=100, threshold2=200)

        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.title('Original Frame')
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.title('Edges')
        plt.imshow(edges, cmap='gray')
        plt.axis('off')

        plt.show()
        display.clear_output(wait=True)
        time.sleep(0.03)

    cap.release()

    
image_path = 'img.jpg'
image = cv2.imread(image_path)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray_image, threshold1=100, threshold2=200)

edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

enhanced_edges = cv2.addWeighted(image, 0.7, edges_colored, 0.3, 0)

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.title('Original Image')
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title('Edges')
plt.imshow(edges, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title('Enhanced Edges')
plt.imshow(cv2.cvtColor(enhanced_edges, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.show()


import cv2
import numpy as np
import matplotlib.pyplot as plt
import IPython.display as display
import time

video_path = 'example.gif'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Ошибка: не удалось открыть видео.")
else:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray_frame, threshold1=100, threshold2=200)

        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        enhanced_edges = cv2.addWeighted(frame, 0.7, edges_colored, 0.3, 0)

        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.title('Original Frame')
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.title('Enhanced Edges')
        plt.imshow(cv2.cvtColor(enhanced_edges, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.show()
        display.clear_output(wait=True)
        time.sleep(0.03)

    cap.release()

    
image_path = 'img_3.jpg'
image = cv2.imread(image_path)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


hist, bins = np.histogram(gray_image.flatten(), bins=16, range=[0, 256])

plt.figure(figsize=(10, 5))
plt.title('Histplot')
plt.xlabel('Intensity')
plt.ylabel('Freq')
plt.xlim([0, 256])
plt.bar(bins[:-1], hist, width=16, edgecolor='black', align='edge')
plt.xticks(bins)
plt.show()


import cv2
import numpy as np
import matplotlib.pyplot as plt
import IPython.display as display
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("не удалось открыть веб-камеру.")
else:
    processed_frames = []
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
            edges = cv2.Canny(blurred_frame, threshold1=100, threshold2=200)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contour_frame = frame.copy()
            cv2.drawContours(contour_frame, contours, -1, (0, 255, 0), 2)

            processed_frames.append(contour_frame)

            plt.imshow(cv2.cvtColor(contour_frame, cv2.COLOR_BGR2RGB))
            plt.axis('off')
            plt.show()

            display.clear_output(wait=True)
            time.sleep(0.03)

    except KeyboardInterrupt:
        print("Завершение работы.")

cap.release()

plt.figure(figsize=(15, 10))
for i, frame in enumerate(processed_frames):
    plt.subplot(len(processed_frames) // 5 + 1, 5, i + 1)
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.axis('off')
plt.show()

from sklearn.cluster import KMeans

image_path = 'img_3.jpg'
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

image_small = cv2.resize(image, (100, 100), interpolation=cv2.INTER_AREA)
pixels = image_small.reshape(-1, 3)

num_clusters = [3, 5, 7, 9]
clustered_images = []

for n in num_clusters:
    kmeans = KMeans(n_clusters=n, random_state=42)
    kmeans.fit(pixels)
    
    new_colors = kmeans.cluster_centers_[kmeans.labels_]
    clustered_image = new_colors.reshape(image_small.shape).astype(int)
    
    clustered_images.append(clustered_image)

plt.figure(figsize=(15, 10))

for i, (n, clustered_image) in enumerate(zip(num_clusters, clustered_images)):
    plt.subplot(2, 2, i + 1)
    plt.imshow(clustered_image)
    plt.title(f'K-Means Clustering with {n} Clusters')
    plt.axis('off')

plt.tight_layout()
plt.show()

image_path = 'img_4.png'
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

denoised_image = cv2.medianBlur(image, ksize=5)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title('Original')
plt.imshow(image)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title('Denoised')
plt.imshow(denoised_image)
plt.axis('off')

plt.show()
            """
        pyperclip.copy(code)

    def lab2_1(self, ind=0):
        """классификация"""
        if ind == 0:
            code = """
from google.colab import drive
drive.mount('/content/drive')

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

path = '/content/drive/MyDrive/cv_lab2/'

train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.465, 0.406], std=[0.229, 0.224, 0.225])
])
test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.465, 0.406], std=[0.229, 0.224, 0.225])
])

dataset = datasets.ImageFolder(root=path, transform=train_transform)
dataset.classes

total_size = len(dataset)
train_size = int(0.7*total_size)
val_size = int(0.15*total_size)
test_size = total_size - train_size - val_size

train_dataset, val_dataset, test_dataset = random_split(dataset, [train_size, val_size, test_size])
val_dataset.dataset.transform = test_transform
test_dataset.dataset.transform = test_transform

class_names = {
    0: 'Apple___Black_rot',
    1: 'Apple___healthy'
}

import matplotlib.pyplot as plt

img, label = next(iter(test_dataset))

plt.imshow(img[0, :, :], cmap="gray")
plt.title(class_names[label])
plt.axis("off")
plt.show()

batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

len(train_dataset), len(val_dataset), len(test_dataset)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device

class CNN_bin(nn.Module):
    def __init__(self):
        super(CNN_bin, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)

        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)
        self.bn3 = nn.BatchNorm2d(128)

        self.pool = nn.MaxPool2d(2, 2)

        self.dropout1 = nn.Dropout2d(0.25)
        self.dropout2 = nn.Dropout2d(0.5)

        dummy_input = torch.zeros(1, 3, 128, 128)
        dummy_output = self._forward_features(dummy_input)
        self.fc_input_size = dummy_output.view(1, -1).size(1)

        self.fc1 = nn.Linear(self.fc_input_size, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 1)

    def _forward_features(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.dropout1(x)
        x = self.pool(F.relu(self.bn3(self.conv3(x))))

        return x

    def forward(self, x):
        x = self._forward_features(x)

        x = torch.flatten(x, 1)

        x = F.relu(self.fc1(x))
        x = self.dropout2(x)
        x = F.relu(self.fc2(x))
        x = self.fc3(x)

        return x

cnn_bin = CNN_bin().to(device)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(cnn_bin.parameters(), lr=0.001, weight_decay=1e-5)
cnn_bin

import numpy as np
from sklearn.metrics import roc_curve, auc

def train_m(model, criterion, optimizer, num_epochs=10):
    train_losses = []
    val_losses = []
    train_accs = []
    val_accs = []

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device).float().unsqueeze(1)

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            predicted = (outputs > 0).float()
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        epoch_loss = running_loss / len(train_dataset)
        epoch_acc = correct / total
        train_losses.append(epoch_loss)
        train_accs.append(epoch_acc)

        model.eval()
        running_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device).float().unsqueeze(1)

                outputs = model(inputs)
                loss = criterion(outputs, labels)

                running_loss += loss.item() * inputs.size(0)
                predicted = (outputs > 0).float()
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        val_loss = running_loss / len(val_dataset)
        val_acc = correct / total
        val_losses.append(val_loss)
        val_accs.append(val_acc)

        print(f'Epoch {epoch+1}/{num_epochs}:')
        print(f'Train Loss: {epoch_loss:.4f}, Train Acc: {epoch_acc:.4f}')
        print(f'Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}')

    return model, train_losses, val_losses, train_accs, val_accs

def evaluate_m(model, data_loader):
    model.eval()
    all_preds = []
    all_labels = []
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in data_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            predicted = (outputs > 0).float().squeeze()

            all_preds.extend(outputs.squeeze().cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

            total += labels.size(0)
            correct += (predicted == labels.float()).sum().item()

    accuracy = correct / total

    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)

    fpr, tpr, _ = roc_curve(all_labels, all_preds)
    roc_auc = auc(fpr, tpr)

    return accuracy, all_preds, all_labels, fpr, tpr, roc_auc

model_bin, train_losses, val_losses, train_accs, val_accs = train_m(
    cnn_bin, criterion, optimizer
)

test_accuracy, all_preds, all_labels, fpr, tpr, roc_auc = evaluate_m(model_bin, test_loader)
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"AUC: {roc_auc:.4f}")

plt.plot(range(1, len(train_losses)+1), train_losses, 'b-', label='Training Loss')
plt.plot(range(1, len(val_losses)+1), val_losses, 'r-', label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()

plt.plot(range(1, len(train_accs)+1), train_accs, 'b-', label='Training Accuracy')
plt.plot(range(1, len(val_accs)+1), val_accs, 'r-', label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()
"""
        elif ind == 1:
            code = """
from google.colab import drive
drive.mount('/content/drive')

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import ReduceLROnPlateau

path = '/content/drive/MyDrive/datasets-2/'

# Улучшенные трансформации с аугментацией для обучающей выборки
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.465, 0.406], std=[0.229, 0.224, 0.225])
])

# Трансформации для тестовой и валидационной выборок (без аугментации)
test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.465, 0.406], std=[0.229, 0.224, 0.225])
])

# Загрузка датасета
dataset = datasets.ImageFolder(root=path, transform=train_transform)
num_classes = len(dataset.classes)
class_names = dataset.classes
print(f"Количество классов: {num_classes}")
print(f"Названия классов: {class_names}")

# Разделение датасета на обучающую, валидационную и тестовую выборки
total_size = len(dataset)
train_size = int(0.7 * total_size)
val_size = int(0.15 * total_size)
test_size = total_size - train_size - val_size

train_dataset, val_dataset, test_dataset = random_split(dataset, [train_size, val_size, test_size])
val_dataset.dataset.transform = test_transform
test_dataset.dataset.transform = test_transform

# Создание загрузчиков данных
batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

print(f"Размер обучающей выборки: {len(train_dataset)}, Размер валидационной выборки: {len(val_dataset)}, Размер тестовой выборки: {len(test_dataset)}")

# Отображение примера изображений
import matplotlib.pyplot as plt

# Получаем батч данных
dataiter = iter(train_loader)
images, labels = next(dataiter)

# Создаем сетку с примерами изображений
fig, axes = plt.subplots(2, 4, figsize=(12, 6))
axes = axes.flatten()

for i in range(min(8, len(images))):
    img = images[i].permute(1, 2, 0).numpy()
    img = img * np.array([0.229, 0.224, 0.225]) + np.array([0.485, 0.465, 0.406])
    img = np.clip(img, 0, 1)

    axes[i].imshow(img)
    axes[i].set_title(f"Класс: {class_names[labels[i]]}")
    axes[i].axis("off")

plt.tight_layout()
plt.show()

# Определение устройства для вычислений
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Используемое устройство: {device}")

# Определение CNN модели для многоклассовой классификации
class CNN_multiclass(nn.Module):
    def __init__(self, num_classes):
        super(CNN_multiclass, self).__init__()
        # Сверточные слои
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)

        # Батч-нормализация
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)
        self.bn3 = nn.BatchNorm2d(128)
        self.bn4 = nn.BatchNorm2d(256)

        # Пулинг
        self.pool = nn.MaxPool2d(2, 2)

        # Дропаут для регуляризации
        self.dropout1 = nn.Dropout2d(0.25)
        self.dropout2 = nn.Dropout2d(0.5)

        # Динамический расчет размера входа для полносвязных слоев
        dummy_input = torch.zeros(1, 3, 224, 224)
        dummy_output = self._forward_features(dummy_input)
        self.fc_input_size = dummy_output.view(1, -1).size(1)

        # Полносвязные слои
        self.fc1 = nn.Linear(self.fc_input_size, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, num_classes)  # Выходной слой с num_classes нейронами

    def _forward_features(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.dropout1(x)
        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        x = self.pool(F.relu(self.bn4(self.conv4(x))))

        return x

    def forward(self, x):
        x = self._forward_features(x)
        x = torch.flatten(x, 1)

        x = F.relu(self.fc1(x))
        x = self.dropout2(x)
        x = F.relu(self.fc2(x))
        x = self.fc3(x)

        return x

# Инициализация модели, функции потерь, оптимизатора и планировщика скорости обучения
model = CNN_multiclass(num_classes).to(device)
criterion = nn.CrossEntropyLoss()  # Функция потерь для многоклассовой классификации
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=3, verbose=True)

print(model)

# Функция обучения с ранней остановкой
def train_multiclass(model, criterion, optimizer, scheduler, num_epochs=25, patience=5):
    train_losses = []
    val_losses = []
    train_accs = []
    val_accs = []

    best_val_loss = float('inf')
    epochs_no_improve = 0

    for epoch in range(num_epochs):
        # Фаза обучения
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        epoch_loss = running_loss / len(train_dataset)
        epoch_acc = correct / total
        train_losses.append(epoch_loss)
        train_accs.append(epoch_acc)

        # Фаза валидации
        model.eval()
        running_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)

                outputs = model(inputs)
                loss = criterion(outputs, labels)

                running_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        val_loss = running_loss / len(val_dataset)
        val_acc = correct / total
        val_losses.append(val_loss)
        val_accs.append(val_acc)

        # Вывод результатов эпохи
        print(f'Эпоха {epoch+1}/{num_epochs}:')
        print(f'Потери при обучении: {epoch_loss:.4f}, Точность при обучении: {epoch_acc:.4f}')
        print(f'Потери при валидации: {val_loss:.4f}, Точность при валидации: {val_acc:.4f}')

        # Планирование скорости обучения
        scheduler.step(val_loss)

        # Ранняя остановка
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            epochs_no_improve = 0
            # Сохранение лучшей модели
            torch.save(model.state_dict(), 'best_model.pth')
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= patience:
                print(f'Ранняя остановка после {epoch+1} эпох')
                break

    # Загрузка лучшей модели
    model.load_state_dict(torch.load('best_model.pth'))

    return model, train_losses, val_losses, train_accs, val_accs

# Функция оценки
def evaluate_multiclass(model, data_loader):
    model.eval()
    all_preds = []
    all_labels = []
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in data_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)

            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = correct / total

    return accuracy, np.array(all_preds), np.array(all_labels)

# Обучение модели
model, train_losses, val_losses, train_accs, val_accs = train_multiclass(
    model, criterion, optimizer, scheduler, num_epochs=25
)

# Оценка на тестовой выборке
test_accuracy, test_preds, test_labels = evaluate_multiclass(model, test_loader)
print(f"Точность на тестовой выборке: {test_accuracy:.4f}")

# Вывод отчета о классификации
print("\nОтчет о классификации:")
print(classification_report(test_labels, test_preds, target_names=class_names))

# Построение матрицы ошибок
cm = confusion_matrix(test_labels, test_preds)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Предсказанный класс')
plt.ylabel('Истинный класс')
plt.title('Матрица ошибок')
plt.show()

# Построение кривых обучения
plt.figure(figsize=(12, 5))

# Построение потерь при обучении и валидации
plt.subplot(1, 2, 1)
plt.plot(range(1, len(train_losses)+1), train_losses, 'b-', label='Потери при обучении')
plt.plot(range(1, len(val_losses)+1), val_losses, 'r-', label='Потери при валидации')
plt.xlabel('Эпохи')
plt.ylabel('Потери')
plt.title('Кривые потерь при обучении и валидации')
plt.legend()

# Построение точности при обучении и валидации
plt.subplot(1, 2, 2)
plt.plot(range(1, len(train_accs)+1), train_accs, 'b-', label='Точность при обучении')
plt.plot(range(1, len(val_accs)+1), val_accs, 'r-', label='Точность при валидации')
plt.xlabel('Эпохи')
plt.ylabel('Точность')
plt.title('Кривые точности при обучении и валидации')
plt.legend()

plt.tight_layout()
plt.show()
"""
        elif ind == 3:
            code = """
# Модель CNN с настраиваемым количеством слоев
class FlexibleCNN(nn.Module):
    def __init__(self, num_classes, num_layers=3):
        super(FlexibleCNN, self).__init__()

        self.num_layers = num_layers
        self.features = nn.Sequential()

        # Создание сверточных слоев
        in_channels = 3
        channels = [32, 64, 128, 256, 512]

        for i in range(num_layers):
            out_channels = channels[i]

            # Добавляем сверточный блок
            self.features.add_module(f'conv{i+1}', nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1))
            self.features.add_module(f'bn{i+1}', nn.BatchNorm2d(out_channels))
            self.features.add_module(f'relu{i+1}', nn.ReLU(inplace=True))
            self.features.add_module(f'pool{i+1}', nn.MaxPool2d(2, 2))

            # Добавляем дропаут после первого слоя
            if i >= 1:
                self.features.add_module(f'dropout{i+1}', nn.Dropout2d(0.25))

            in_channels = out_channels

        # Расчет размера входа для полносвязного слоя
        dummy_input = torch.zeros(1, 3, 224, 224)
        dummy_output = self.features(dummy_input)
        self.fc_input_size = dummy_output.view(1, -1).size(1)

        # Полносвязные слои
        self.classifier = nn.Sequential(
            nn.Linear(self.fc_input_size, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

# Функция обучения модели (упрощенная)
def train_model(model, criterion, optimizer, num_epochs=10):
    train_losses = []
    val_losses = []
    train_accs = []
    val_accs = []

    for epoch in range(num_epochs):
        # Фаза обучения
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        epoch_loss = running_loss / len(train_dataset)
        epoch_acc = correct / total
        train_losses.append(epoch_loss)
        train_accs.append(epoch_acc)

        # Фаза валидации
        model.eval()
        running_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)

                running_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        val_loss = running_loss / len(val_dataset)
        val_acc = correct / total
        val_losses.append(val_loss)
        val_accs.append(val_acc)

        print(f'Эпоха {epoch+1}/{num_epochs}:')
        print(f'Обучение - потери: {epoch_loss:.4f}, точность: {epoch_acc:.4f}')
        print(f'Валидация - потери: {val_loss:.4f}, точность: {val_acc:.4f}')

    return model, train_losses, val_losses, train_accs, val_accs

# Оценка модели на тестовом наборе
def evaluate_model(model, test_loader):
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = correct / total
    return accuracy

# Эксперимент с разным количеством слоев
def run_experiment(num_classes, max_layers=5, epochs=10):
    results = {
        'num_layers': [],
        'train_losses': [],
        'val_losses': [],
        'train_accs': [],
        'val_accs': [],
        'test_acc': [],
        'params': []
    }

    for num_layers in range(1, max_layers + 1):
        print(f"\n===== Модель с {num_layers} слоями =====\n")

        # Создание модели
        model = FlexibleCNN(num_classes, num_layers=num_layers).to(device)

        # Подсчет параметров
        total_params = sum(p.numel() for p in model.parameters())
        print(f"Параметров: {total_params:,}")

        # Обучение
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)

        model, train_losses, val_losses, train_accs, val_accs = train_model(
            model, criterion, optimizer, num_epochs=epochs
        )

        # Тестирование
        test_accuracy = evaluate_model(model, test_loader)
        print(f"Точность на тесте: {test_accuracy:.4f}")

        # Сохранение результатов
        results['num_layers'].append(num_layers)
        results['train_losses'].append(train_losses)
        results['val_losses'].append(val_losses)
        results['train_accs'].append(train_accs)
        results['val_accs'].append(val_accs)
        results['test_acc'].append(test_accuracy)
        results['params'].append(total_params)

    return results

# Визуализация результатов
def plot_results(results):
    # 1. График зависимости точности от количества слоев
    plt.figure(figsize=(10, 6))
    plt.plot(results['num_layers'], [accs[-1] for accs in results['train_accs']], 'b-o', label='Обучение')
    plt.plot(results['num_layers'], [accs[-1] for accs in results['val_accs']], 'r-o', label='Валидация')
    plt.plot(results['num_layers'], results['test_acc'], 'g-o', label='Тест')
    plt.xlabel('Количество слоев')
    plt.ylabel('Точность')
    plt.title('Зависимость точности от количества слоев')
    plt.xticks(results['num_layers'])
    plt.legend()
    plt.grid(True)
    plt.show()

    # 2. Кривые обучения для каждой модели
    plt.figure(figsize=(15, 10))
    for i, num_layers in enumerate(results['num_layers']):
        plt.subplot(len(results['num_layers']), 2, i*2 + 1)
        plt.plot(results['train_losses'][i], 'b-', label='Обучение')
        plt.plot(results['val_losses'][i], 'r-', label='Валидация')
        plt.title(f'Потери ({num_layers} слоев)')
        plt.legend()

        plt.subplot(len(results['num_layers']), 2, i*2 + 2)
        plt.plot(results['train_accs'][i], 'b-', label='Обучение')
        plt.plot(results['val_accs'][i], 'r-', label='Валидация')
        plt.title(f'Точность ({num_layers} слоев)')
        plt.legend()

    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.bar(results['num_layers'], results['params'])
    plt.xlabel('Количество слоев')
    plt.ylabel('Количество параметров')
    plt.title('Сложность модели')
    plt.xticks(results['num_layers'])
    plt.grid(True, axis='y')
    plt.show()

results = run_experiment(num_classes, max_layers=5, epochs=8)

plot_results(results)

best_idx = results['test_acc'].index(max(results['test_acc']))
best_layers = results['num_layers'][best_idx]
print(f"\nЛучшая модель: {best_layers} слоев, точность на тесте: {results['test_acc'][best_idx]:.4f}")

for i, layers in enumerate(results['num_layers']):
    train_acc = results['train_accs'][i][-1]
    val_acc = results['val_accs'][i][-1]
    gap = train_acc - val_acc

    print(f"Модель с {layers} слоями:")
    print(f"  - Точность обучения: {train_acc:.4f}")
    print(f"  - Точность валидации: {val_acc:.4f}")
    print(f"  - Разрыв (переобучение): {gap:.4f}")
    print(f"  - Параметров: {results['params'][i]:,}")
    print()
"""
        elif ind == 4:
            code = """
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from torch.utils.tensorboard import SummaryWriter
import time
import os
from datetime import datetime

# Устанавливаем путь для логов TensorBoard
log_dir = os.path.join('runs', datetime.now().strftime("%Y%m%d-%H%M%S"))
os.makedirs(log_dir, exist_ok=True)

# Функция для создания модели на основе VGG16 с разным количеством новых слоев
def create_transfer_model(num_classes, num_new_layers=1):
    # Загружаем предобученную VGG16
    model = models.vgg16(pretrained=True)

    # Замораживаем веса предобученной модели
    for param in model.parameters():
        param.requires_grad = False

    # Получаем количество входов для последнего полносвязного слоя
    num_features = model.classifier[6].in_features

    # Создаем новый классификатор с заданным количеством слоев
    layers = []

    if num_new_layers == 1:
        # Только один выходной слой
        layers = [
            nn.Linear(num_features, num_classes)
        ]
    elif num_new_layers == 2:
        # Один скрытый + выходной слой
        layers = [
            nn.Linear(num_features, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        ]
    elif num_new_layers == 3:
        # Два скрытых + выходной слой
        layers = [
            nn.Linear(num_features, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(1024, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        ]
    elif num_new_layers == 4:
        # Три скрытых + выходной слой
        layers = [
            nn.Linear(num_features, 2048),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(2048, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(1024, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        ]
    else:
        raise ValueError("Поддерживается от 1 до 4 слоев")

    # Заменяем классификатор в модели
    model.classifier[6] = nn.Sequential(*layers)

    return model

# Функция для обучения модели с логированием в TensorBoard
def train_transfer_model(model, criterion, optimizer, num_epochs=10, new_layers=1):
    # Создаем писателя для TensorBoard
    writer = SummaryWriter(log_dir=os.path.join(log_dir, f'layers_{new_layers}'))

    start_time = time.time()

    for epoch in range(num_epochs):
        # Фаза обучения
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        train_loss = running_loss / len(train_dataset)
        train_acc = correct / total

        # Фаза валидации
        model.eval()
        running_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)

                running_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        val_loss = running_loss / len(val_dataset)
        val_acc = correct / total

        # Логирование в TensorBoard
        writer.add_scalar('Loss/train', train_loss, epoch)
        writer.add_scalar('Loss/validation', val_loss, epoch)
        writer.add_scalar('Accuracy/train', train_acc, epoch)
        writer.add_scalar('Accuracy/validation', val_acc, epoch)

        # Вывод информации
        print(f'Эпоха {epoch+1}/{num_epochs}:')
        print(f'Обучение - потери: {train_loss:.4f}, точность: {train_acc:.4f}')
        print(f'Валидация - потери: {val_loss:.4f}, точность: {val_acc:.4f}')

    total_time = time.time() - start_time
    print(f'Обучение завершено за {total_time:.2f} секунд')

    # Закрытие писателя
    writer.close()

    return model, val_acc

# Функция для оценки модели на тестовом наборе
def evaluate_transfer_model(model, test_loader):
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = correct / total
    return accuracy

# Проведение эксперимента с разным количеством слоев
def run_transfer_experiment(num_classes, max_layers=4, epochs=10):
    results = {
        'num_layers': [],
        'val_acc': [],
        'test_acc': [],
        'train_time': []
    }

    for num_layers in range(1, max_layers + 1):
        print(f"\n===== Модель с {num_layers} новыми слоями =====\n")

        # Создание модели
        model = create_transfer_model(num_classes, num_layers).to(device)

        # Определение оптимизатора и функции потерь
        # Обучаем только добавленные слои, так как остальные заморожены
        optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=0.001)
        criterion = nn.CrossEntropyLoss()

        # Обучение модели
        start_time = time.time()
        model, val_acc = train_transfer_model(
            model, criterion, optimizer, num_epochs=epochs, new_layers=num_layers
        )
        train_time = time.time() - start_time

        # Оценка на тестовом наборе
        test_acc = evaluate_transfer_model(model, test_loader)
        print(f"Точность на тестовом наборе: {test_acc:.4f}")

        # Сохранение результатов
        results['num_layers'].append(num_layers)
        results['val_acc'].append(val_acc)
        results['test_acc'].append(test_acc)
        results['train_time'].append(train_time)

        # Сохранение модели
        torch.save(model.state_dict(), f'vgg16_transfer_layers_{num_layers}.pth')

    return results

# Визуализация результатов
def plot_transfer_results(results):
    plt.figure(figsize=(10, 6))
    plt.plot(results['num_layers'], results['val_acc'], 'b-o', label='Валидация')
    plt.plot(results['num_layers'], results['test_acc'], 'r-o', label='Тест')
    plt.xlabel('Количество добавленных слоев')
    plt.ylabel('Точность')
    plt.title('Зависимость точности от количества добавленных слоев')
    plt.xticks(results['num_layers'])
    plt.legend()
    plt.grid(True)
    plt.show()

    # График времени обучения
    plt.figure(figsize=(10, 6))
    plt.bar(results['num_layers'], results['train_time'])
    plt.xlabel('Количество добавленных слоев')
    plt.ylabel('Время обучения (с)')
    plt.title('Зависимость времени обучения от количества добавленных слоев')
    plt.xticks(results['num_layers'])
    plt.grid(True, axis='y')
    plt.show()

# Запуск эксперимента (можно уменьшить количество эпох для скорости)
print("Запуск эксперимента с трансферным обучением...")
results = run_transfer_experiment(num_classes, max_layers=4, epochs=5)

# Построение графиков
plot_transfer_results(results)

# Анализ результатов
best_idx = results['test_acc'].index(max(results['test_acc']))
best_layers = results['num_layers'][best_idx]
print(f"\nЛучший результат: {best_layers} слоев, точность: {results['test_acc'][best_idx]:.4f}")

# Инструкции по запуску TensorBoard
print("\nЧтобы просмотреть графики в TensorBoard, выполните:")
print(f"tensorboard --logdir={log_dir}")
print("Затем откройте http://localhost:6006 в браузере")
"""
        pyperclip.copy(code.strip())

    def lab4(self, ind=0):
        """детекция yolo"""
        if ind == 0:
            code = """
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

model = YOLO("yolov8s.pt")

results = model.train(
    data=f"/content/drive/MyDrive/wind_turbines/data.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
    name="yolov8_bottle_cup"
)

model.export()

from ultralytics import YOLO

model = YOLO("/content/drive/MyDrive/yolov8_bottle_cup/weights/best.pt")

import cv2
import matplotlib.pyplot as plt

test_image_path = '/content/drive/MyDrive/wind_turbine_example.webp'
img = cv2.imread(test_image_path)
if img is None:
    raise FileNotFoundError(f"Изображение не найдено: {test_image_path}")

results_infer = model(img)

annotated_img = results_infer[0].plot()
annotated_img_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(10, 10))
plt.imshow(annotated_img_rgb)
plt.axis('off')
plt.title("Результат обнаружения Wind turbine")
plt.show()

cv2.imwrite('annotated_result.jpg', annotated_img)

from ultralytics import YOLO

model = YOLO('/content/drive/MyDrive/yolov8_bottle_cup/weights/best.pt')

results = model.predict(source='/content/drive/MyDrive/wind_turbine_video.mp4', save=True, show=True)
results
"""
        pyperclip.copy(code.strip())

    def lab5(self, ind=0):
        """semantic segmentation"""
        if ind == 0:
            code = """
import torch
import torch.nn as nn
import torchvision.transforms as T
import cv2
import numpy as np
from ultralytics import YOLO
import segmentation_models_pytorch as smp
from pathlib import Path
import matplotlib.pyplot as plt

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_video(path):
    cap = cv2.VideoCapture(path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    cap.release()
    return frames

class UNet(nn.Module):
    def __init__(self, n_channels=3, n_classes=2):
        super().__init__()
        self.encoder = smp.Unet('resnet50', encoder_weights='imagenet',
                                in_channels=n_channels, classes=n_classes)

    def forward(self, x):
        return torch.sigmoid(self.encoder(x))

model_unet = UNet().to(device)
model_unet.eval()

model_unet = UNet().to(device)
transform = T.Compose([
    T.ToPILImage(),
    T.Resize((256, 256)),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def segment_unet(frame):
    h, w = frame.shape[:2]
    img = transform(frame).unsqueeze(0).to(device)
    with torch.no_grad():
        mask = model_unet(img)
        if mask.shape[1] == 2:
            mask = mask[:, 1:2]
        mask = (mask.squeeze().cpu().numpy() * 255).astype(np.uint8)
    return cv2.resize(mask, (w, h))

frames = load_video("/content/drive/MyDrive/lab5/my_video_lab5_v2.mp4")
print(f"Загружено {len(frames)} кадров")

unet_results = []
for i, frame in enumerate(frames[:10]):
    mask = segment_unet(frame)
    result = np.hstack([frame, cv2.applyColorMap(mask, cv2.COLORMAP_JET)])
    unet_results.append(result)

plt.figure(figsize=(15, 5))
for i in range(min(3, len(unet_results))):
    plt.subplot(1, 3, i+1)
    plt.imshow(unet_results[i])
    plt.axis('off')
    plt.title(f'U-Net Frame {i+1}')
plt.tight_layout()
plt.show()
        """
        elif ind == 1:
            code = """
model_yolo = YOLO('yolov8n-seg.pt')

def segment_yolo(frame):
    results = model_yolo(frame, verbose=False)
    if results[0].masks is not None:
        masks = results[0].masks.data.cpu().numpy()
        combined_mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
        for mask in masks:
            resized_mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
            combined_mask = np.maximum(combined_mask, (resized_mask * 255).astype(np.uint8))
        return combined_mask
    return np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)

yolo_results = []
for i, frame in enumerate(frames[:10]):
    mask = segment_yolo(frame)
    colored_mask = cv2.applyColorMap(mask, cv2.COLORMAP_VIRIDIS)
    result = np.hstack([frame, colored_mask])
    yolo_results.append(result)

plt.figure(figsize=(15, 5))
for i in range(min(3, len(yolo_results))):
    plt.subplot(1, 3, i+1)
    plt.imshow(yolo_results[i])
    plt.axis('off')
    plt.title(f'YOLO Frame {i+1}')
plt.tight_layout()
plt.show()

def compare_methods(frame_idx=0):
    frame = frames[frame_idx]
    unet_mask = segment_unet(frame)
    yolo_mask = segment_yolo(frame)

    plt.figure(figsize=(20, 5))
    plt.subplot(1, 4, 1)
    plt.imshow(frame)
    plt.title('Original')
    plt.axis('off')

    plt.subplot(1, 4, 2)
    plt.imshow(cv2.applyColorMap(unet_mask, cv2.COLORMAP_JET))
    plt.title('U-Net')
    plt.axis('off')

    plt.subplot(1, 4, 3)
    plt.imshow(cv2.applyColorMap(yolo_mask, cv2.COLORMAP_VIRIDIS))
    plt.title('YOLO')
    plt.axis('off')

    plt.subplot(1, 4, 4)
    overlay = frame.copy()
    overlay[unet_mask > 50] = [255, 0, 0]
    overlay[yolo_mask > 50] = [0, 255, 0]
    plt.imshow(overlay)
    plt.title('Overlay (Red=U-Net, Green=YOLO)')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

compare_methods(0)
"""
        pyperclip.copy(code.strip())

    def lab6(self, ind=0):
        """instance segmentation"""
        if ind == 0:
            code = """"""
        pyperclip.copy(code.strip())

    def lab7(self, ind=0):
        """object tracking"""
        if ind == 0:
            code = """
import numpy as np
import cv2
import torch
import torchvision
from filterpy.kalman import KalmanFilter
from collections import defaultdict
from scipy.optimize import linear_sum_assignment

class KalmanBoxTracker(object):
    count = 0

    def __init__(self, bbox, class_id):
        # Определяем модель фильтра Калмана с 7 параметрами состояния и 4 параметрами измерения
        # dim_x=7 имеется в виду [x, y, w, h] — координаты центра bbox (x,y), ширину (w) и высоту (h) и
        # [vx, vy, vw, vh] — скорости изменения этих параметров (но в коде используется только vx, vy, см. матрицу F).
        # для полного описания надо бы 8 параметров, но в SORT 6 параметров + 7-й параметр  vh и vw объединены в один параметр
        # (предполагается, что они равны или слабо влияют на трекинг).
        # На практике vh часто игнорируется, и остаётся vw (отсюда dim_x=7)
        # 6 бы тоже работало, но в SORT принято 7

        # dim_z=4 В фильтре Калмана для трекинга объектов dim_z=4 означает,
        # что вектор измерений (т.е. данные, которые поступают от детектора) состоит из 4 параметров [x, y, w, h]
        # Вектор состояния x имеет размерность 7 ([x, y, w, h, vx, vy, vw]),
        # но измерения (z) включают только наблюдаемые параметры — координаты и размеры (x, y, w, h).
        # Скорости (vx, vy, vw) нельзя измерить напрямую — они вычисляются фильтром Калмана на
        # основе изменений координат и размеров между кадрами.

        self.kf = KalmanFilter(dim_x=7, dim_z=4)

        # Матрица перехода состояния (предполагаем постоянную скорость)
        # Матрица F описывает, как состояние объекта изменяется от кадра к кадру. Для модели с dim_x=7 имеем:
        self.kf.F = np.array([
          [1,0,0,0,1,0,0],  # x_new = x_prev + vx*dt  В SORT обычно предполагается dt = 1
          [0,1,0,0,0,1,0],  # y_new = y_prev + vy*dt
          [0,0,1,0,0,0,1],  # w_new = w_prev + vw*dt
          [0,0,0,1,0,0,0],  # h_new = h_prev (vh игнорируется)
          [0,0,0,0,1,0,0],  # vx_new = vx_prev
          [0,0,0,0,0,1,0],  # vy_new = vy_prev
          [0,0,0,0,0,0,1]   # vw_new = vw_prev
        ])
        # Строки 1-4: Обновление координат и размеров:
        # x и y меняются на vx и vy (предполагается движение с постоянной скоростью).
        # w меняется на vw, а h остаётся неизменным (или меняется слабо — поэтому в F нет vh).
        # Строки 5-7: Скорости (vx, vy, vw) остаются постоянными (диагональные 1).

        # Матрица измерения
        # Показывает, какие параметры состояния видны в измерениях. Здесь — только [x, y, w, h] (без скоростей).
        self.kf.H = np.array([
            [1,0,0,0,0,0,0],  # измеряем x: z_x = 1*x + 0*y + 0*w + 0*h + 0*vx + 0*vy + 0*vw = x
            [0,1,0,0,0,0,0],  # измеряем y: аналогично, z_y = y
            [0,0,1,0,0,0,0],  # измеряем w: аналогично
            [0,0,0,1,0,0,0]   # измеряем h: аналогично
        ])

        # Ковариация измерения (шум)
        self.kf.R[2:,2:] *= 10.

        # Ковариация состояния (начальная)
        self.kf.P[4:,4:] *= 1000. # Даем высокую неопределенность неизмеряемым начальным скоростям
        self.kf.P *= 10.

        # Шум процесса
        self.kf.Q[-1,-1] *= 0.01
        self.kf.Q[4:,4:] *= 0.01

        # Инициализация состояния
        self.kf.x[:4] = self.convert_bbox_to_z(bbox)
        self.id = KalmanBoxTracker.count
        self.class_id = class_id
        KalmanBoxTracker.count += 1
        self.history = []
        self.hits = 0
        self.hit_streak = 0
        self.age = 0
        self.time_since_update = 0
        self.birth_frame = 0
        self.death_frame = None

    def update(self, bbox, class_id=None):
        self.time_since_update = 0
        self.history = []
        self.hits += 1
        self.hit_streak += 1
        if class_id is not None:
            self.class_id = class_id
        self.kf.update(self.convert_bbox_to_z(bbox))

    def predict(self):
        if (self.kf.x[6] + self.kf.x[2]) <= 0:
            self.kf.x[6] *= 0.0
        self.kf.predict()
        self.age += 1
        if self.time_since_update > 0:
            self.hit_streak = 0
        self.time_since_update += 1
        self.history.append(self.convert_x_to_bbox(self.kf.x))
        return self.history[-1]

    def get_state(self):
        return self.convert_x_to_bbox(self.kf.x)

    @staticmethod
    def convert_bbox_to_z(bbox):
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = bbox[0] + w/2.
        y = bbox[1] + h/2.
        s = w * h
        r = w / float(h)
        return np.array([x, y, s, r]).reshape((4, 1))

    @staticmethod
    def convert_x_to_bbox(x, score=None):
        w = np.sqrt(x[2] * x[3])
        h = x[2] / w
        if score is None:
            return np.array([x[0]-w/2., x[1]-h/2., x[0]+w/2., x[1]+h/2.]).reshape((1,4))
        else:
            return np.array([x[0]-w/2., x[1]-h/2., x[0]+w/2., x[1]+h/2., score]).reshape((1,5))

def iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
    box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    iou = intersection / float(box1_area + box2_area - intersection)
    return iou

def associate_detections_to_trackers(detections, trackers, iou_threshold=0.3):
    if len(trackers) == 0:
        return np.empty((0,2), dtype=int), np.arange(len(detections)), np.empty((0,5), dtype=int)

    iou_matrix = np.zeros((len(detections), len(trackers)), dtype=np.float32)
    for d, det in enumerate(detections):
        for t, trk in enumerate(trackers):
            iou_matrix[d, t] = iou(det, trk)

    if min(iou_matrix.shape) > 0:
        a = (iou_matrix > iou_threshold).astype(np.int32)
        if a.sum(1).max() == 1 and a.sum(0).max() == 1:
            matched_indices = np.stack(np.where(a), axis=1)
        else:
            row_ind, col_ind = linear_sum_assignment(-iou_matrix)
            matched_indices = np.array([[row, col] for row, col in zip(row_ind, col_ind)])
    else:
        matched_indices = np.empty(shape=(0,2))

    unmatched_detections = []
    for d, det in enumerate(detections):
        if d not in matched_indices[:,0]:
            unmatched_detections.append(d)

    unmatched_trackers = []
    for t, trk in enumerate(trackers):
        if t not in matched_indices[:,1]:
            unmatched_trackers.append(t)

    matches = []
    for m in matched_indices:
        if iou_matrix[m[0], m[1]] < iou_threshold:
            unmatched_detections.append(m[0])
            unmatched_trackers.append(m[1])
        else:
            matches.append(m.reshape(1,2))

    if len(matches) == 0:
        matches = np.empty((0,2), dtype=int)
    else:
        matches = np.concatenate(matches, axis=0)

    return matches, np.array(unmatched_detections), np.array(unmatched_trackers)

class Sort(object):
    def __init__(self, max_age=1, min_hits=3, iou_threshold=0.3):
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.trackers = []
        self.frame_count = 0
        self.total_unique_objects = 0
        self.false_positives = 0
        self.track_lifetimes = []

    def update(self, dets=np.empty((0,5)), class_ids=None):
        self.frame_count += 1

        trks = np.zeros((len(self.trackers), 5))
        to_del = []
        ret = []

        for t, trk in enumerate(trks):
            pos = self.trackers[t].predict()[0]
            trk[:] = [pos[0], pos[1], pos[2], pos[3], 0]
            if np.any(np.isnan(pos)):
                to_del.append(t)

        trks = np.ma.compress_rows(np.ma.masked_invalid(trks))
        for t in reversed(to_del):
            tracker = self.trackers.pop(t)
            self._handle_tracker_deletion(tracker)

        matched, unmatched_dets, unmatched_trks = associate_detections_to_trackers(dets, trks, self.iou_threshold)

        for m in matched:
            det_class = class_ids[m[0]] if class_ids is not None else None
            self.trackers[m[1]].update(dets[m[0], :], det_class)

        for i in unmatched_dets:
            det_class = class_ids[i] if class_ids is not None else 0
            trk = KalmanBoxTracker(dets[i,:], det_class)
            trk.birth_frame = self.frame_count
            self.trackers.append(trk)
            self.total_unique_objects += 1

        i = len(self.trackers)
        for trk in reversed(self.trackers):
            d = trk.get_state()[0]
            if (trk.time_since_update < 1) and (trk.hit_streak >= self.min_hits or self.frame_count <= self.min_hits):
                ret.append(np.concatenate((d, [trk.id+1, trk.class_id])).reshape(1,-1))
            i -= 1

            if trk.time_since_update > self.max_age:
                tracker = self.trackers.pop(i)
                self._handle_tracker_deletion(tracker)

        if len(ret) > 0:
            return np.concatenate(ret)
        return np.empty((0,6))

    def _handle_tracker_deletion(self, tracker):
        tracker.death_frame = self.frame_count
        lifetime = tracker.death_frame - tracker.birth_frame
        self.track_lifetimes.append(lifetime)

        if tracker.hits < self.min_hits:
            self.false_positives += 1

    def get_statistics(self):
        avg_lifetime = np.mean(self.track_lifetimes) if self.track_lifetimes else 0
        return {
            'total_unique_objects': self.total_unique_objects,
            'average_lifetime': avg_lifetime,
            'false_positives': self.false_positives
        }

model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
    'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut',
    'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table', 'N/A', 'N/A',
    'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

def detect_objects(img, model, threshold=0.5):
    img_tensor = torchvision.transforms.functional.to_tensor(img)
    img_tensor = img_tensor.unsqueeze(0)

    with torch.no_grad():
        predictions = model(img_tensor)

    boxes = predictions[0]['boxes'].cpu().numpy()
    scores = predictions[0]['scores'].cpu().numpy()
    labels = predictions[0]['labels'].cpu().numpy()

    mask = scores >= threshold
    boxes = boxes[mask]
    scores = scores[mask]
    labels = labels[mask]

    detections = np.hstack((boxes, scores[:, np.newaxis]))
    return detections, labels

def track_objects(video_path, output_path='output.mp4'):
    mot_tracker = Sort(max_age=5, min_hits=3, iou_threshold=0.3)

    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections, labels = detect_objects(rgb_frame, model)

        tracked_objects = mot_tracker.update(detections, labels)

        for obj in tracked_objects:
            x1, y1, x2, y2, obj_id, class_id = obj
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            obj_id = int(obj_id)
            class_id = int(class_id)

            color = (int(255 * (obj_id % 3)/3), int(255 * (obj_id % 6)/6), int(255 * (obj_id % 9)/9))
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            class_name = COCO_INSTANCE_CATEGORY_NAMES[class_id] if class_id < len(COCO_INSTANCE_CATEGORY_NAMES) else 'unknown'
            label = f'ID: {obj_id}, {class_name}'
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        out.write(frame)
        frame_count += 1

        if frame_count % 50 == 0:
            print(f'Processed {frame_count} frames')

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    stats = mot_tracker.get_statistics()
    print(f'Tracking completed. Result saved to {output_path}')
    print(f'Total unique objects: {stats["total_unique_objects"]}')
    print(f'Average track lifetime: {stats["average_lifetime"]:.2f} frames')
    print(f'False positives: {stats["false_positives"]}')

video_path = "/content/drive/MyDrive/lab7/my_video.mp4"
output_path = "my_video_tracked.mp4"
track_objects(video_path, output_path)

import cv2
import matplotlib.pyplot as plt
import numpy as np

def show_frames_grid(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_indices = np.linspace(0, total_frames-1, 9, dtype=int)

    fig, axes = plt.subplots(3, 3, figsize=(12, 12))

    for i, frame_idx in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()

        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            row, col = i // 3, i % 3
            axes[row, col].imshow(frame_rgb)
            axes[row, col].set_title(f'Кадр {frame_idx}')
            axes[row, col].axis('off')

    cap.release()
    plt.tight_layout()
    plt.show()

show_frames_grid("/content/drive/MyDrive/lab7/my_video_tracked.mp4")
        """

        elif ind == 1:
            code = """
import numpy as np
import cv2
import torch
from ultralytics import YOLO
from filterpy.kalman import KalmanFilter
from collections import defaultdict
from scipy.optimize import linear_sum_assignment
import time

class Sort(object):
    def __init__(self, max_age=1, min_hits=3, iou_threshold=0.3):
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.trackers = []
        self.frame_count = 0
        self.total_unique_objects = 0
        self.false_positives = 0
        self.track_lifetimes = []

        self.id_switches = 0
        self.fragmented_tracks = 0
        self.detection_errors = {
            'missed_detections': 0,
            'false_detections': 0,
            'low_confidence_detections': 0,
            'high_overlap_detections': 0
        }
        self.track_quality_metrics = []

    def update(self, dets=np.empty((0,5)), class_ids=None, confidences=None):
        self.frame_count += 1

        self._analyze_detection_quality(dets, confidences)

        trks = np.zeros((len(self.trackers), 5))
        to_del = []
        ret = []

        for t, trk in enumerate(trks):
            pos = self.trackers[t].predict()[0]
            trk[:] = [pos[0], pos[1], pos[2], pos[3], 0]
            if np.any(np.isnan(pos)):
                to_del.append(t)

        trks = np.ma.compress_rows(np.ma.masked_invalid(trks))
        for t in reversed(to_del):
            tracker = self.trackers.pop(t)
            self._handle_tracker_deletion(tracker)

        matched, unmatched_dets, unmatched_trks = associate_detections_to_trackers(dets, trks, self.iou_threshold)

        for m in matched:
            det_class = class_ids[m[0]] if class_ids is not None else None
            det_conf = confidences[m[0]] if confidences is not None else None
            self.trackers[m[1]].update(dets[m[0], :], det_class, det_conf)

        for i in unmatched_dets:
            det_class = class_ids[i] if class_ids is not None else 0
            det_conf = confidences[i] if confidences is not None else 0.5
            trk = KalmanBoxTracker(dets[i,:], det_class, det_conf)
            trk.birth_frame = self.frame_count
            self.trackers.append(trk)
            self.total_unique_objects += 1

        self.detection_errors['missed_detections'] += len(unmatched_trks)

        i = len(self.trackers)
        for trk in reversed(self.trackers):
            d = trk.get_state()[0]
            if (trk.time_since_update < 1) and (trk.hit_streak >= self.min_hits or self.frame_count <= self.min_hits):
                ret.append(np.concatenate((d, [trk.id+1, trk.class_id])).reshape(1,-1))
            i -= 1

            if trk.time_since_update > self.max_age:
                tracker = self.trackers.pop(i)
                self._handle_tracker_deletion(tracker)

        if len(ret) > 0:
            return np.concatenate(ret)
        return np.empty((0,6))

    def _analyze_detection_quality(self, dets, confidences):
        if len(dets) == 0:
            return

        if confidences is not None:
            low_conf_count = np.sum(confidences < 0.5)
            self.detection_errors['low_confidence_detections'] += low_conf_count

        overlap_count = 0
        for i in range(len(dets)):
            for j in range(i+1, len(dets)):
                if iou(dets[i], dets[j]) > 0.7:
                    overlap_count += 1
        self.detection_errors['high_overlap_detections'] += overlap_count

    def _handle_tracker_deletion(self, tracker):
        tracker.death_frame = self.frame_count
        lifetime = tracker.death_frame - tracker.birth_frame
        self.track_lifetimes.append(lifetime)

        quality_metrics = {
            'lifetime': lifetime,
            'hits': tracker.hits,
            'missed_detections': tracker.missed_detections,
            'avg_confidence': tracker.get_avg_confidence(),
            'class_switches': tracker.class_switches
        }
        self.track_quality_metrics.append(quality_metrics)

        if tracker.hits < self.min_hits:
            self.false_positives += 1

        if tracker.class_switches > 2:
            self.id_switches += tracker.class_switches

        if tracker.missed_detections > lifetime * 0.3:
            self.fragmented_tracks += 1

    def get_statistics(self):
        avg_lifetime = np.mean(self.track_lifetimes) if self.track_lifetimes else 0

        if self.track_quality_metrics:
            avg_hits = np.mean([m['hits'] for m in self.track_quality_metrics])
            avg_confidence = np.mean([m['avg_confidence'] for m in self.track_quality_metrics])
            total_class_switches = sum([m['class_switches'] for m in self.track_quality_metrics])
        else:
            avg_hits = 0
            avg_confidence = 0
            total_class_switches = 0

        return {
            'total_unique_objects': self.total_unique_objects,
            'average_lifetime': avg_lifetime,
            'false_positives': self.false_positives,
            'id_switches': total_class_switches,
            'fragmented_tracks': self.fragmented_tracks,
            'detection_errors': self.detection_errors,
            'avg_hits_per_track': avg_hits,
            'avg_confidence': avg_confidence
        }

# YOLOv8 detection
def detect_objects_yolo(img, model, threshold=0.5):
    results = model(img, verbose=False)

    if len(results[0].boxes) == 0:
        return np.empty((0,5)), np.array([])

    boxes = results[0].boxes.xyxy.cpu().numpy()
    scores = results[0].boxes.conf.cpu().numpy()
    labels = results[0].boxes.cls.cpu().numpy().astype(int)

    mask = scores >= threshold
    boxes = boxes[mask]
    scores = scores[mask]
    labels = labels[mask]

    detections = np.hstack((boxes, scores[:, np.newaxis]))
    return detections, labels

# SSD detection
def detect_objects_ssd(img, model, threshold=0.5):
    import torchvision.transforms as T

    transform = T.Compose([T.ToTensor()])
    img_tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        predictions = model(img_tensor)

    boxes = predictions[0]['boxes'].cpu().numpy()
    scores = predictions[0]['scores'].cpu().numpy()
    labels = predictions[0]['labels'].cpu().numpy()

    mask = scores >= threshold
    boxes = boxes[mask]
    scores = scores[mask]
    labels = labels[mask]

    detections = np.hstack((boxes, scores[:, np.newaxis]))
    return detections, labels

def track_objects_comparative(video_path, output_path='output.mp4', detector_type='yolo'):
    if detector_type == 'yolo':
        model = YOLO('yolov8n.pt')
        detect_func = detect_objects_yolo
        class_names = model.names
    elif detector_type == 'ssd':
        import torchvision
        model = torchvision.models.detection.ssd300_vgg16(pretrained=True)
        model.eval()
        detect_func = detect_objects_ssd
        class_names = {
            0: '__background__', 1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle',
            5: 'airplane', 6: 'bus', 7: 'train', 8: 'truck', 9: 'boat'
        }
    else:
        raise ValueError("Unsupported detector type")

    mot_tracker = Sort(max_age=5, min_hits=3, iou_threshold=0.3)

    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    total_detection_time = 0
    detection_counts = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        start_time = time.time()
        detections, labels = detect_func(rgb_frame, model)
        detection_time = time.time() - start_time
        total_detection_time += detection_time

        detection_counts.append(len(detections))

        confidences = detections[:, 4] if len(detections) > 0 else np.array([])

        tracked_objects = mot_tracker.update(detections, labels, confidences)

        for obj in tracked_objects:
            x1, y1, x2, y2, obj_id, class_id = obj
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            obj_id = int(obj_id)
            class_id = int(class_id)

            color = (int(255 * (obj_id % 3)/3), int(255 * (obj_id % 6)/6), int(255 * (obj_id % 9)/9))
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            class_name = class_names.get(class_id, 'unknown') if isinstance(class_names, dict) else class_names[class_id]
            label = f'ID: {obj_id}, {class_name}'
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        cv2.putText(frame, f'Frame: {frame_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f'Detections: {len(detections)}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f'Tracks: {len(tracked_objects)}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        out.write(frame)
        frame_count += 1

        if frame_count % 50 == 0:
            print(f'Processed {frame_count} frames')

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    stats = mot_tracker.get_statistics()
    avg_detection_time = total_detection_time / frame_count if frame_count > 0 else 0
    avg_detections_per_frame = np.mean(detection_counts) if detection_counts else 0

    print(f'\n=== АНАЛИЗ ТРЕКИНГА С {detector_type.upper()} ===')
    print(f'Обработано кадров: {frame_count}')
    print(f'Среднее время детекции: {avg_detection_time:.4f} сек')
    print(f'Среднее количество детекций на кадр: {avg_detections_per_frame:.2f}')
    print(f'\n--- ОСНОВНЫЕ МЕТРИКИ ---')
    print(f'Всего уникальных объектов: {stats["total_unique_objects"]}')
    print(f'Среднее время жизни трека: {stats["average_lifetime"]:.2f} кадров')
    print(f'Ложные срабатывания: {stats["false_positives"]}')
    print(f'Переключения ID: {stats["id_switches"]}')
    print(f'Фрагментированные треки: {stats["fragmented_tracks"]}')
    print(f'Средняя уверенность треков: {stats["avg_confidence"]:.3f}')
    print(f'\n--- ОШИБКИ ДЕТЕКЦИИ ---')
    print(f'Пропущенные детекции: {stats["detection_errors"]["missed_detections"]}')
    print(f'Детекции с низкой уверенностью: {stats["detection_errors"]["low_confidence_detections"]}')
    print(f'Перекрывающиеся детекции: {stats["detection_errors"]["high_overlap_detections"]}')

    print(f'\n--- АНАЛИЗ КРИТИЧНОСТИ ОШИБОК ---')
    critical_errors = analyze_critical_errors(stats)
    for error_type, severity in critical_errors.items():
        print(f'{error_type}: {severity}')

    return stats

def analyze_critical_errors(stats):
    critical_analysis = {}

    missed_ratio = stats["detection_errors"]["missed_detections"] / max(stats["total_unique_objects"], 1)
    if missed_ratio > 0.3:
        critical_analysis["Пропущенные детекции"] = "КРИТИЧНО - может привести к потере треков"
    elif missed_ratio > 0.1:
        critical_analysis["Пропущенные детекции"] = "УМЕРЕННО - снижает стабильность"
    else:
        critical_analysis["Пропущенные детекции"] = "ДОПУСТИМО"

    id_switch_ratio = stats["id_switches"] / max(stats["total_unique_objects"], 1)
    if id_switch_ratio > 0.5:
        critical_analysis["Переключения ID"] = "КРИТИЧНО - нарушает непрерывность трекинга"
    elif id_switch_ratio > 0.2:
        critical_analysis["Переключения ID"] = "УМЕРЕННО - ухудшает качество"
    else:
        critical_analysis["Переключения ID"] = "ДОПУСТИМО"

    fragment_ratio = stats["fragmented_tracks"] / max(stats["total_unique_objects"], 1)
    if fragment_ratio > 0.4:
        critical_analysis["Фрагментация треков"] = "КРИТИЧНО - много прерванных треков"
    elif fragment_ratio > 0.2:
        critical_analysis["Фрагментация треков"] = "УМЕРЕННО - влияет на качество"
    else:
        critical_analysis["Фрагментация треков"] = "ДОПУСТИМО"

    false_positive_ratio = stats["false_positives"] / max(stats["total_unique_objects"], 1)
    if false_positive_ratio > 0.3:
        critical_analysis["Ложные срабатывания"] = "КРИТИЧНО - много шумовых треков"
    elif false_positive_ratio > 0.15:
        critical_analysis["Ложные срабатывания"] = "УМЕРЕННО - загрязняет результаты"
    else:
        critical_analysis["Ложные срабатывания"] = "ДОПУСТИМО"

    return critical_analysis

def compare_detectors(video_path):
    print("Сравнение детекторов для SORT трекинга\n")
    print("Тестирование YOLOv8...")
    yolo_stats = track_objects_comparative(video_path, 'yolo_output.mp4', 'yolo')
    print("\n" + "="*50 + "\n")
    return yolo_stats
stats = compare_detectors(video_path)
stats
"""
        elif ind == 2:
            code == """
from ikomia.dataprocess.workflow import Workflow
import cv2
import numpy as np
from collections import defaultdict
import json

input_video_path = '/content/drive/MyDrive/lab7/my_video.mp4'
output_video_path = 'deepsort_output_video.avi'

wf = Workflow()

detector = wf.add_task(name="infer_yolo_v7", auto_connect=True)
detector.set_parameters({
    "conf_thres": "0.5",
    "iou_thres": "0.45",
    "input_size": "640"
})

tracking = wf.add_task(name="infer_deepsort", auto_connect=True)
tracking.set_parameters({
    "categories": "person,car",
    "conf_thres": "0.5",
    "max_age": "50",
    "min_hits": "3",
    "iou_threshold": "0.2",
    "cosine_threshold": "0.2",
    "nn_budget": "100",
    "use_cuda": "True"
})

TARGET_CLASSES = {'person', 'car'}
COCO_CLASSES = {0: 'person', 2: 'car', 5: 'bus', 7: 'truck'}

stream = cv2.VideoCapture(input_video_path)
frame_width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_rate = stream.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (frame_width, frame_height))

frame_count = 0
total_counts = defaultdict(int)
class_statistics = []
track_history = defaultdict(list)

def extract_detection_info(obj_detect_out):
    detections_info = []

    try:
        if hasattr(obj_detect_out, 'get_objects'):
            objects = obj_detect_out.get_objects()
            for obj in objects:
                class_name = getattr(obj, 'label', 'unknown')
                if class_name in TARGET_CLASSES:
                    detection = {
                        'class_name': class_name,
                        'track_id': getattr(obj, 'id', -1),
                        'confidence': getattr(obj, 'confidence', 0.0),
                        'bbox': [getattr(obj, 'x', 0), getattr(obj, 'y', 0),
                                getattr(obj, 'width', 0), getattr(obj, 'height', 0)]
                    }
                    detections_info.append(detection)

        elif hasattr(obj_detect_out, '__iter__'):
            for item in obj_detect_out:
                try:
                    if hasattr(item, 'label'):
                        class_name = item.label
                    elif hasattr(item, 'class_id'):
                        class_name = COCO_CLASSES.get(item.class_id, 'unknown')
                    else:
                        continue

                    if class_name in TARGET_CLASSES:
                        detection = {
                            'class_name': class_name,
                            'track_id': getattr(item, 'id', -1),
                            'confidence': getattr(item, 'confidence', 0.0),
                            'bbox': [getattr(item, 'x', 0), getattr(item, 'y', 0),
                                    getattr(item, 'width', 0), getattr(item, 'height', 0)]
                        }
                        detections_info.append(detection)
                except:
                    continue

        elif hasattr(obj_detect_out, 'data'):
            data = obj_detect_out.data
            items = data if isinstance(data, list) else [data]
            for item in items:
                try:
                    class_name = getattr(item, 'label', COCO_CLASSES.get(getattr(item, 'class_id', -1), 'unknown'))
                    if class_name in TARGET_CLASSES:
                        detection = {
                            'class_name': class_name,
                            'track_id': getattr(item, 'id', -1),
                            'confidence': getattr(item, 'confidence', 0.0),
                            'bbox': [getattr(item, 'x', 0), getattr(item, 'y', 0),
                                    getattr(item, 'width', 0), getattr(item, 'height', 0)]
                        }
                        detections_info.append(detection)
                except:
                    continue

    except Exception as e:
        print(f"Warning: {e}")

    return detections_info

def count_objects_by_class(detections_info):
    class_counts = defaultdict(int)
    unique_tracks = defaultdict(set)

    for detection in detections_info:
        class_name = detection['class_name']
        track_id = detection['track_id']

        if class_name in TARGET_CLASSES:
            class_counts[class_name] += 1
            if track_id != -1:
                unique_tracks[class_name].add(track_id)

    unique_counts = {class_name: len(tracks) for class_name, tracks in unique_tracks.items()}
    return dict(class_counts), dict(unique_counts)

def update_track_history(detections_info, track_history, frame_count):
    for detection in detections_info:
        track_id = detection['track_id']
        class_name = detection['class_name']

        if track_id != -1:
            track_history[track_id].append({
                'frame': frame_count,
                'class': class_name,
                'bbox': detection['bbox'],
                'confidence': detection['confidence']
            })

def draw_statistics(frame, class_counts, unique_counts, frame_number, track_counts):
    overlay = frame.copy()
    cv2.rectangle(overlay, (5, 5), (300, 180), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)

    y = 25
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(frame, f'Frame: {frame_number}', (10, y), font, 0.6, (255, 255, 255), 2)
    y += 25

    cv2.putText(frame, 'Current detections:', (10, y), font, 0.6, (0, 255, 255), 2)
    y += 20

    for class_name in TARGET_CLASSES:
        count = class_counts.get(class_name, 0)
        unique = unique_counts.get(class_name, 0)

        color = (0, 255, 0) if class_name == 'person' else (255, 100, 0)
        text = f'{class_name}: {count} ({unique} tracks)'
        cv2.putText(frame, text, (15, y), font, 0.5, color, 2)
        y += 20

    total_detections = sum(class_counts.values())
    total_unique = sum(unique_counts.values())
    cv2.putText(frame, f'Total: {total_detections} ({total_unique} tracks)', (10, y), font, 0.6, (0, 255, 255), 2)
    y += 25

    cv2.putText(frame, 'All-time tracks:', (10, y), font, 0.5, (255, 255, 0), 2)
    y += 20
    for class_name in TARGET_CLASSES:
        total_tracks = track_counts.get(class_name, 0)
        cv2.putText(frame, f'{class_name}: {total_tracks}', (15, y), font, 0.5, (255, 255, 0), 2)
        y += 20

    return frame

def get_track_counts(track_history):
    track_counts = defaultdict(set)
    for track_id, history in track_history.items():
        if history:
            class_name = history[-1]['class']
            track_counts[class_name].add(track_id)
    return {class_name: len(tracks) for class_name, tracks in track_counts.items()}

while True:
    ret, frame = stream.read()

    if not ret:
        break

    frame_count += 1

    wf.run_on(array=frame)

    image_out = tracking.get_output(0)
    obj_detect_out = tracking.get_output(1)

    detections_info = extract_detection_info(obj_detect_out)

    class_counts, unique_counts = count_objects_by_class(detections_info)

    update_track_history(detections_info, track_history, frame_count)

    track_counts = get_track_counts(track_history)

    for class_name, count in class_counts.items():
        total_counts[class_name] += count

    class_statistics.append({
        'frame': frame_count,
        'detections': class_counts.copy(),
        'unique_tracks': unique_counts.copy()
    })

    img_out = image_out.get_image_with_graphics(obj_detect_out)
    img_res = cv2.cvtColor(img_out, cv2.COLOR_RGB2BGR)

    img_res = draw_statistics(img_res, class_counts, unique_counts, frame_count, track_counts)

    out.write(img_res)

    if frame_count % 30 == 0:
        print(f"Frame {frame_count}: {class_counts}")

stream.release()
out.release()

print(f"\nTotal frames: {frame_count}")

for class_name in TARGET_CLASSES:
    total_detections = total_counts.get(class_name, 0)
    avg_per_frame = total_detections / frame_count if frame_count > 0 else 0
    print(f"{class_name}: {total_detections} total, {avg_per_frame:.2f} avg/frame")

final_track_counts = get_track_counts(track_history)
for class_name in TARGET_CLASSES:
    unique_tracks = final_track_counts.get(class_name, 0)
    print(f"{class_name} unique tracks: {unique_tracks}")

if class_statistics:
    for class_name in TARGET_CLASSES:
        detection_counts = [frame_stats['detections'].get(class_name, 0) for frame_stats in class_statistics]

        if detection_counts:
            print(f"{class_name} per frame - max: {max(detection_counts)}, avg: {sum(detection_counts) / len(detection_counts):.2f}")

with open('tracking_stats.json', 'w') as f:
    json.dump({
        'frame_statistics': class_statistics,
        'total_counts': dict(total_counts),
        'track_counts': final_track_counts,
        'frame_count': frame_count
    }, f, indent=2)

print(f"Video saved: {output_video_path}")
print("Stats saved: tracking_stats.json")

show_frames_grid("/content/drive/MyDrive/lab7/deepsort_output_video.avi")
"""
        pyperclip.copy(code.strip())

    def remove_comments_and_docstrings(self, code: str) -> str:
        try:
            output = []
            prev_toktype = None
            last_lineno = -1
            last_col = 0

            tokgen = tokenize.generate_tokens(io.StringIO(code).readline)

            for tok_type, tok_val, (start_line, start_col), (end_line, end_col), _ in tokgen:
                if tok_type == tokenize.STRING and prev_toktype in {tokenize.INDENT, tokenize.NEWLINE, None}:
                    continue
                elif tok_type == tokenize.COMMENT:
                    continue

                if start_line > last_lineno:
                    output.append('\n' * (start_line - last_lineno))
                    last_col = 0
                if start_col > last_col:
                    output.append(' ' * (start_col - last_col))

                output.append(tok_val)
                prev_toktype = tok_type
                last_lineno = end_line
                last_col = end_col

            return ''.join(output).strip()
        except Exception as e:
            return f"# Ошибка при постобработке: {e}"

    def putText(self, api_key: str, task_text: str, model: str = "gpt-4o") -> str:
        client = OpenAI(api_key=api_key)

        prompt = f"""
        Ты — умный и лаконичный помощник, который решает задания по теме компьютерного зрения.
        Приведи решение в виде кода на Python для следующего задания. Возвращай только код, НЕ пиши в нем комментарии (ни через '#', ни черещ тройные кавычки) и не добавляй ничего лишнего.
        Решение должно быть полным и запускаться в ячейке jupyter ноутбука (и в колабе в том числе)/

        Задание:
        {task_text}
        """

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Ты — помощник, который решает задания."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            content = response.choices[0].message.content.strip()

            code_match = re.search(
                r"```(?:python)?\s*(.*?)```", content, re.DOTALL)
            code = code_match.group(1).strip() if code_match else content
            return self.remove_comments_and_docstrings(code)
        except Exception as e:
            return f"Ошибка: {e}"

    def help(self):
        """Выводит справку о всех доступных методах."""
        help_message = "Справка по методам:\n"
        for method, description in self.methods_info.items():
            help_message += f"- {method}: {description}\n"
        pyperclip.copy(help_message)
