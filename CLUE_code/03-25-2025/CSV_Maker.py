class CSV_Maker():
    def __init__(self, file_name, data_names, mode):
        self.file_name = file_name + '(1).csv'
        self.data_names = data_names
        self.iterator = 2
        self.mode = mode

    def create_file(self):
        try:
            with open(self.file_name, self.mode) as f:
                for i in range(len(self.data_names) - 1):
                    f.write(f'{self.data_names[i]},') # Write CSV header
                f.write(f'{self.data_names[len(self.data_names) - 1]}\n')
        except OSError:
             # File already exists
            self.file_name = (self.file_name[0:self.file_name.index('(')]
                            + f'({self.iterator}).csv')
            self.iterator += 1
            self.create_file()

    def write_file(self, data):
        with open(self.file_name, "a") as f:
            for i in range(len(data) - 1):
                f.write(f'{data[i]},')
            f.write(f'{data[len(data) - 1]}\n')

    def get_file_name(self):
        return self.file_name
