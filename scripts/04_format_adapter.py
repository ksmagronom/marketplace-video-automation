import os
from moviepy.editor import ImageClip, CompositeVideoClip

# ================= НАСТРОЙКИ =================
IMAGE_FOLDER = "images"
OUTPUT_FILE = "output_adapted.mp4"
DURATION_PER_IMAGE = 3.0

# Выберите нужный формат, раскомментировав нужную строку (убрав #):
TARGET_SIZE = (1080, 1440) # 3:4 (Стандарт Wildberries, Яндекс Маркет)
# TARGET_SIZE = (1080, 1080) # 1:1 (Квадрат)
# TARGET_SIZE = (1080, 1920) # 9:16 (Stories, Reels, Shorts)

BG_COLOR = (245, 245, 245) # Светло-серый фон для полей (нейтральный для маркетплейсов)
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
    print(f"✅ Найдено {len(image_files)} изображений. Адаптируем под формат {TARGET_SIZE[0]}x{TARGET_SIZE[1]}...")
    
    clips = []
    for img in image_files:
        # 1. Загружаем исходное фото
        original_clip = ImageClip(img, duration=DURATION_PER_IMAGE)
        
        # 2. Вычисляем масштаб, чтобы фото вписалось в рамку без искажений
        scale_w = TARGET_SIZE[0] / original_clip.w
        scale_h = TARGET_SIZE[1] / original_clip.h
        scale = min(scale_w, scale_h) # Берем меньший коэффициент, чтобы ничего не обрезалось
        
        # 3. Изменяем размер
        resized_clip = original_clip.resize(scale)
        
        # 4. Вычисляем отступы для центрирования
        margin_x = (TARGET_SIZE[0] - resized_clip.w) / 2
        margin_y = (TARGET_SIZE[1] - resized_clip.h) / 2
        
        # 5. Добавляем отступы (поля) с заданным цветом фона
        final_clip = resized_clip.margin(
            left=margin_x, right=margin_x, 
            top=margin_y, bottom=margin_y, 
            color=BG_COLOR
        ).set_position('center')
        
        clips.append(final_clip)

    final_video = CompositeVideoClip(clips, size=TARGET_SIZE).set_duration(len(clips) * DURATION_PER_IMAGE)
    
    final_video.write_videofile(OUTPUT_FILE, fps=24, codec="libx264", audio=False, logger=None)
    print(f"🎉 Готово! Адаптированное видео сохранено как '{OUTPUT_FILE}'")
