import sys, pygame
import rz_jpeg_hider
pygame.init()

size = width, height = 600, 400
speed = [2, 2]
black = 0, 0, 0
argv = sys.argv
print(argv)

screen = pygame.display.set_mode(size)

# img, payload = my_extract_iamge_and_payload('test-plus-payload.jpg')
img, audio = rz_jpeg_hider.my_extract_iamge_and_payload("test-plus-payload.jpg")

with open('tmp.wav', 'wb') as sndfile:
    sndfile.write(audio)

ball = pygame.image.load("test-plus-payload.jpg")
print(dir(ball))
ballrect = ball.get_rect()

rz_jpeg_hider.my_play_sound_file('tmp.wav', True)


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