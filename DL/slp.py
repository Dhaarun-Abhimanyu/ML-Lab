x = [[0,0], [0,1], [1,0], [1,1]] #input
y = [] #output
w = [] #weights
lrate = 0.1 #learning rate

def inp(): #getting input
    fn = input('Enter and (or) or: ')
    for i in x:
        if fn == 'and':
            y.append(i[0] & i[1])
        elif fn == 'or':
            y.append(i[0] | i[1])
        elif fn == 'nand':
            y.append((i[0] & i[1]) ^ 1)
        elif fn == 'nor':
            y.append((i[0] | i[1]) ^ 1)
        else:
            return 0
    
    temp = list(map(float, input('Enter 3 weights: ').split(' ')))
    w.extend(temp)
    return 1

def activation(out): #returns after passing output to activaiton function
    #>=0: 1, else 0
    if out >= 0:
        return 1
    else:
        return 0

def test(): #returns 1 if targets and outputs match, else 0
    res = []
    for inp in x:
        curr = w[0]
        for i,j in zip(inp, w[1:]):
            curr += i*j
        res.append(activation(curr))
    for i,j in zip(res, y):
        if i != j:
            return 0
    return 1

def forward(curr): #forward pass
    res = w[0]
    for i,j in zip(curr, w[1:]):
        res += i*j
    return activation(res)

def backward(curr, target, output): #backward pass
    delt = lrate * (target - output)
    w[0] += delt
    for i in range(0,2):
        w[i+1] += delt*curr[i]

def epoch(): #runs one epoch (iterate over all test cases)
    for i in range(0,len(x)):
        output = forward(x[i])
        backward(x[i], y[i], output)

def train(): #runs epochs until convergence
    if inp() == 0:
        print('Error fetching inputs')
        exit(0)
    i = 1
    while(test() == 0):
        epoch()
        print('Weights after epoch',i,':',w)
        i+=1
    print('\nFinal Weights: ', w)

train()