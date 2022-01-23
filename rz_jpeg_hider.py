import os
import time
import wave
import pygame
import sys
import threading
import asyncio
import sounddevice as sd
from multiprocessing import Process
from scipy.io.wavfile import write
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

def my_rec_sound(_dur):
    _sample_rate = 22050
    my_rec = sd.rec(int(_sample_rate * _dur),
                    samplerate=_sample_rate,
                    channels=1,
                    dtype='int16')
    while sd.wait():
        time.sleep(1)
    print(f"got {len(my_rec)} bytes of data")
    return my_rec


def my_write_sound(_data, _file):
    """

    :param _data: the sound samples
    :param _file: the file to write to as wav file
    :return:
    """
    write(_file, 22050, _data)


#
# not working 10/18/21
def my_play_sound(_sound_samples, _sample_rate=22050):
    sd.play(_sound_samples, _sample_rate)
    # while sd.wait():
    #     print("playing")
    #     time.sleep(1)


def my_save_sound(_sound_samples, _filename):
    with open(_filename, 'bw') as ofile:
        ofile.write(_sound_samples)


def my_load_sound(_filename):
    with open(_filename, 'br') as ifile:
        _samples = ifile.read()
    return _samples


def my_play_sound_file(_soundfile='testfile.wav', _bg=True):
    pygame.mixer.init()
    pygame.mixer.music.load(_soundfile)
    pygame.mixer.music.play(1)
    if _bg == False:
        while pygame.mixer.music.get_busy():
            print('sleeping')
            time.sleep(1)


# def my_test_play_recorded_sound_file(_soundfile='tmp.wav'):
#     # my_data = read(_soundfile)
#     mixer.init()
#     mixer.Sound(_soundfile)
#     mixer.Sound.play(1, 5, 0)
#     while mixer.Sound.get_busy():
#         print('sleeping')
#         time.sleep(1)


def test_my_get_wav_data_from_file():
    assert my_get_wav_data_from_file('testfile.wav') != None


def my_get_wav_data_from_file(_the_file='testfile.wav'):
    with wave.open(_the_file, 'rb') as wfile:
        try:
            _rate = wfile.getframerate()
            _channels = wfile.getnchannels()
            # print(dir(wfile))
            _frames = wfile.getnframes()
            my_wave_data = wfile.readframes(_frames)
        except Exception as _e:
            print(f"{_e=}")
    return my_wave_data


def my_extract_iamge_and_payload(_the_file='ofile.jpg'):
    with open(_the_file, 'rb') as infile:
        mydata = infile.read()
        # get jpeg end tag location
        myendtagloc = mydata.find(b'\xff\xd9')
        # payload is after the end tag
        my_extra_payload = mydata[myendtagloc + 2:]
        # image (pic_data) is everything up to the end tag
        my_pic_data = mydata[:myendtagloc]
        # print(f"my_extra_payload = {str(my_extra_payload)}")
        #
        # we only need the payload, return it
    return my_pic_data, my_extra_payload


def test_my_add_payload_to_jpg():
    assert my_add_payload_to_jpg("test", 'test.jpg') == True


def my_add_payload_to_jpg(_payload, _filename='rob-deepweb.jpg'):
    with open(_filename, 'rb') as ifile:
        img_data = ifile.read()
    with open(f"{_filename.split('.')[0]}-plus-payload.jpg", 'wb') as ofile:
        if type(_payload) == str:
            my_combined_data = img_data + bytes(_payload, 'utf-8')
        else:
            my_combined_data = img_data + _payload
        ofile.write(my_combined_data)
    return True


# with open('testfile.wav', 'rb') as ifile:
#     my_audio_data = ifile.read()

# mysamples = pygame.sndarray.array()

def my_rec_sound_file(_filename, _duration):
    _samples = my_rec_sound(_duration)
    my_write_sound(_samples, _filename)


def my_do_payload_process(_jpegfile: str):
    my_rec_sound_file('recording.wav', 5)
    with open('recording.wav', 'rb') as ifile:
        my_audio_data = ifile.read()
    my_add_payload_to_jpg(my_audio_data, _jpegfile)


def my_hider():
    global root, my_num, my_counter, my_bar
    my_counter = 5
    my_file = 'test-plus-payload.jpg'
    if os.path.exists(my_file):
        my_rm = os.remove(my_file)
        if not my_rm:
            print(f"Removed {my_file}")
    my_rec_process = Process(target=my_do_payload_process, args=('test.jpg',))
    my_rec_process.start()
    while my_rec_process.is_alive():
        print(f"Countdown {my_counter} seconds left!")
        my_bar.step(-1)
        my_bar.update()
        my_counter -= 1
        time.sleep(1)


# def my_bar():
#     root = tk.Tk()
#     bp = ttk.Progressbar(root, length=300,
#                          orient=tk.HORIZONTAL)
#     bp.pack()
#     button = tk.Button(root, text="Start")
#     # self.p.grid(row=5)
#     # bp.grid(padx=10, pady=10, row=1)
#     button.pack(padx=10, pady=10)
#     root.mainloop()
#

def my_playit():
    global my_img, canvas
    pygame.init()
    size = width, height = 600, 400
    speed = [2, 2]
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)
    img, audio = my_extract_iamge_and_payload("test-plus-payload.jpg")  # extracts to tmp.wav
    # canvas.update_image(20, 20, anchor=tk.NW, image=img)
    # my_img.config(image=my_img)

    with open('tmp.wav', 'wb') as sndfile:
        sndfile.write(audio)
    ball = pygame.image.load("test-plus-payload.jpg")
    ballrect = ball.get_rect()

    # my_daisy = ImageTk.PhotoImage(file="daisy.jpeg")
    # canvas.create_image(200, 200, anchor=tk.SW, image=my_daisy)
    # my_img.config(image=my_daisy)

    my_play_process = Process(target=my_play_sound_file, args=('tmp.wav', False,))
    my_play_process.start()
    _t = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]
        screen.fill(black)
        screen.blit(ball, ballrect)
        pygame.display.flip()
        # _t += 1
        # time.sleep(.01)
        # print(_t)
        if _t > 500 or (not my_play_process.is_alive()):
            return


def main():
    global root, my_num, my_counter, my_bar, canvas, my_img
    my_counter = 5
    root = tk.Tk()
    my_lbl = tk.Label(root, text="JPEG Hider!!!")
    my_lbl.pack()
    # path = "test.jpg"
    # img = ImageTk.PhotoImage(Image.open(path))
    # my_imgfile = tk.PhotoImage(img)
    # print(tk.image_types())

    canvas = tk.Canvas(root, width=600, height=600)
    canvas.pack()
    my_img = ImageTk.PhotoImage(file="test.jpg")
    # print(dir(my_img))
    canvas.create_image(20, 20, anchor=tk.NW, image=my_img)
    # my_img = tk.Image(image=my_imgfile, imgtype='photo')
    # my_img.pack()
    my_num = tk.Button(root, text="5")
    my_num.pack()
    my_progress_frame = ttk.Frame(root)
    my_progress_frame.pack()
    my_bar = ttk.Progressbar(my_progress_frame,
                             orient='horizontal',
                             mode='determinate', maximum=5, value=5,
                             length=280, style='yellow.Horizontal.TProgressbar')
    my_bar.pack(side=tk.LEFT, expand=True, fill='both')
    my_btn = tk.Button(root, text="Record", command=my_hider)
    my_btn.pack()
    my_quit = tk.Button(root, text="Play", command=my_playit)
    my_quit.pack()
    my_stop = tk.Button(root, text="Stop", command=pygame.init())
    my_stop.pack()
    my_quit2 = tk.Button(root, text="Quit", command=root.destroy)
    my_quit2.pack()
    root.mainloop()



if __name__ == "__main__":
    # my_bar()
    main()
# if __name__ == '__main__':
#     # create root window
#     root = tk.Tk()
#     # call Main_Frame class with reference to root as top
#     Main_Frame(top=root)
