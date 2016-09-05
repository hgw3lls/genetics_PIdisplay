#!/usr/bin/python
#
# Author Ben Allen

import pygame, sys, os, math
from pygame.locals import *
import time
from os import listdir
from os.path import isfile, join
import string
import json

# Set the display to fb1 - i.e. the TFT
os.environ["SDL_FBDEV"] = "/dev/fb0"
# Remove mouse
os.environ["SDL_NOMOUSE"]="1"

SLIDES_DIR = "/var/media/current/"
LOGOS_DIR =  "/var/media/logos/topright"
DATA_DIR =  "/var/media/data/"
WEATHER_IMG = "/var/media/data/yimg/"

update_slide = 10
update_text1 = 1     
update_text2 = 1
update_logo = 60
update_weather = 900
update_stocks = 900

# Set constants
FPS=1000
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
GRAY   = (62,   62,   62)
BLUE = (  10, 48,   72)

# main game loop
def main():
    now = time.time()
    
    screen = None;

    "Ininitializes a new pygame screen using the framebuffer"
    disp_no = os.getenv("DISPLAY")
    if disp_no:
        print "I'm running under X display = {0}".format(disp_no)

    # Check which frame buffer drivers are available
    # Start with fbcon since directfb hangs with composite output
    drivers = ['fbcon', 'directfb', 'svgalib']
    found = False
    for driver in drivers:
        # Make sure that SDL_VIDEODRIVER is set
        if not os.getenv('SDL_VIDEODRIVER'):
            os.putenv('SDL_VIDEODRIVER', driver)
        try:
            print 'Driver: {0} Success.'.format(driver)
            pygame.display.init()
        except pygame.error:
            print 'Driver: {0} failed.'.format(driver)
            continue
        found = True
        break

    global FPSCLOCK, DISPLAYSURF, DISPLAY_W, DISPLAY_H
    global slide_num, last_slide, last_text1, last_text2, last_logo, line1_num, line2_num, logo_num
    global line1, line2

    load_text()
    #load_stock()
    load_weather()
    
    last_slide = now
    last_text1 = now   
    last_text2 = now
    last_logo = now

    slide_num = 0
    line1_num = 0
    line2_num = 0
    logo_num = 0

    FPSCLOCK = pygame.time.Clock()
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    #size = (1080, 720)
    DISPLAY_W = pygame.display.Info().current_w
    DISPLAY_H = pygame.display.Info().current_h

    print "Framebuffer size: %d x %d" % (size[0], size[1])
    DISPLAYSURF=pygame.display.set_mode(size, pygame.FULLSCREEN, 32)
    pygame.mouse.set_visible(0)
    pygame.font.init()

    print "Showing logo."
    dispLogo()
    pygame.display.update()

    time.sleep(2)

    print "Running main loop."

    while True:
        for event in pygame.event.get():
            if event.type ==  QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
  
        mainLoop()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        time.sleep(2)


# a funtion to do something
def dispLogo():
    DISPLAYSURF.fill(BLACK)

    logo = pygame.image.load("/var/media/logos/GGS_Case Logo Wide.png").convert()
    logo2 = pygame.transform.scale(logo, (DISPLAY_W, DISPLAY_H))
    DISPLAYSURF.blit(logo2, (0,0))

    

    # fontObj = pygame.font.Font('../fonts/TitilliumMaps26L.otf', 42)

    # textSurfaceObj = fontObj.render('Department of Genetics and Genome Sciences', True, BLACK)
    # textRectObj = textSurfaceObj.get_rect()

    # textRectObj.center = (DISPLAY_W/2,DISPLAY_H/2+20+1)
    # DISPLAYSURF.blit (textSurfaceObj, textRectObj)

    # textRectObj.center = (DISPLAY_W/2+1,DISPLAY_H/2+20-1)
    # DISPLAYSURF.blit (textSurfaceObj, textRectObj)

    # textRectObj.center = (DISPLAY_W/2+1,DISPLAY_H/2+20)
    # DISPLAYSURF.blit (textSurfaceObj, textRectObj)

    # textRectObj.center = (DISPLAY_W/2-1,DISPLAY_H/2+20)
    # DISPLAYSURF.blit (textSurfaceObj, textRectObj)

    # textSurfaceObj = fontObj.render('Department of Genetics and Genome Sciences', True, WHITE)
    # textRectObj = textSurfaceObj.get_rect()

    # textRectObj.center = (DISPLAY_W/2,DISPLAY_H/2+20)
    # DISPLAYSURF.blit (textSurfaceObj, textRectObj)

def mainLoop():
    global slide_num, last_slide, last_text1, last_text2, last_logo, line1_num, line2_num, logo_num
    global line1, line2, stock, weather
    now = time.time()
    
    DISPLAYSURF.fill(WHITE)
    #bg = pygame.image.load('/var/media/bg.jpg').convert()
    #DISPLAYSURF.blit(bg, (0,870))
    
    borderColor = (255, 255, 255)
    lineColor = (64, 64, 64)

    s1w = 1440
    s1h = 900
    so = 5
    #pygame.draw.rect(DISPLAYSURF, borderColor, (so,so,s1w,s1h), 1)
    #pygame.draw.rect(DISPLAYSURF, borderColor, (2*so+s1w,so,364,131), 1)
    pygame.draw.rect(DISPLAYSURF, BLUE, (2*so+s1w,5,1920-s1w-3*so,1920-s1w-3*so), 0)
    pygame.draw.rect(DISPLAYSURF, BLUE, (2*so+s1w,480,1920-s1w-3*so,425), 0)
    #pygame.draw.rect(DISPLAYSURF, borderColor, (2*so+s1w,510,364,364), 1)
    pygame.draw.rect(DISPLAYSURF, WHITE, (0,0,1920-1,1080-1), 1)
    pygame.draw.rect(DISPLAYSURF, BLUE, (5,s1h+2*so,1920-2*so,1080-s1h-3*so), 0)
    
    # Display Slides
    slides = [f for f in listdir(SLIDES_DIR) if isfile(join(SLIDES_DIR, f))]

    if slide_num >= len(slides):
      slide_num=0;

    slide = pygame.image.load(SLIDES_DIR+slides[slide_num]).convert()
    slide2 = pygame.transform.scale(slide, (s1w-2, s1h-2))
    DISPLAYSURF.blit(slide2, (6, 6))
    if now-last_slide > update_slide:
      last_slide = now
      slide_num = slide_num+1

    # Draw Text Ticker
    if line1_num>=len(line1):
      line1_num=0;

    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 100)
    text_surface = font.render(line1[line1_num], 
      True, (255, 255, 200))
    DISPLAYSURF.blit(text_surface, (10, 880))
    if now-last_text1 > update_text1:
      last_text1 = now
      line1_num = line1_num+1

    if line2_num>=len(line2):
      line2_num=0;

    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 70)
    text_surface = font.render(line2[line2_num], 
      True, (255, 255, 200))
    DISPLAYSURF.blit(text_surface, (10, 980))
    if now-last_text2 > update_text2:
      last_text2 = now
      line2_num = line2_num+1

    # Display Logo
    logos = [f for f in listdir(LOGOS_DIR) if isfile(join(LOGOS_DIR, f))]

    if logo_num>=len(logos):
      logo_num=0;

    logo = pygame.image.load(LOGOS_DIR+logos[logo_num]).convert()
    logo2 = pygame.transform.scale(logo, (362,129))
    DISPLAYSURF.blit(logo2, (2*so+s1w+1,so+1))
    if now-last_logo > update_logo:
       last_logo = now
       logo_num = logo_num+1
    
    # Display Stock Info
    # font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 50)
    # text_surface = font.render(stock['name'], True, (255, 255, 255), None)  # White text  
    # DISPLAYSURF.blit(text_surface, (2*so+s1w+5,515))

    # font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 30)
    # text_surface = font.render(stock['share'], True, (200, 255, 200), None)  # White text  
    # DISPLAYSURF.blit(text_surface, (2*so+s1w+5,565))

    # font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 50)
    # text_surface = font.render("" + stock['change'], True, (255, 100, 100), None)  # White text  
    # DISPLAYSURF.blit(text_surface, (2*so+s1w+5,615))

    # font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 50)
    # text_surface = font.render("Price: " + stock['price'], True, (200, 200, 200), None)  # White text  
    # DISPLAYSURF.blit(text_surface, (2*so+s1w+5,665))
 
    # font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 20)
    # text_surface = font.render("Todays High: " + stock['high'], True, (255, 200, 200), None)  # White text  
    # DISPLAYSURF.blit(text_surface, (2*so+s1w+5,735))

    # font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 20)
    # text_surface = font.render("Todays Low: " + stock['low'], True, (255, 200, 200), None)  # White text  
    # DISPLAYSURF.blit(text_surface, (2*so+s1w+5,765))

    # Display Weather
    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 50)
    text_surface = font.render(weather['location'], True, (255, 255, 255), None)  # White text  
    DISPLAYSURF.blit(text_surface, (2*so+s1w+5,145))
    
#    pygame.draw.rect(DISPLAYSURF, (255,255,255), (2*so+s1w+5,195,350,150), 0)
    if os.path.isfile(WEATHER_IMG+weather['current_conditions']['icon']+".gif"):
      icon = pygame.image.load(WEATHER_IMG+weather['current_conditions']['icon']+".gif").convert()
      DISPLAYSURF.blit(icon, (2*so+s1w+5,195))

    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 50)
    text_surface = font.render(weather['current_conditions']['temperature']+"F", True, BLACK)  # Black text 
    DISPLAYSURF.blit(text_surface, (2*so+s1w+5+100,195))

    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 30)
    text_surface = font.render(weather['current_conditions']['text'], True, GRAY) 
    DISPLAYSURF.blit(text_surface, (2*so+s1w+5,245))

    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 30)
    text_surface = font.render("Wind: " + string.lower(weather['current_conditions']['wind']['speed']) + weather['current_conditions']['wind']['text'], True, (100, 100, 100))
    DISPLAYSURF.blit(text_surface, (2*so+s1w+5,295))

#    pygame.draw.rect(DISPLAYSURF, (255,255,255), (2*so+s1w+5,350,55,55), 0)
#    pygame.draw.rect(DISPLAYSURF, (255,255,255), (2*so+s1w+5+110,350,55,55), 0)
#    pygame.draw.rect(DISPLAYSURF, (255,255,255), (2*so+s1w+5+220,350,55,55), 0)
    if os.path.isfile(WEATHER_IMG+weather['current_conditions']['icon']+".gif"):
      icon = pygame.image.load(WEATHER_IMG+weather['current_conditions']['icon']+".gif").convert()
      DISPLAYSURF.blit(icon, (2*so+s1w+5,350))
    if os.path.isfile(WEATHER_IMG+weather['forecasts'][1]['day']['icon']+".gif"):
      icon = pygame.image.load(WEATHER_IMG+weather['forecasts'][1]['day']['icon']+".gif").convert()
      DISPLAYSURF.blit(icon, (2*so+s1w+5+110,350))
    if os.path.isfile(WEATHER_IMG+weather['forecasts'][2]['day']['icon']+".gif"):
      icon = pygame.image.load(WEATHER_IMG+weather['forecasts'][2]['day']['icon']+".gif").convert()
      DISPLAYSURF.blit(icon, (2*so+s1w+5+220,350))

    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 15)
    text_surface = font.render(weather['forecasts'][0]['day_of_week'], True, (255, 255, 255), None)  # White text  
    DISPLAYSURF.blit(text_surface, (2*so+s1w+5,400))
    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 15)
    text_surface = font.render("High: " + weather['forecasts'][0]['high'], True, (255, 100, 100), None)  # White text  
    DISPLAYSURF.blit(text_surface, (2*so+s1w+5,430))
    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 15)
    text_surface = font.render("Low: " + weather['forecasts'][0]['low'], True, (100, 255, 100), None)  # White text  
    DISPLAYSURF.blit(text_surface, (2*so+s1w+5,460))

    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 15)
    text_surface = font.render(weather['forecasts'][1]['day_of_week'], True, (220, 220, 220), None)  # White text  
    DISPLAYSURF.blit(text_surface, (2*so+s1w+5+110,400))
    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 15)
    text_surface = font.render("High: " + weather['forecasts'][1]['high'], True, (255, 100, 100), None)  # White text  
    DISPLAYSURF.blit(text_surface, (2*so+s1w+5+110,430))
    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 15)
    text_surface = font.render("Low: " + weather['forecasts'][1]['low'], True, (100, 255, 100), None)  # White text  
    DISPLAYSURF.blit(text_surface, (2*so+s1w+5+110,460))

    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 15)
    text_surface = font.render(weather['forecasts'][2]['day_of_week'], True, (200, 200, 200), None)  # White text  
    DISPLAYSURF.blit(text_surface, (2*so+s1w+5+220,400))
    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 15)
    text_surface = font.render("High: " + weather['forecasts'][2]['high'], True, (255, 100, 100), None)  # White text  
    DISPLAYSURF.blit(text_surface, (2*so+s1w+5+220,430))
    font = pygame.font.Font("../fonts/TitilliumTitle12.otf", 15)
    text_surface = font.render("Low: " + weather['forecasts'][2]['low'], True, (100, 255, 100), None)  # White text  
    DISPLAYSURF.blit(text_surface, (2*so+s1w+5+220,460))

    print "."

def load_text():
    global line1, line2
    line1 = [line.rstrip('\n') for line in open(DATA_DIR+"line1.txt")]
    line2 = [line.rstrip('\n') for line in open(DATA_DIR+"line2.txt")]

def load_stock():
    global stock
    with open(DATA_DIR+'stock.json', 'r') as f:
      stock = json.load(f)

def load_weather():
    global weather
    with open(DATA_DIR+'weather.json', 'r') as f:
      weather = json.load(f)

# Run Main Function
if __name__ == '__main__':
    main()


