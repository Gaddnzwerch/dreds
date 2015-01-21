import gc

class Nutrition:
    def get_consumed(self):
        self.add_message('The ' + type(self).__name__ + ' ' + repr(self) + ' is being consumed ')
        self.active = False
