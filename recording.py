import csv

class Object_recorder:
    def __init__(self, filename):
        self.filename = filename

    def record_position(self, x, y):
        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([x, y])

