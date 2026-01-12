import random
import math

#input & weights, biases
X = [[1,1], [0,1], [1,0], [0,0]]
Y = [0, 1, 1, 0]
W = []
bW = []
V = []
bV = 0.0
h = [0.0, 0.0]
y = [0.0, 0.0, 0.0, 0.0]

n_ = 0.1 #learning rate

def input(): #initializing random weights and biases
    global bW, V, bV
    W.append([random.uniform(-2,2), random.uniform(-2,2)])
    W.append([random.uniform(-2,2), random.uniform(-2,2)])
    bW = [random.uniform(-2,2), random.uniform(-2,2)]
    
    V = [random.uniform(-2,2), random.uniform(-2,2)]
    bV = random.uniform(-2,2)
    
def activate(x): #sigmoid
    return 1.0 / (1+math.exp(x))

def layer1(ind): #hidden layer
    for i in range(0,2):
        h[i] = activate(W[i][0]*X[ind][0] + W[i][1]*X[ind][1] + bW[i])
    
def layer2(ind): #output layer
    global y
    y[ind] = activate(V[0]*h[0] + V[1]*h[1] + bV)
    
def forward(ind):
    layer1(ind)
    layer2(ind)
    
def outerErr(ind): #Error derivative for output layer
    return -2.0*(Y[ind]-y[ind])*y[ind]*(1-y[ind])

def hiddenErr(dout): #Error derivative for hidden layer
    return [dout*V[0]*h[0]*(1-h[0]), dout*V[1]*h[1]*(1-h[1])]

def outputUpdate(dout): #update output layer weights
    V[0] = V[0] - n_*dout*h[0]
    V[1]= V[1] - n_*dout*h[1]
    
def hiddenUpdate(dh, ind): #update hidden layer weights
    for i in range(0,2):
        for j in range(0,2):
            W[i][j] = W[i][j] - n_*dh[j]*X[ind][i]
            
def backward(ind):
    dout = outerErr(ind)
    dh = hiddenErr(dout)
    outputUpdate(dout)
    hiddenUpdate(dh, ind)
    
def train():
    input()
    print('Original weights:')
    print('Output layer :',V)
    print('Hidden layer :',W)
    print('\n')
    
    for i in range(0,4): # Batch size = 1
        forward(i)
        print('Output at iter',i,': ',y)
        backward(i)
        print('Updated weights:')
        print('Output layer :',V)
        print('Hidden layer :',W)
        print('\n')
        
train()