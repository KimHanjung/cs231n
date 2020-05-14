from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    num_train = X.shape[0]
    num_class = W.shape[1]

    for i in range(num_train):
      scores = X[i].dot(W)
      score_max = np.max(scores)
      scores -= score_max
      loss += -scores[[y[i]]] + np.log(np.sum(np.exp(scores)))
      for j in range(num_class):
        if j == y[i]:
          dW[:,j] -= X[i]
        dW[:, j] += (np.exp(scores[j]) / np.sum(np.exp(scores))) * X[i]


    loss = loss / num_train + reg * np.sum(W*W)
    dW = dW/ num_train + reg * W
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    num_train = X.shape[0]
    num_class = W.shape[1]

    scores = X.dot(W)
    score_max = scores[np.arange(num_train), np.argmax(scores, axis=1)]
    score_max = np.reshape(score_max, (num_train, 1))
    scores -= score_max
    scores = np.exp(scores)
    loss_map = scores[np.arange(num_train), y[np.arange(num_train)]]
    sum_map = np.sum(scores, axis=1)
    loss = (np.sum(-np.log(loss_map / sum_map)) / num_train) +  reg * np.sum(W*W)

    scores = X.dot(W)
    scores = np.exp(scores)
    sum_map = np.sum(scores, axis=1)
    sum_map = np.reshape(sum_map, (num_train, 1))
    scores /= sum_map
    dW = X.T.dot(scores)
    mask = np.zeros((num_train, num_class))
    mask[np.arange(num_train), y[np.arange(num_train)]] = 1
    mask = X.T.dot(mask)
    dW -= mask
    dW = dW / num_train + reg * W
    

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
