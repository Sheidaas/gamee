class GuiAbstractObject:

    def is_clicked(self, mouse):
        area = (self.position[0] * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                self.position[1] * self.screen.engine.settings.graphic['screen']['resolution_scale'][1],
                (self.position[0] + self.position[2]) * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                (self.position[1] + self.position[3]) * self.screen.engine.settings.graphic['screen']['resolution_scale'][1] )

        if mouse[0][0] >= area[0] and mouse[0][0] <= area[2] \
            and mouse[0][1] >= area[1] and mouse[0][1] <= area[3]:
            return True
        return False

    def clicked(self, mouse):
        print('clicked')
