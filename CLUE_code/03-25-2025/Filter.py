class SMA:
    def __init__(self, start_value, window):
        self.start_value = start_value
        self.window = window
        self.data_values = []
        for i in range(self.window):
            self.data_values.append(start_value)

    def update(self, data):
        self.data_values.append(data)
        self.data_values.pop(0)
        avg = 0
        for x in self.data_values:
            avg += x
        return avg / self.window
