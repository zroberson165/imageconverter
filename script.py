from PIL import Image
from pillow_heif import register_heif_opener
import os
import argparse
import sys

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
#converting images logic
def convert_image(input_path, output_path, format, quality, resize, recursive):
    validInputFormats = [".HEIC",".png","jpg",".jpeg", ".NEF"]
    if(recursive):
        for root, dirs, files in os.walk(input_path):
            for file in files:
                name, ext = os.path.splitext(file)
                if ext not in validInputFormats:
                    print(f"{name}{ext} is invalid for conversion, skipping")
                    continue
                old_path = os.path.join(root, file)
                temp = Image.open(old_path)
                input_size = convert_bytes(os.path.getsize(input_path))
                relative = os.path.relpath(root, input_path)
                new_png = name + format
                current_output = os.path.join(output_path, relative)
                os.makedirs(current_output, exist_ok=True)
                new_path = os.path.join(current_output, new_png)
                if(resize != 0):
                    new_width = int(temp.size[0] * (resize/100))
                    new_height = int(temp.size[1] * (resize/100))
                    temp.thumbnail((new_width,new_height), Image.LANCZOS)
                temp.save(new_path, quality=quality)
                output_size = convert_bytes(os.path.getsize(new_path))
                print(f"{name}{ext} ({input_size}) -> {new_png} ({output_size})")
    else:
        dirs = os.listdir(input_path)
        for file in dirs:
            name, ext = os.path.splitext(file)
            if ext not in validInputFormats:
                print(f"{name}{ext} is invalid for conversion, skipping")
                continue
            old_path = os.path.join(input_path, file)
            temp = Image.open(old_path)
            input_size = convert_bytes(os.path.getsize(input_path))
            new_png = name + format
            new_path = os.path.join(output_path, new_png)
            if(resize != 0):
                new_width = int(temp.size[0] * (resize/100))
                new_height = int(temp.size[1] * (resize/100))
                temp.thumbnail((new_width,new_height), Image.LANCZOS)
            temp.save(new_path, quality=quality)
            output_size = convert_bytes(os.path.getsize(new_path))
            print(f"{name}{ext} ({input_size}) -> {new_png} ({output_size})")



def main():
    #Parser for determining input output locations and what to convert to
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="folder of images to convert")
    parser.add_argument("--output", help="folder to save converted images")
    parser.add_argument("--format", help="output format")
    parser.add_argument("--quality", help="quality of output", type=int)
    parser.add_argument("--resize", help="resize image width with fixed aspect ratio, enter as percentage", type=int, default=0)
    parser.add_argument("--recursive", help="determine if you should explore subdirectories for conversion", action="store_true")
    args = parser.parse_args()
        
    #Determining if paths exist and creating
    register_heif_opener()
    path = args.input
    if not os.path.exists(path):
        print("Invalid path")
        sys.exit()
    newDir = args.output
    dirs = os.listdir(path)
    os.makedirs(newDir, exist_ok=True)
    validOutputFormats = [".png", ".jpeg", ".jpg"]
    if(args.format not in validOutputFormats):
        print("invalid output format")
        sys.exit()

    convert_image(path, newDir, args.format, args.quality, args.resize, args.recursive)

if __name__ == "__main__":
    main()

