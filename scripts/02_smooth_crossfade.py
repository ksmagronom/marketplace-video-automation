import os
from moviepy.editor import ImageClip, CompositeVideoClip

# ================= НАСТРОЙКИ =================
IMAGE_FOLDER = "images"
OUTPUT_FILE = "output_crossfade.mp4"
DURATION_PER_IMAGE = 3.0
FADE_DURATION = 0.5      # Длительность плавного перехода (секунды)
TARGET_SIZE = (1080, 1440) # Формат 3:4
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
    print(f"✅ Найдено {len(image_files)} изображений. Создаем видео с плавными переходами...")
    
    clips = []
    for i, img in enumerate(image_files):
        clip = ImageClip(img, duration=DURATION_PER_IMAGE).resize(TARGET_SIZE).set_position('center')
        
        if i == 0:
            clip = clip.set_start(0)
        else:
            # Сдвигаем начало клипа, чтобы он накладывался на предыдущий
            start_time = i * (DURATION_PER_IMAGE - FADE_DURATION)
            clip = clip.set_start(start_time).crossfadein(FADE_DURATION)
            
        clips.append(clip)

    # Рассчитываем точную общую длительность
    total_duration = len(clips) * DURATION_PER_IMAGE - (len(clips) - 1) * FADE_DURATION

    # Накладываем клипы друг на друга
    final_video = CompositeVideoClip(clips, size=TARGET_SIZE).set_duration(total_duration)

    final_video.write_videofile(OUTPUT_FILE, fps=24, codec="libx264", audio=False, logger=None)
    print(f"🎉 Готово! Видео с переходами сохранено как '{OUTPUT_FILE}'")
