import os
import time
import wave
import pygame
import sounddevice as sd
from multiprocessing import Process
from scipy.io.wavfile import write
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from PIL import ImageTk


IMAGEFILE = 'daisy.jpeg'
PROGRESSBARCOUNTER = 5


def my_rec_sound(_dur):
    _sample_rate = 22050
    my_rec = sd.rec(int(_sample_rate * _dur),
                    samplerate=_sample_rate,
                    channels=1,
                    dtype='int16')
    while sd.wait():
        my_num.after(250)
    print(f"got {len(my_rec)} bytes of data")
    return my_rec


def my_write_sound(_data, _file):
    """

    :param _data: the sound samples
    :param _file: the file to write to as wav file
    :return:
    """
    write(_file, 22050, _data)


# def my_play_sound(_sound_samples, _sample_rate=22050):
#     sd.play(_sound_samples, _sample_rate)
#     while sd.wait():
#         print("playing")
#         my_num.after(250)


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
    if not _bg:
        while pygame.mixer.music.get_busy():
            print('sleeping')
            time.sleep(1)


def test_my_get_wav_data_from_file():
    assert my_get_wav_data_from_file('testfile.wav') is not None


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
        print(f"End Tag Location = {myendtagloc}")
        # payload is after the end tag
        my_extra_payload = mydata[myendtagloc + 2:]
        # image (pic_data) is everything up to the end tag
        my_pic_data = mydata[:myendtagloc]
        # print(f"my_extra_payload = {str(my_extra_payload)}")
        #
        # we only need the payload, return it
    return my_pic_data, my_extra_payload


def test_my_add_payload_to_jpg():
    assert my_add_payload_to_jpg("test", IMAGEFILE)


def is_valid_jpeg(_filename=IMAGEFILE):
    _orig_jpeg = False
    _tagged_jpeg = False
    _base = _filename.split(".")[0]
    _extension = _filename.split(".")[-1]
    with open(_filename, 'rb') as ifile:
        img_data = ifile.read()
    #
    # check for the tag at eof
    #
    _endtag = img_data[-2:]
    print(f"Img Tag = {_endtag}")
    if _endtag == b'\xff\xd9':
        print("Original JPEG")
        _orig_jpeg = True
    _tagloc = img_data.find(b'\xff\xd9')
    if _tagloc > 0:
        print(f"Tag Location = {_tagloc}.  Len = {len(img_data)}")
        if _tagloc != (len(img_data) - 2):
            _tagged_jpeg = True
    return _orig_jpeg, _tagged_jpeg


def my_add_payload_to_jpg(_payload, _filename=IMAGEFILE):
    """

    will add text or bytes (e.g. audio) to end of jpeg file

    :param _payload:
    :param _filename:
    :return:
    """
    _base = _filename.split(".")[0]
    _extension = _filename.split(".")[-1]
    _is_valid, _is_tagged = is_valid_jpeg(_filename)
    if _is_valid:
        with open(_filename, 'rb') as ifile:
            img_data = ifile.read()
        #
        # check for the tag at eof
        #
        _tag = img_data[-2:]
        print(f"Img Tag = {_tag}")
        if _tag == b'\xff\xd9':
            print("File is JPEG File.  Processing")
            with open(f"{_base}-plus-payload.{_extension}", 'wb') as ofile:
                if type(_payload) == str:
                    my_combined_data = img_data + bytes(_payload, 'utf-8')
                else:
                    my_combined_data = img_data + _payload
                ofile.write(my_combined_data)
            return True


def my_rec_sound_file(_filename, _duration):
    _samples = my_rec_sound(_duration)
    my_write_sound(_samples, _filename)


def my_do_payload_process(_jpegfile: str):
    my_rec_sound_file('recording.wav', 5)
    with open('recording.wav', 'rb') as ifile:
        my_audio_data = ifile.read()
    my_add_payload_to_jpg(my_audio_data, _jpegfile)


def my_hider():
    global PROGRESSBARCOUNTER
    _base = IMAGEFILE.split(".")[0]
    _extension = IMAGEFILE.split(".")[-1]
    my_file = f'{_base}-plus-payload.{_extension}'
    #
    # remove the annotated jpeg file if it exists
    #
    if os.path.exists(my_file):
        try:
            os.remove(my_file)
            print(f"Removed {my_file}")
        except Exception as _e:
            print(f"exception {_e} attempting to remove {my_file}")
    #
    # ok, now record in the background
    #
    my_rec_process = Process(target=my_do_payload_process, args=(IMAGEFILE,))
    my_rec_process.start()
    my_counter = 5
    while my_rec_process.is_alive():
        my_num.after(1000)
        # print(f"Countdown {my_counter} seconds left!")
        my_bar.step(-1)
        my_counter -= 1
        my_num.configure(text=my_counter)
        my_num.text = my_counter
        my_num.update()
    print("done")


def my_playit():
    _base = IMAGEFILE.split(".")[0]
    _extension = IMAGEFILE.split(".")[-1]
    img, audio = my_extract_iamge_and_payload(f"{_base}-plus-payload.{_extension}")  # extracts to tmp.wav
    with open('tmp.wav', 'wb') as sndfile:
        sndfile.write(audio)
    # ball = pygame.image.load("test-plus-payload.jpg")
    # ballrect = ball.get_rect()
    # my_play_sound_file("tmp.wav", False)
    my_play_process = Process(target=my_play_sound_file, args=('tmp.wav', True,))
    my_play_process.run()


def my_img_stats(_img):
    ht = _img.height()
    wt = _img.width()
    print(f"Image {_img} height = {ht}, width = {wt}")


def my_change_photo():
    global IMAGEFILE, PROGRESSBARCOUNTER
    my_nam = fd.askopenfilename()
    IMAGEFILE = my_nam
    print(my_nam)
    _is_valid, _is_tagged = is_valid_jpeg(my_nam)
    if _is_valid:
        my_new_img = ImageTk.PhotoImage(file=my_nam)
        my_img_stats(my_new_img)
        my_image_label.config(image=my_new_img)
        my_image_label.image = my_new_img
        my_image_text.config(text=f"Image: {IMAGEFILE}")
        my_num.config(text='5')
        my_num.text = '5'

        # PROGRESSBARCOUNTER = 5

        my_bar.config(value=5)
        my_bar.value = 5
        _msg = "Good JPEG.  Able to Process"
        my_msg_label.config(text=_msg)
        my_msg_label.config(fg='black', bg='white')
        print(_msg)
    else:
        _msg = f"Can only process jpeg files.  Can't process {my_nam}"
        my_msg_label.config(text=_msg)
        my_msg_label.config(fg='red', bg='white')
        print(_msg)


"""
    panel.configure(image=img2)
    panel.image = img2
"""
if __name__ == "__main__":
    root = tk.Tk()
    root.title("JPEG Annotator - Add your audio to JPEGs")
    root.geometry('640x1200')
    my_lbl = tk.Label(root, text="JPEG Hider!!!")
    my_lbl.pack()


    my_img = ImageTk.PhotoImage(file=IMAGEFILE)

    my_img_stats(my_img)

    my_image_label = tk.Label(root, image=my_img)
    my_image_label.pack()
    my_image_text = tk.Label(root, text=f"Image: {IMAGEFILE}")
    my_image_text.pack()
    my_num = tk.Button(root, text="5")
    my_num.pack()
    my_msg_label = tk.Label(root, text="Messages")
    my_msg_label.pack()
    my_progress_frame = ttk.Frame(root)
    my_progress_frame.pack()
    PROGRESSBARCOUNTER = 5
    my_bar = ttk.Progressbar(my_progress_frame,
                             orient='horizontal',
                             value=5,
                             mode='determinate', maximum=5,
                             length=280, style='yellow.Horizontal.TProgressbar')
    my_bar.pack(side=tk.LEFT, expand=True, fill='both')
    my_file_dialog = tk.Button(root, text="Choose File", command=my_change_photo)
    my_file_dialog.pack()
    my_btn = tk.Button(root, text="Record", command=my_hider)
    my_btn.pack()
    my_quit = tk.Button(root, text="Play", command=my_playit)
    my_quit.pack()
    my_stop = tk.Button(root, text="Stop", command=pygame.init)
    my_stop.pack()
    my_quit2 = tk.Button(root, text="Quit", command=root.destroy)
    my_quit2.pack()
    root.mainloop()


