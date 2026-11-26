def indexed_values(items):
    result = []

    for index in range(len(items)):
        value = items[index]
        result.append((index, value))

    return result


numbers = [2, 3, 4, 5, 6]
print(indexed_values(numbers))

def indexed_values(items):
    return list(enumerate(items))


numbers = [2, 3, 4, 5, 6]
print(indexed_values(numbers))