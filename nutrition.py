import gc

class Nutrition:
    def get_consumed(self):
        print('The ' , type(self).__name__ , ' ' , self , ' is being consumed ')
        self.active = False