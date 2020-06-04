# Angel Villa

from PIL import Image as im
import cv2, os

# convert video to frames
def video_to_frames(video, output_dir, sample_freq):
    vidcap = cv2.VideoCapture(video)
    count = 1
    while vidcap.isOpened():
        success, image = vidcap.read()
        if success and count % (24*sample_freq) == 0:
            height, width = image.shape[:2]
            image = cv2.resize(image, None, fx=256/float(height), fy=256/float(height), interpolation=cv2.INTER_AREA)
            frame_no = str(count)
            frame_no_zero_pad = frame_no.zfill(7)
            cv2.imwrite(os.path.join(output_dir, "frame_" + frame_no_zero_pad + ".jpeg"), image)
        elif success and count % (24*sample_freq) != 0:
            pass
        else:
            break
        count += 1
    cv2.destroyAllWindows()
    vidcap.release()
        
def main():
    video = input("Video path: ")
    output_dir = input("Output path: ")
    vid = video_to_frames(video, output_dir,1)
    video_to_frames(vid, os.getcwd())
    
if __name__ == "__main__":
    main()

