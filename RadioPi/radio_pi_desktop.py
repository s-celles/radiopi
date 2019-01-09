import os
import time

import pygame

from controller.controller import Controller
from radiostation.radio_browser_de_api_model import RadioBrowserDeClient
from radiostation.radioservice import RadioService
from ui.mouse_device import MouseDevice
from ui.view import ImageFont, UI, FrameBuilder
from view.radio_view import Images, RadioPlayView, RadioSelectView,\
    RadioSetupView
from audio.player import Player
from network.network import NetworkService


radio_client = RadioBrowserDeClient()
radio_service = RadioService(radio_client)
audio_player = Player()
network_service = NetworkService()

#from ui.touch_device import TouchDevice
os.putenv('SDL_FBDEV', '/dev/fb1')

pygame.init()
pygame.font.init() 

screen = pygame.display.set_mode((320, 240))
pygame.display.set_caption("Radio PI")

font = ImageFont('gfx/font.png', (20, 20))
font_pushed = ImageFont('gfx/font_pushed.png', (20, 20))
font_inactive = ImageFont('gfx/font_inactive.png', (20, 20))
ui = UI(screen, 320, 240, (0, 0, 0))
images = Images(font, font, font_pushed, font_inactive)
framebuilder = FrameBuilder(
    images.label(Images.FRAME_TOP_LEFT),
    images.label(Images.FRAME_TOP_RIGHT),
    images.label(Images.FRAME_BOTTOM_LEFT),
    images.label(Images.FRAME_BOTTOM_RIGHT),
    images.label(Images.FRAME_LEFT),
    images.label(Images.FRAME_RIGHT),
    images.label(Images.FRAME_TOP),
    images.label(Images.FRAME_BOTTOM),
    20,20
    )
fonts = [
    'fonts/DejaVuSans.ttf',
    'fonts/DejaVuSans-Bold.ttf',
    'fonts/DejaVuSans-Oblique.ttf',
    'fonts/DejaVuSans-BoldOblique.ttf'    
]
sizes = [12, 16, 20, 24]
#sizes = [20, 24, 28, 36]
colors = [(255,255,255), (0,255,0)]

play_view = RadioPlayView(screen, images, framebuilder, fonts, sizes, colors)
play_view.set_size(320, 240);

select_view = RadioSelectView(screen, images, framebuilder, fonts, sizes, colors)
select_view.set_size(320, 240)

setup_view = RadioSetupView(screen, images, framebuilder, fonts, sizes, colors)
setup_view.set_size(320, 240)

ui.get_root().add(play_view)
ui.get_root().add(select_view)
ui.get_root().add(setup_view)
controller = Controller(play_view, select_view, setup_view, radio_service, audio_player, network_service)

ui.get_root().show()
ui.refresh()

input_device = MouseDevice()
pygame.mouse.set_visible(True)
#pygame.mouse.set_visible(False)
#input_device = TouchDevice()
#input_device.calibration_load('calibration.ini')

while True:
    input_device.poll(ui)
    ui.refresh()
    time.sleep(0.05)
    