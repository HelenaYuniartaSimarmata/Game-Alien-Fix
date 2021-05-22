import sys
from time import sleep

import pygame

from peluru import peluru
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """ Merrspon ketika keyboard ditekan"""

    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        tembak_peluru(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event, ship):
    """merespon ketika tombol kanan atau kiri ditekan."""

    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets):
    """merespon ketika keyboard atau mouse ditekan"""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cek_tombol_play(ai_settings, screen, stats, sb, play_button,
                ship, aliens, bullets, mouse_x, mouse_y)
            
def cek_tombol_play(ai_settings, screen, stats, sb, play_button, ship,            #BENI
        aliens, bullets, mouse_x, mouse_y):
    """Memulai game ketika user mengklik tombol start"""
    
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Setel ulang pengaturan game.
        ai_settings.initialize_dynamic_settings()
        
        # Sembunyikan kursor mouse.
        pygame.mouse.set_visible(False)
        
        # Setel ulang statistik permainan.
        stats.reset_stats()
        stats.game_active = True
        
        # Setel ulang gambar papan skor.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        # Kosongkan daftar alien dan peluru.
        aliens.empty()
        bullets.empty()
        
        # Buat armada baru dan pusatkan kapal.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def tembak_peluru(ai_settings, screen, ship, bullets):
    """Fungsi untuk menjalankan program supaya ship bisa menembak."""
   
    # Buat poin baru, tambahkan ke grup poin.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = peluru(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
        play_button):
    """Mengupdate tampilan layar"""
    # Gambar ulang layar, masing-masing melewati loop.
    screen.fill(ai_settings.bg_color)
    
    # Gambar ulang semua peluru, di belakang kapal dan alien.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    # Gambarkan informasi skor.
    sb.show_score()
    
    # Gambar tombol putar jika game tidak aktif.
    if not stats.game_active:
        play_button.draw_button()

    # Jadikan layar yang paling baru digambar terlihat.
    pygame.display.flip()
    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Mengupdate tampilan dari tembakan/bullet"""
    # Perbarui posisi poin.
    bullets.update()

    # Singkirkan peluru yang hilang.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets)
        
def cek_high_score(stats, sb):
    """mengecek apakah ada skor tertinggi baru"""                      #HELENA
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
            
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets):
    """merespon hasil tembakan pesawat terhadap alien"""

    # Singkirkan semua peluru dan alien yang bertabrakan.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        cek_high_score(stats, sb)
    
    if len(aliens) == 0:
        # Jika seluruh armada hancur, mulailah level baru.
        bullets.empty()
        ai_settings.increase_speed()
        
        # Tingkatkan level.
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)
    
def check_fleet_edges(ai_settings, aliens):
    """membuat batasan pergerakan pada setiap alien di bagian pojok layar"""
    for alien in aliens.sprites():
        if alien.cek_batas():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    """merubah arah dari alien"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):             #UNI
    """merespon ketika pesawat tertabrak alien"""

    if stats.ships_left > 0:
        # Kapal pengurangan pergi.
        stats.ships_left -= 1
        
        # Perbarui papan skor.
        sb.prep_ships()
        
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
    # Kosongkan daftar alien dan peluru.
    aliens.empty()
    bullets.empty()
    
    # Buat armada baru, dan pusatkan kapal.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    
    # Berhenti sebentar.
    sleep(0.5)
    
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,               
        bullets):
    """mengecek ketika sudah ada alien yang sudah mencapai bagian bawah"""

    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Perlakukan ini sama seperti jika kapal tertabrak.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
            
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):                  
    """mengakses perubahan keadaan pada alien
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Cari alien memukul bagian bawah layar.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

    #menjelaskan mengenai keseluruhan aksi pada alien
            
def get_number_aliens_x(ai_settings, alien_width):
    """mendapatkan hasil yang teradi pada alien ketika game sudah dimainkan pada setiap baris."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
    
def get_number_rows(ai_settings, ship_height, alien_height):
    """menampilkan hasil yang terjadi pada alien ke layar"""
    available_space_y = (ai_settings.screen_height -
                            (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """memvisualisasikan gambar dan bentuk alien ke layar."""

    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """membuat barisan lengkap seluruh alien pada layar"""

    # Buat alien, dan temukan jumlah alien berturut-turut
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)
    
    # Buat armada alien.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)
