import random
import math

X = [[0,0], [0,1], [1,0], [1,1]]
H = [0.0, 0.0]
Y = [0, 1, 1, 0]
y = [0, 0, 0, 0]
W = []
bW = []
V = []
bV = 0.0
lrate = 0.1
eps = 0.1

def inp():
    global W, bW, V, bV
    for i in range(0,2):
        temp = []
        for j in range(0,2):
            temp.append(random.uniform(-1, 1))
        W.append(temp)
    for i in range(0,2):
        bW.append(random.uniform(-1, 1))
        V.append(random.uniform(-1, 1))
    bV = random.uniform(-1, 1)
    
def activation(x):
    if x < -100:
        return 0.0
    return 1 / (1 + math.exp(-x))
    
def layer1(ind):
    global H
    for i in range(0,2):
        H[i] = activation(bW[i] + W[i][0]*X[ind][0] + W[i][1]*X[ind][1])
        
def layer2(ind):
    global y
    y[ind] = activation(H[0]*V[0] + H[1]*V[1] + bV)
    
def forward(ind):
    layer1(ind)
    layer2(ind)
    
def outErr(ind):
    return -2.0*(Y[ind] - y[ind])*y[ind]*(1-y[ind])

def hiddenErr(dout):
    return [dout*V[0]*H[0]*(1-H[0]), dout*V[1]*H[1]*(1-H[1])]

def outUpdate(dout):
    global bV
    V[0] = V[0] - dout*lrate*H[0]
    V[1] = V[1] - dout*lrate*H[1]
    bV = bV - dout*lrate
    
def hiddenUpdate(dh, ind):
    global bW
    for i in range(0,2):
        bW[i] = bW[i] - dh[i]*lrate
        for j in range(0,2):
            W[i][j] = W[i][j] - lrate*dh[j]*X[ind][i]
            
def backward(ind):
    dout = outErr(ind)
    dh = hiddenErr(dout)
    outUpdate(dout)
    hiddenUpdate(dh, ind)
    
def error(ind):
    return -(Y[ind]*math.log(y[ind]) + (1-Y[ind])*math.log(y[ind]))

def epoch():
    err = 0
    for i in range(0,4):
        forward(i)
        backward(i)
        err += error(i)
    return err/len(X)

def train():
    inp()
    err = 1.0
    i = 0
    while err > eps and i <= 100000:
        err = epoch()
        i+=1
    print('Final weights & values:', W)
    for i in range(0,4):
        print(X[i][0], X[i][1], y[i])

train()
    