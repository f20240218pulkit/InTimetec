class ReverseIterator:
    def __init__(self, numbers):
        self.numbers = numbers
        self.index = len(numbers) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < 0:
            raise StopIteration

        value = self.numbers[self.index]
        self.index -= 1
        return value


for number in ReverseIterator([8, 4, 9]):
    print(number)