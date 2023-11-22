from modules.enemies.enemy import Enemy

class Blob(Enemy):
    def __init__(self, image, x, y):
        Enemy.__init__(self, image, x, y)
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        
        self.rect.x += self.move_direction

        # bloque para el movimiento de los enemigos
        # se moveran a derecha e izquierda durante +/-50 pixeles de su ubicacion original
        # self.move_counter ira de -51 a 50, luego de 50 vuelve a -51, en loop infinito
        # durante este tiempo los enemigos se iran moviendo en un sentido
        # cuando self.move_counter se reinicia en -51, los enemigos cambian de direccion
        # sib abs() aparentemente funciona igual
        self.move_counter += 1 
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1