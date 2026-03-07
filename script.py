from PIL import Image
from pillow_heif import register_heif_opener
import os
import click
from analyze import analyze_image
from utils import open_image, convert_bytes
import rawpy

#converting images logic
def convert_image(input_path, output_path, format, quality, resize, recursive):
    validInputFormats = [".HEIC",".png","jpg",".jpeg", ".NEF", "RAW"]
    input_size_list = []
    output_size_list = []

    #code for single image conversion rather than walking through whole folder
    if(os.path.isfile(input_path)):
        name, ext = os.path.splitext(os.path.basename(input_path))
        if ext not in validInputFormats:
            print(f"{name}{ext} is invalid for conversion, skipping")
            return
        old_path = input_path
        temp = open_image(old_path, ext)
        input_size = convert_bytes(os.path.getsize(old_path))
        input_size_list.append(os.path.getsize(old_path))
        new_png = name + format
        new_path = os.path.join(output_path, new_png)
        if(resize != 0):
            new_width = int(temp.size[0] * (resize/100))
            new_height = int(temp.size[1] * (resize/100))
            temp.thumbnail((new_width,new_height), Image.LANCZOS)
        temp.save(new_path, quality=quality)
        output_size = convert_bytes(os.path.getsize(new_path))
        output_size_list.append(os.path.getsize(new_path))
        print(f"{name}{ext} ({input_size}) -> {new_png} ({output_size})")
    else:
        if(recursive):
            for root, dirs, files in os.walk(input_path):
                for file in files:
                    name, ext = os.path.splitext(file)
                    if ext not in validInputFormats:
                        print(f"{name}{ext} is invalid for conversion, skipping")
                        continue
                    old_path = os.path.join(root, file)
                    temp = open_image(old_path, ext)
                    input_size = convert_bytes(os.path.getsize(old_path))
                    input_size_list.append(os.path.getsize(old_path))
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
                    output_size_list.append(os.path.getsize(new_path))
                    print(f"{name}{ext} ({input_size}) -> {new_png} ({output_size})")
        else:
            dirs = os.listdir(input_path)
            for file in dirs:
                name, ext = os.path.splitext(file)
                if ext not in validInputFormats:
                    print(f"{name}{ext} is invalid for conversion, skipping")
                    continue
                old_path = os.path.join(input_path, file)
                temp = open_image(old_path, ext)
                input_size = convert_bytes(os.path.getsize(old_path))
                input_size_list.append(os.path.getsize(old_path))
                new_png = name + format
                new_path = os.path.join(output_path, new_png)
                if(resize != 0):
                    new_width = int(temp.size[0] * (resize/100))
                    new_height = int(temp.size[1] * (resize/100))
                    temp.thumbnail((new_width,new_height), Image.LANCZOS)
                temp.save(new_path, quality=quality)
                output_size = convert_bytes(os.path.getsize(new_path))
                output_size_list.append(os.path.getsize(new_path))
                print(f"{name}{ext} ({input_size}) -> {new_png} ({output_size})")
    return output_size_list, input_size_list


@click.command()
@click.option("--input", help="folder of images to convert")
@click.option("--output", help="folder to save converted images")
@click.option("--format", help="output format")
@click.option("--quality", help="quality of output", type=int)
@click.option("--resize", help="resize image width with fixed aspect ratio, enter as percentage", type=int, default=0)
@click.option("--recursive", help="determine if you should explore subdirectories for conversion", is_flag=True)
@click.option("--recommend", help="include to print recommended settings", is_flag=True)
def main(input = None, output = None, format = None, quality = 0, resize = None, recursive = None, recommend = None):     
    #Determining if paths exist and creating
    if (not input):
        print("no input provided")
        exit(0)
    register_heif_opener()
    if not os.path.exists(input):
        print("Invalid path")
        raise click.BadParameter("Invalid Path")
    newDir = output
    dirs = os.listdir(input)
    os.makedirs(newDir, exist_ok=True)
    validOutputFormats = [".png", ".jpeg", ".jpg"]
    if(format not in validOutputFormats):
        raise click.BadParameter("Invalid output format")
    if(recommend):
        recommended_list = analyze_image(input)
        choice = click.prompt("Use suggested? (y/n)")
        if choice == "y":
            running_osl = []
            running_isl = []
            for item in recommended_list:
                file_path = os.path.join(input, item["file"])
                output_size_list, input_size_list = convert_image(file_path, newDir, item["format"], item["quality"], item["resize"], recursive)
                running_osl += output_size_list
                running_isl += input_size_list
        else:
            running_osl, running_isl = convert_image(input, newDir, format, quality, resize, recursive)
    else:
        running_osl, running_isl = convert_image(input, newDir, format, quality, resize, recursive)
    total_conversions = len(running_osl)
    space_saved = sum(running_isl) - sum(running_osl)
    print("----------------------------------------------")
    print(f"Total conversions made: {total_conversions}")
    print(f"Total Space Saved: {convert_bytes(space_saved)}")
    
    #Checking for everything in recommended_listl, for testing purposes
    # if(recommend):
    #     for i in recommended_list:
    #         print(i)

if __name__ == "__main__":
    main()

