class Detect_Max():
    def __init__(self, name, threshold=5):
            self.max_num = (-1, -1)
            self.previous_num = -1
            self.threshold = threshold
            self.name = name

    def update(self, nums):
        if self.previous_num != -1:
            if self.previous_num - nums[0] > self.threshold:
                return True
        if nums[0] > self.max_num[0]:
            self.max_num = nums

        self.previous_num = nums[0]
        return False

    def get_max(self):
        return self.max_num

    def write_max(self, file_name):
        with open(file_name, 'r') as file:
            rows = [line.strip().split(',') for line in file.readlines()]

        rows[0].append(self.name)
        rows[0].append(f'{self.name} time')
        rows[1].append(str(self.max_num[0]))
        rows[1].append(str(self.max_num[1]))

        with open(file_name, 'w') as file:
            file.write("\n".join(",".join(row) for row in rows))
