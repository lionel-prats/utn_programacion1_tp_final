from modules.enemies.enemy import Enemy

class Blob(Enemy):
    def __init__(self, path_image, x, y, tile_size):
        Enemy.__init__(self, path_image, x, y)
        
        # pongo a los blobs sobre el suelo si su altura es menor a la de las baldosas
        if self.rect.height < tile_size:
            self.rect.y += abs(self.rect.height - tile_size) 
        
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        
        # movimiento blobs:
        # se moveran a derecha e izquierda durante +/-50 pixeles de su ubicacion original
        # self.move_counter ira de -51 a 50, luego de 50 vuelve a -51, en loop infinito
        # durante este tiempo los enemigos se iran moviendo en un sentido
        # cuando self.move_counter se reinicia en -51, los enemigos cambian de direccion
        self.rect.x += self.move_direction
        self.move_counter += 1 
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1