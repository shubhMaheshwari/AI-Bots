from __future__ import division

import json

def num_board(board):
    new_board = []
    for x in board:
        row = []
        for y in x:
            if y == 'x':
                row.append(1)
            elif y == 'o':
                row.append(-1)
            elif y == '-':
                row.append(0)
            else:
                print("Error:",y)
        new_board.append(row)
    return new_board


with open('simple_game.json') as f:
    data = json.load(f)

saitama = []

for game in data:    
    perfect = [] 
    for x in reversed(game):
        perfect_dict = {}
        if x['WINNER'] == 'P1':
            perfect_dict['y'] = float(1.0)
        elif x['WINNER'] == 'P2':
            perfect_dict['y'] = -float(1.0)
        elif x['WINNER'] == 'NONE':
            break
        else:               
            perfect_dict['y'] = float(float(perfect[-1]['y'])/2.0)
        
        perfect_dict['board'] = num_board(x['board'])
        perfect.append(perfect_dict)
    saitama.append(perfect)
 
# print(saitama)

import numpy as np 

def forward_pass(X,W):
    y = np.sum(np.multiply(X,W))
    return y       


def loss(x,y_pred,y,W):
    

    loss = 0.5*np.sum((y - y_pred)**2)/y_pred.size

    x = np.reshape(x,(x.shape[0],np.prod(x.shape[1:])))

    dW = np.zeros_like(W)
    dW = (x.T.dot(y_pred - y))/x.shape[0]

    dW = np.reshape(dW, W.shape)

    return loss,dW



import matplotlib.pyplot as plt

def train(X,lr=1e-1,batch_size=200,epoch=100):
    W = np.random.rand(4,4)*2

    losses = []    
    y = []
    x = []
    for game in X:
        for stage in game:
            y.append(stage['y'])
            x.append(stage['board'])
    
    y = np.array(y)
    x = np.array(x)

    num_train = x.shape[0]

    for i in range(epoch):
        random_list = np.random.randint(num_train, size = batch_size)
        x_batch = x[random_list]
        y_batch = y[random_list]

        y_pred = forward_pass(x_batch, W)
        loss_batch ,dW = loss(x_batch,y_pred,y_batch,W)
        losses.append(loss_batch)

        W = W - lr*dW

        print('iteration %d / %d: loss %f' % (i, epoch, loss_batch))

    # plt.plot(losses)
    # plt.show()
    print(W)
    # plt.close()
    return W

W = train(saitama,lr=1e-3,batch_size=100,epoch=10)

for x in saitama[0]:
    print(x['board'])
    print(forward_pass(x['board'],W),x['y'])


# Failure 

# Now we will implement using sklearn

from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

x = []
y = []
for game in saitama:
    for stage in game:
        y.append(stage['y'])
        x.append(stage['board'])
    
y = np.array(y)
x = np.array(x)

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2, random_state = 4)
x_train = np.reshape(x_train,(x_train.shape[0],np.prod(x_train.shape[1:])))
x_test = np.reshape(x_test,(x_test.shape[0],np.prod(x_test.shape[1:])))

# nn = MLPRegressor(hidden_layer_sizes=(16,16),learning_rate_init=1e-2,random_state=34)
# losses = []
# for x in range(20):
#     nn.fit(x_train,y_train)
#     losses.append(nn.score(x_test,y_test))

# plt.plot(losses)
# plt.show()

# def xxx(i):
#     print(x_train[i])
#     print(y_train[i])
#     print(nn.predict(x_train[i]))
