import pygame
from pygame.sprite import Sprite

class Kapal(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship, and set its starting position."""
        super(Kapal, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Muat gambar kapal, dan dapatkan persegi.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Mulailah setiap kapal baru di bagian tengah bawah layar.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Simpan nilai desimal untuk pusat kapal.
        self.center = float(self.rect.centerx)
        
        # Bendera gerakan.
        self.moving_right = False
        self.moving_left = False
        
    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
        
    def update(self):
        """Update the ship's position, based on movement flags."""
        # Perbarui nilai tengah kapal, bukan persegi.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            
        # Perbarui objek persegi dari self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
