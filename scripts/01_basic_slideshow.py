import os
from moviepy.editor import ImageClip, concatenate_videoclips

# ================= НАСТРОЙКИ =================
IMAGE_FOLDER = "images"          # Папка с вашими фото
OUTPUT_FILE = "output_basic.mp4" # Имя готового видео
DURATION_PER_IMAGE = 3.0         # Время показа одного фото (секунды)
TARGET_SIZE = (1080, 1440)       # Формат 3:4 (Ширина, Высота). Для 1:1 используйте (1080, 1080)
# =============================================

# Создаем папку images, если её нет (чтобы не было ошибки при первом запуске)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Собираем список изображений, сортируем по имени
image_files = sorted([
    os.path.join(IMAGE_FOLDER, f) 
    for f in os.listdir(IMAGE_FOLDER) 
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
])

if not image_files:
    print(f"⚠️ В папке '{IMAGE_FOLDER}' не найдено изображений.")
    print("👉 Загрузите фото в эту папку (перетащите в левую панель Colab) и запустите ячейку снова.")
else:
    print(f"✅ Найдено {len(image_files)} изображений. Начинаем сборку видео...")
    
    clips = []
    for img in image_files:
        # Изменяем размер под целевой формат и центрируем
        clip = ImageClip(img, duration=DURATION_PER_IMAGE).resize(TARGET_SIZE).set_position('center')
        clips.append(clip)

    # Склеиваем клипы в одно видео
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Сохраняем видео (без звука, с оптимальным кодеком для маркетплейсов)
    final_video.write_videofile(OUTPUT_FILE, fps=24, codec="libx264", audio=False, logger=None)
    
    print(f"🎉 Готово! Видео успешно сохранено как '{OUTPUT_FILE}'")
    print("📥 Нажмите на иконку папки слева в Colab, обновите список файлов и скачайте результат.")
