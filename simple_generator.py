
def gen():
    n_max = 100
    n = 0
    while n < n_max:
        yield n, n+1
        n += 1

g = gen()

for i in range(4):
    x,y = next(g)
    print("x: ",x, " y: ",y)
