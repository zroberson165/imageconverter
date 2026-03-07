import rawpy
import numpy as np
import io
from PIL import Image
#converting bytes so output is displayed correctly
def convert_bytes(bytes_size):
    kb = bytes_size / 1024
    mb = kb / 1024
    gb = mb / 1024
    if(gb < 1):
        if(mb < 1):
            if(kb < 1):
                return f"{bytes_size:.2f} bytes"
            else:
                return f"{kb:.2f} KB"
        else:
            return f"{mb:.2f} MB"
    else:
        return f"{gb:.2f} GB"
    
#Opening Images
def open_image(old_path, ext):
    if ext in [".NEF", ".RAW", ".CR2", ".ARW"]:
        with rawpy.imread(old_path) as raw:
            #generate base data
            rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=True)
            curr_mean = rgb.mean()

            # Find target brightness from jpeg thumbnail
            try:
                thumb = raw.extract_thumb()
                if thumb.format == rawpy.ThumbFormat.JPEG:
                    preview_img = Image.open(io.BytesIO(thumb.data))
                    target_mean = np.array(preview_img).mean()
                else:
                    # Fallback if the thumbnail isn't a JPEG
                    target_mean = curr_mean * 3.0 
            except rawpy.LibRawNoThumbnailError:
                # Fallback if no thumbnail exists at all
                target_mean = curr_mean * 3.0 

            # Apply scale
            scale = target_mean / curr_mean
            
            # Tone mapping curve
            rgb_float = rgb.astype(np.float32) / 255.0
            rgb_float = rgb_float * scale
            # compress highlights instead of hard clipping
            rgb_float = rgb_float / (1.0 + rgb_float)
            rgb_float *= 1.60
            rgb_scaled = np.clip(rgb_float * 255, 0, 255).astype(np.uint8)
            temp = Image.fromarray(rgb_scaled)
    else:
        temp = Image.open(old_path)
    return temp
