class csv:
    def __init__(self, file_name, data_names):
        self.file_name = '/' + file_name + '(1).csv'
        self.data_names = data_names
        self.iterator = 2

    def create_file(self):
        try:
            with open(self.file_name, "x") as f:
                for x in self.data_names:
                    f.write(f'{x},') # Write CSV header
                f.write('\n')
        except OSError:
            # File already exists
            self.file_name = self.file_name[0:(len(self.file_name) - len(str(self.iterator)) - 6)] + f'({self.iterator}).csv'
            self.iterator += 1
            self.create_file()

    def write_file(self, data):
        with open(self.file_name, "a") as f:
            for x in data:
                f.write(f'{x},')
            f.write('\n')
