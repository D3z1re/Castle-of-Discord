class Camera:
    # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        # вычислим координату клитки, если она уехала влево за границу экрана
#        if obj.rect.x < -obj.rect.width:
#            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        # вычислим координату клитки, если она уехала вправо за границу экрана
#        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
#            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
#        obj.rect.y += self.dy
        # вычислим координату клитки, если она уехала вверх за границу экрана
#        if obj.rect.y < -obj.rect.height:
#            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        # вычислим координату клитки, если она уехала вниз за границу экрана
#        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
#            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = int(-(target.rect.x + target.rect.w // 2 - WIDTH // 2) / 20)
        self.dy = int(-(target.rect.y + target.rect.h // 2 - HEIGHT // 2) / 20)


camera = Camera((level_x, level_y))