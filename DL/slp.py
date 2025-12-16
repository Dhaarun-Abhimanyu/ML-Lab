x = [[0,0], [0,1], [1,0], [1,1]]
y = []
w = []
lrate = 0.1

def inp():
    fn = input('Enter and (or) or: ')
    if fn != 'and' and fn != 'or':
        return 0
    for i in x:
        if fn == 'and':
            y.append(i[0] & i[1])
        elif fn == 'or':
            y.append(i[0] | i[1])
    
    temp = list(map(float, input('Enter 3 weights: ').split(' ')))
    w.extend(temp)
    return 1

def activation(out):
    #>=0: 1, else 0
    if out >= 0:
        return 1
    else:
        return 0

def test():
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

def forward(curr):
    res = w[0]
    for i,j in zip(curr, w[1:]):
        res += i*j
    return activation(res)

def backward(curr, target, output):
    delt = lrate * (target - output)
    w[0] += delt
    for i in range(0,2):
        w[i+1] += delt*curr[i]

def epoch():
    for i in range(0,len(x)):
        output = forward(x[i])
        backward(x[i], y[i], output)

def train():
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