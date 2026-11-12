import os
from moviepy.editor import ImageClip, concatenate_videoclips

# ================= НАСТРОЙКИ =================
IMAGE_FOLDER = "images"
OUTPUT_FILE = "output_zoom.mp4"
DURATION_PER_IMAGE = 3.0
TARGET_SIZE = (1080, 1440) # Формат 3:4
ZOOM_FACTOR = 1.15         # Сила зума (1.15 = плавное приближение на 15%)
# =============================================

os.makedirs(IMAGE_FOLDER, exist_ok=True)

image_files = sorted([
    os.path.join(IMAGE_FOLDER, f)
    for f in os.listdir(IMAGE_FOLDER)
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
])

if not image_files:
    print(f"⚠️ В папке '{IMAGE_FOLDER}' не найдено изображений.")
else:
    print(f"✅ Найдено {len(image_files)} изображений. Создаем видео с эффектом зума...")
    
    clips = []
    for img in image_files:
        # Увеличиваем исходное изображение, чтобы при анимации не было черных полей
        base_size = (int(TARGET_SIZE[0] * ZOOM_FACTOR), int(TARGET_SIZE[1] * ZOOM_FACTOR))
        clip = ImageClip(img, duration=DURATION_PER_IMAGE).resize(base_size)
        
        # Анимируем масштаб: от увеличенного к нормальному (эффект плавного наезда)
        animated_clip = clip.resize(lambda t: ZOOM_FACTOR - (ZOOM_FACTOR - 1.0) * (t / DURATION_PER_IMAGE))
        animated_clip = animated_clip.set_position('center')
        
        clips.append(animated_clip)

    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile(OUTPUT_FILE, fps=24, codec="libx264", audio=False, logger=None)
    print(f"🎉 Готово! Видео с зумом сохранено как '{OUTPUT_FILE}'")
