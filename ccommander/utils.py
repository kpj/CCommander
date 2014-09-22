class ConstantLengthList(list):
    def __init__(self, length):
        super(ConstantLengthList, self).__init__()
        self.length = length

    def append(self, item):
        super(ConstantLengthList, self).append(item)
        if len(self) > self.length:
            self.pop(0)

    def get_avg(self):
        if len(self) == 0:
            return 0
        return sum(self)/len(self)
