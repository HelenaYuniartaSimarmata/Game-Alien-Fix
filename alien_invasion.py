import pygame
from pygame.sprite import Group

from pengaturan import Pengaturan
from statistik_game import GameStatistik
from papan_skor import PapanSkor
from tombol import Tombol
from kapal import Kapal
import fungsi_game as gf

def Mainkan_game():
    # Inisialisasi pygame, Pengaturans, dan objek layar.
    pygame.init()
    ai_settings = Pengaturan()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Buat tombol Putar.
    play_button = Tombol(ai_settings, screen, "Play")
    
    # Buat sebuah contoh untuk menyimpan statistik permainan, dan papan skor.
    stats = GameStatistik(ai_settings)
    sb = PapanSkor(ai_settings, screen, stats)
    
    # Atur warna latar belakang.
    bg_color = (230, 230, 230)
    
    # Buatlah kapal, sekelompok peluru, dan sekelompok alien.
    ship = Kapal(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    
    # Buat armada alien.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Mulai putaran utama game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
            aliens, bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                bullets)
        
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
            bullets, play_button)

Mainkan_game()
