#! /usr/bin/python
import numpy as np

def rnn_cell_forward(xt, a_prev, parameters):
    Wax = parameters["Wax"]
    Waa = parameters["Waa"]
    Wya = parameters["Wya"]
    ba = parameters["ba"]
    bb = parameters["bb"]

    a_next = np.tanh(np.dot(Wax, xt) + np.dot(Waa, a_prev) + ba)
    yt_pred = softmax(np.dot(Wya, a_next) + by)

    cache = (a_next, a_prev, xt, parameters)

    return a_next, yt_pred, cache

def rnn_forward_pass(x, a0, parameters):
    caches = []

    _, m, T_x = x.shape
    n_y, n_a = parameters["Wya"].shape

    a = np.zeros((n_a, m, T_x))
    y_pred = np.zeros((n_y, m, T_x))

    a_next = a0

    for t in range(T_x):
        a_next, yt_pred, cache = rnn_cell_forward(x[:, :, t], 
a_next, parameters)
        a[:, :, t] = a_next
        yt_pred[:, :, t] = yt_pred

    caches.append(cache)
    caches = (caches, x)

    return a, y_pred, caches

def rnn_cell_backward(da_next, cache):
    (a_next, a_prev, xt, parameters) = cache
    Wax = parameters["Wax"]
    Waa = parameters["Waa"]
    Wya = parameters["Wya"]
    ba = parameters["ba"]
    bb = parameters["bb"]

    dtanh = (1 - a_next * a_next) * da_next
    dWax = np.dot(dtanh, xt.T)
    dxt = np.dot(Wax.T, dtanh)
    dWaa = np.dot(dtanh, a_prev.T)
    da_prev = np.dot(Waa.T, dtanh)
    dba = np.sum(dtanh, keepdims=True, axis=-1)

    gradients = {"dxt": dxt, "da_prev": da_prev, "dWax": dWax, "dWaa": 
dWaa, "dba": dba}

    return gradients

def rnn_backward(da, caches):
    caches, x = caches
    a1, a0, x1, parameters = caches[0]
    n_a, m, T_x = da.shape
    n_x, m = x1.shape

    dx = np.zeros((n_x, m, T_x))
    dWax = np.zeros((parameters['Wax'].shape))
    dWaa = np.zeros((parameters['Waa'].shape))
    dba = np.zeros((parameters['ba'].shape))
    da0 = np.zeros(a0.shape)
    da_prevt = np.zeros((n_a, m))

    for t in reversed(range(T_x)):
        gradients = rnn_cell_backward(da[:, :, t] + da_prevt, caches[t])
        dxt, da_prevt, dWaxt, dWaat, dbat = gradients['dxt'],
gradients['da_prev'], gradients['dWax'], gradients['dWaa'],
gradients['dba']

    dWax += dWaxt
    dWaa += dWaat
    dba += dbat
    dx[:, :, t] = dxt
    da0 = da_prevt

    gradients = {"dx": dx, "da0": da0, "dWax": dWax, "dWaa": dWaa, "dba":
dba}

    return gradients
