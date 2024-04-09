# AUTOGENERATED! DO NOT EDIT! File to edit: ../mikroml_notebooks/04_minibatch.ipynb.

# %% ../mikroml_notebooks/04_minibatch.ipynb 2
from __future__ import annotations
import torch
from torch import nn
import math

# %% auto 0
__all__ = ['accuracy', 'report', 'MLP', 'get_lin_model', 'Dataset', 'fit', 'get_dls']

# %% ../mikroml_notebooks/04_minibatch.ipynb 35
def accuracy(preds, targs) -> float:
    """ The average accuracy of the correctly predicted numbers """
    return (preds.argmax(dim=1)==targs).float().mean()

# %% ../mikroml_notebooks/04_minibatch.ipynb 37
def report(epoch:int, preds:torch.tensor, targs:torch.tensor, loss:float):
    """ Print a report """
    print(f"epoch:{epoch}\n#-------------------------#")
    print(f"accuracy:{accuracy(preds, targs).item():.3f} \t loss:{loss.item():.5f}")
    print("#=========================#")

# %% ../mikroml_notebooks/04_minibatch.ipynb 49
class MLP(nn.Module):
    """
    Simple Multi Layer Perceptron to illustrate the use of parameter. 
    A MLP has a minimum of 3 layers which makes this one the simplest MLP.
    """
    
    def __init__(self, n_in, nh, n_out):
        super().__init__()
        self.l1 = nn.Linear(n_in, nh)
        self.l2 = nn.Linear(nh, n_out)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        """ Forward pass """
        return self.l2(self.relu(self.l1(x)))

# %% ../mikroml_notebooks/04_minibatch.ipynb 84
def get_lin_model():
    """ Use PyTorch to create the smallest MLP and SGD optimizer. """
    _model = nn.Sequential(nn.Linear(m, nh), nn.ReLU(), nn.Linear(nh, c))
    _opt = optim.SGD(_model.parameters(), lr=0.5)
    return _model, _opt

# %% ../mikroml_notebooks/04_minibatch.ipynb 87
class Dataset():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, s):
        """ Slicing function: replaced slice() """
        return self.x[s], self.y[s]

# %% ../mikroml_notebooks/04_minibatch.ipynb 127
from torch.utils.data import DataLoader, SequentialSampler, RandomSampler, BatchSampler

# %% ../mikroml_notebooks/04_minibatch.ipynb 141
def fit(epochs, model, loss_func, opt, train_dl, valid_dl):
    for epoch in range(epochs):
        model.train()
        
        epoch_total_loss = 0
        nof_samples = 0
        cumulative_preds = torch.Tensor()
        cumulative_targs = torch.Tensor()
        
        for xb, yb in train_dl:
            train_preds = model(xb)
            cumulative_preds = torch.cat((cumulative_preds, train_preds))
            cumulative_targs = torch.cat((cumulative_targs, yb))
            train_loss = loss_func(train_preds, yb)
            nof_samples += 1
            epoch_total_loss += train_loss
            train_loss.backward()
            opt.step()
            opt.zero_grad()
        print("Training report")
        report(epoch, cumulative_preds, cumulative_targs, epoch_total_loss/nof_samples)
        
        model.eval()
        with torch.no_grad():
            tot_loss, tot_acc, count = 0.,0.,0
            for xb, yb in valid_dl:
                valid_preds = model(xb)
                n = len(xb)
                count += n
                tot_loss += loss_func(valid_preds, yb).item()*n # Why multiply?
                tot_acc += accuracy(valid_preds, yb)*n
        print("Validation report")
        print(f"valid accuracy: {tot_acc/count:.3}\t valid loss: {tot_loss/count:.3}\n")
    return tot_loss/count, tot_acc/count

# %% ../mikroml_notebooks/04_minibatch.ipynb 142
def get_dls(train_ds, valid_ds, bs, **kwargs):
    train_dl = DataLoader(train_ds, bs, shuffle=True, drop_last=True, num_workers=2, **kwargs)
    valid_dl = DataLoader(valid_ds, bs, shuffle=False, num_workers=2, **kwargs)
    return(train_dl, valid_dl)
