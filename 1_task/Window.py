from matplotlib import pyplot as plt

class Window:
    def __init__(self, title):
        self.title = title
        self.objects = []

    def show(self,xlabel='X-axis',ylabel='Y-axis'):
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(self.title)
        plt.show()

    def add_object(self,obj):
        self.objects.append(obj)

    def plot_objects(self):
        for obj in self.objects:
            plt.plot(obj[0], obj[1], marker='o', linestyle='None')

w = Window('1. Task')
w.add_object((50,100))
w.plot_objects()
w.show()