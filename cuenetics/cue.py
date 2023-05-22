import pygame

class Cue():
    def __init__(self, pos):
        self.originalImage = pygame.image.load("cuenetics/assets/images/cue.png").convert_alpha() # this is the original form/image of the cue itself
        self.angle = 0
        self.image = pygame.transform.rotate(self.originalImage, self.angle) #this is the image that will be rotating
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, angle):
        self.angle = angle

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.originalImage, self.angle)
        surface.blit(self.image, 
                     (self.rect.centerx - self.image.get_width()/2,
                      self.rect.centery - self.image.get_height()/2
                      ))