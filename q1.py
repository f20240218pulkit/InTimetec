
def fib(numbers):
    n1=0
    n2=1

    for number in range(numbers):
        yield n2
        n= n1 +n2
        n1=n2
        n2=n
    
    return n

print(list(fib(6)))
    