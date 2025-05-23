import os
import subprocess

def split_video_by_size(input_path, output_dir, size_mb=99, crf=23):
    os.makedirs(output_dir, exist_ok=True)
    output_pattern = os.path.join(output_dir, 'part_%03d.mkv')
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'libx264',
        '-crf', str(crf),
        '-preset', 'fast',
        '-c:a', 'aac',
        '-f', 'segment',
        '-segment_format', 'matroska',
        '-fs', f'{size_mb * 1024 * 1024}',
        output_pattern
    ]
    subprocess.run(cmd, check=True)
    return sorted([os.path.join(output_dir, f) for f in os.listdir(output_dir)])
