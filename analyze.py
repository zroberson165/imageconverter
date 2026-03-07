from PIL import Image
import os
from utils import open_image
import rawpy
import io

#Analysis of image files to recommend settings
def analyze_image(input_path):
    print("-------------------------")
    print("Recommended Settings:")
    validInputFormats = [".HEIC",".png","jpg",".jpeg", ".NEF", "RAW", ".CR2", ".ARW"]
    dirs = os.listdir(input_path)
    dict_list = []
    for file in dirs:
        name, ext = os.path.splitext(file)
        if ext not in validInputFormats:
            print(f"{name}{ext} is invalid for conversion, skipping")
            continue
        old_path = os.path.join(input_path, file)
        if ext in [".NEF", "RAW", ".CR2", ".ARW"]:
            with rawpy.imread(old_path) as raw:
                thumb = raw.extract_thumb()
                preview_img = Image.open(io.BytesIO(thumb.data))
                temp = preview_img
        else:
            temp = open_image(old_path, ext)
        img_width, img_height = temp.size
        print(f"{file} dimensions: {img_width}x{img_height}")
        if(ext == ".jpg" or ext == ".jpeg"):
            print(f"{file} - Recommended Settings: No Resize, Quality 85, Format as jpg")
            new_dict = {"file": file, "resize": 0, "quality": 85, "format": ".jpg"}
            dict_list.append(new_dict)
        elif("A" in temp.mode):
            print(f"{file} - Recommended Settings: No Resize, Quality 60, Format .PNG")
            new_dict = {"file": file, "resize": 0, "quality": 60, "format": ".png"}
            dict_list.append(new_dict)
        elif(img_width > 4000 or img_height > 4000):
            print(f"{file} - Recommended Settings: 50% Resize, Quality 65, Format .jpg")
            new_dict = {"file": file, "resize": 50, "quality": 65, "format": ".jpg"}
            dict_list.append(new_dict)
        else:
            print(f"{file} - Recommended Settings: No Resize, Quality 85, Format .jpg")
            new_dict = {"file": file, "resize": 0, "quality": 85, "format": ".jpg"}
            dict_list.append(new_dict)
    print("-------------------------")
    return dict_list