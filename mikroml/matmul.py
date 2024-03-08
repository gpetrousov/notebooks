# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/01_matmul.ipynb.

# %% auto 0
__all__ = ['chuncks']

# %% ../notebooks/01_matmul.ipynb 16
def chuncks(list_vals, step):
    """
    Is an iterator to return chuncks of list values
    """
    for i in range(0, len(list_vals), step):
        yield list_vals[i:i+step]
