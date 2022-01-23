import sys, pygame, time


def my_play_sound_file(_soundfile='testfile.wav', _bg=True):
    pygame.mixer.init()
    pygame.mixer.music.load(_soundfile)
    pygame.mixer.music.play(1)
    if _bg == False:
        while pygame.mixer.music.get_busy():
            print('sleeping')
            time.sleep(1)


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


pygame.init()

size = width, height = 600, 400
speed = [2, 2]
black = 0, 0, 0
argv = sys.argv
my_file = argv[1]



screen = pygame.display.set_mode(size)

# img, payload = my_extract_iamge_and_payload('test-plus-payload.jpg')
my_file = argv[0]
img, audio = my_extract_iamge_and_payload(my_file)

with open('tmp.wav', 'wb') as sndfile:
    sndfile.write(audio)

ball = pygame.image.load("daisy-plus-payload.jpg")
ballrect = ball.get_rect()

my_play_sound_file('tmp.wav', True)


while 1:
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