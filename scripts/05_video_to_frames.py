import cv2
import os

# ================= НАСТРОЙКИ =================
VIDEO_PATH = "input_video.mp4"   # Имя исходного видео
OUTPUT_FOLDER = "extracted_frames" # Папка для сохранения кадров
FRAMES_COUNT = 5                 # Сколько кадров извлечь равномерно
# =============================================

# Создаем папку для кадров
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Открываем видео
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print(f"⚠️ Не удалось открыть видео '{VIDEO_PATH}'.")
    print("👉 Убедитесь, что файл загружен в корень папки Colab и имя совпадает.")
else:
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"✅ Видео открыто. Всего кадров: {total_frames}. Извлекаем {FRAMES_COUNT} кадров...")
    
    # Вычисляем шаг между кадрами для равномерного распределения
    interval = total_frames // (FRAMES_COUNT + 1)
    
    for i in range(1, FRAMES_COUNT + 1):
        # Перемещаемся на нужный кадр
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * interval)
        ret, frame = cap.read()
        
        if ret:
            # Сохраняем кадр с максимальным качеством (100%)
            filename = os.path.join(OUTPUT_FOLDER, f"frame_{i:02d}.jpg")
            cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
            print(f"   📸 Сохранен кадр {i}: {filename}")
        else:
            print(f"   ⚠️ Не удалось прочитать кадр {i}")
            
    cap.release()
    print(f"\n🎉 Готово! Все {FRAMES_COUNT} кадров сохранены в папку '{OUTPUT_FOLDER}'")
    print("📥 Теперь вы можете использовать эти фото в других скриптах или скачать их.")
