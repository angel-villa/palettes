# Angel Villa

import time, glob, os
from PIL import Image as im
from numpy import *

# get average color from rectangle defined by opposite corners (x1, y1) and (x2, y2)
def avg_color(image, x1, y1, x2, y2):
    pix_count = 0
    cumul_color = array([0,0,0])
    for i in range(x1, x2, int((x2-x1)/2**4.0)):
        for j in range(y1, y2, int((y2-y1)/2**4.0)):
            cumul_color += asarray(image.getpixel((i,j)))
            pix_count += 1
    avg = [int(1.0*x/pix_count) for x in cumul_color]
    return avg

# get average color from row y
def avg_color_row(image, y):
    pix_count = 0
    cumul_color = array([0,0,0])
    for i in range(1, image.width, int((image.width)/2**4.0)):
        cumul_color += asarray(image.getpixel((i,y)))
        pix_count += 1
    avg = [int(1.0*x/pix_count) for x in cumul_color]
    return avg

# convert directory of frames to palette
def frames_to_palette(frames_dir, target_dir):
    pal_height = 0
    frame_count = 0
    os.chdir(frames_dir)
    title = frames_dir.split("/")[-1]
    for infile in glob.glob("*.jpeg"):
        frame_count += 1
        if pal_height == 0:
            img = im.open(infile)
            pal_height = img.height
        else:
            continue
        
    color_array = zeros([pal_height, frame_count, 3], dtype=uint8)
    index = 0
    for infile in glob.glob("*.jpeg"):
        file, ext = os.path.splitext(infile)
        img = im.open(infile)
        for i in range(1, img.height):
            avg = avg_color_row(img, i)
            color_array[(i-1)*int(pal_height/img.height):i*int(pal_height/img.height),index] = list(avg)
        index += 1

    os.chdir(target_dir)
    pal = im.fromarray(color_array)
    pal.save(title+"_palette.jpeg")
    
def main():
    quit()
    
if __name__ == "__main__":
    main()
            

