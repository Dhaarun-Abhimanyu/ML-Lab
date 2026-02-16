X = [[0,0], [0,1], [1,0], [1,1]]
Y = [0, 0, 0, 1] #and
lrate = 0.1
W = [0.1, 0.2]
b = 0.1
eps = 0.0000001

def activation(x):
    if x >= 0:
        return 1
    else:
        return 0
    
def forward(inp):
    res = b;
    for i,j in zip(inp, W):
        res += i*j
    return activation(res)

def backward(ind, out):
    global b
    delt = lrate*(Y[ind] - out)
    b += delt
    for i in range(0, len(W)):
        W[i] += delt*X[ind][i]
        
def error(ind, out):
    return (Y[ind]-out)**2        

def epoch():
    err = 0.0
    for i in range(0, len(X)):
        out = forward(X[i])
        backward(i, out)
        err += error(i, out)
    err = err / len(X)
    return err

def train():
    err = 1.0
    while err >= eps:
        err = epoch()
    print("Final weights: ", W)
    for i in range(0, len(X)):
        out = b
        for j,k in zip(X[i], W):
            out += j*k
        print(X[i][0], X[i][1], out, activation(out))

train()