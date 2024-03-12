# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/03_backpropagation.ipynb.

# %% auto 0
__all__ = ['lin', 'glorot_init', 'relu', 'kaiming_init', 'mse_func']

# %% ../notebooks/03_backpropagation.ipynb 4
def lin(x, w, b):
    """ Linear layer y=w@x+b"""
    return x @ w + b

# %% ../notebooks/03_backpropagation.ipynb 20
def glorot_init(nof_inputs):
    """
    Glorot initializer.
    """
    return math.sqrt(1/nof_inputs)

# %% ../notebooks/03_backpropagation.ipynb 26
def relu(l):
    return l.clamp_min(0.)

# %% ../notebooks/03_backpropagation.ipynb 31
def kaiming_init(n_input):
    """ Kaiming He et al. initialization """
    return math.sqrt(2/n_input)

# %% ../notebooks/03_backpropagation.ipynb 57
def mse_func(predictions, targets):
    """ Mean Squared Error function """
    t = (predictions.squeeze() - targets).pow(2).mean()
    return t
