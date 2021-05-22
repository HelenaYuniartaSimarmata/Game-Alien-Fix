import pygame
from pygame.sprite import Sprite

class peluru(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object, at the ship's current position."""
        super(peluru, self).__init__()
        self.screen = screen

        # Buat kotak peluru di (0, 0), lalu setel posisi yang benar.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        #Simpan nilai desimal untuk posisi peluru.
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen."""

        # Perbarui posisi desimal poin.
        self.y -= self.speed_factor
        # Perbarui posisi persegi.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        
        pygame.draw.rect(self.screen, self.color, self.rect)
