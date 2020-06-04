# Angel Villa

from tkinter import filedialog as fd
from tkinter import *
import palette_operations as pal_op
import vid_to_frames as vid_tf
import os, time

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)        
        self.master = master
        self.palettes_dir = os.getcwd()
        self.filename = ""
        self.dir = ""
        self.sample_freq = 1
        
        # widget can take up entire window
        self.pack(fill=BOTH, expand=1)
        
        # creating buttons
        self.file_button = Button(self, text="Select video file", command=self.browse_file, width = 20, height = 2)
        self.dir_button = Button(self, text="Select target directory",
            command=self.browse_dir, width = 20, height = 2)
        self.clear_button = Button(self, text="Clear selections", command=self.clear_selections, width = 20, height = 2)
        self.vtf_button = Button(self, text="Convert video", command=self.vtf, width = 20, height = 2)
        self.palette_button = Button(self, text="Make palette", command=self.make_palette, width = 20, height = 2)
        
        # creating spinbox
        self.sample_freq_box = Spinbox(self, from_=1, to=12, state="readonly")
        
        # placing spinbox
        self.sample_freq_box.grid(row = 4, column = 0, padx=5, pady=5)
        
        # creating labels
        self.file_label_text = StringVar()
        self.file_label_text.set("None selected")
        file_label = Label(self, textvariable=self.file_label_text, wraplength=150)
        self.dir_label_text = StringVar()
        self.dir_label_text.set("None selected")
        dir_label = Label(self, textvariable=self.dir_label_text, wraplength=150)
        self.sample_freq_text = StringVar()
        self.sample_freq_text.set("Sample rate \n(seconds per frame)")
        sample_freq_label = Label(self, textvariable=self.sample_freq_text, wraplength=150)
        
        # placing buttons 
        self.file_button.grid(row = 0, column = 0, padx=5, pady=5)
        self.dir_button.grid(row = 2, column = 0, padx=5, pady=5)
        self.clear_button.grid(row = 6, column = 0, padx=5, pady=5)
        self.vtf_button.grid(row = 7, column = 0, padx=5, pady=5)
        self.palette_button.grid(row = 4, column = 1, padx=5, pady=5)
        
        # placing labels
        file_label.grid(row = 1, column = 0, padx=5, pady=5)
        dir_label.grid(row = 3, column = 0, padx=5, pady=5)
        sample_freq_label.grid(row = 5, column = 0, padx=5, pady=5)
        
        # creating dialog box
        self.dialog_box = Text(self, height = 10, width = 60, state=DISABLED)
        
        # placing dialog box
        self.dialog_box.grid(row = 8, column = 0, columnspan = 3, padx=5,pady=5)
        
    # browse for video file
    def browse_file(self):
        self.write_to_dialog_box("Selecting video file . . . \n")
        
        self.filename = fd.askopenfilename(
            initialdir = "\\",
            title = "Select file",
            filetypes = (("Video files","*.MOV;*.MP4;*.AVI;*.MKV"),("All files","*.*"))
        )
        if self.filename != "":
            head_tail = os.path.split(self.filename)
            tail = os.path.splitext(head_tail[1])
            self.file_label_text.set(tail[0])
            
            self.write_to_dialog_box("File = " + self.filename + "\n")
            
        else: 
            pass
        
    # browse for directory to place frames
    def browse_dir(self):
        self.write_to_dialog_box("Selecting directory to place frames . . . \n")
        
        self.dir = fd.askdirectory()
        self.dir_label_text.set(self.dir)
        
        if self.dir != "":
            self.write_to_dialog_box("Directory = " + self.dir + "\n")
        else:
            self.dir_label_text.set("None selected")

    # convert video to frames    
    def vtf(self):
        self.sample_freq = int(self.sample_freq_box.get())
        self.write_to_dialog_box("Converting video to frames, " + str(self.sample_freq) + " seconds per frame . . . \n")
        
        if self.dir != "":
            vid_tf.video_to_frames(self.filename, self.dir, self.sample_freq)
        else:
            head_tail = os.path.split(self.filename)
            tail = os.path.splitext(head_tail[1])
            self.dir = self.palettes_dir + "\\Frames\\" + tail[0]
            try:
                os.makedirs(self.dir)
                vid_tf.video_to_frames(self.filename, self.dir, self.sample_freq)
            except FileExistsError:
                vid_tf.video_to_frames(self.filename, self.dir, self.sample_freq)
                
        self.write_to_dialog_box("Done! Frames location: " + self.dir + "\n")
        
        self.dir = ""
    
    # clear all path selections
    def clear_selections(self):
        self.filename = ""
        self.dir = ""
        self.file_label_text.set("None selected")
        self.dir_label_text.set("None selected")
        self.write_to_dialog_box("Selections cleared \n")
        
    # convert frames to palette
    def make_palette(self):
        self.write_to_dialog_box("Selecting frames directory . . . \n")
        
        directory = fd.askdirectory()
        target_dir = self.palettes_dir + "\\Final Palettes\\"
        try:
            os.mkdir(target_dir)
            pal_op.frames_to_palette(directory, target_dir)
        except FileExistsError:
            pal_op.frames_to_palette(directory, target_dir)
            
        self.write_to_dialog_box("Done! Palette location: " + target_dir + "\n")
        
    def write_to_dialog_box(self, text):
        self.dialog_box.config(state=NORMAL) 
        self.dialog_box.insert("1.0", text + "\n")
        self.dialog_box.config(state=DISABLED)
        
     
def main():
    palettes_dir = os.getcwd()
    root = Tk()
    app = Window(root)
    root.wm_title("Palettes")
    root.geometry("500x460")
    root.mainloop()
    
if __name__ == "__main__":
    main()
