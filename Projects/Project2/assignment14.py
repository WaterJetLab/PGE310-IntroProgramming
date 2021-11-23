#!/usr/bin/env python
# coding: utf-8

# # Assignment 14
# 
# I have provided a Python/NumPy implementation of a [PLU Decomposition](https://johnfoster.pge.utexas.edu/numerical-methods-book/LinearAlgebra_LU.html#Python/NumPy-implementation-of-$\mathbf{PLU}$-decomposition) in the course notes.  Because this function makes use of NumPy broadcasting, it's about as fast as they can be in Python, but this efficiency is at the expense of code readability.
# 
# We can make this function more readable and maintainable by using an object-oriented approach.  Your assignment is to complete the `LU` class below.  Specifically, you need to implement the `decomp` member function to perform the $\mathbf{PLU}$ decomposition and store the resulting matrices in the class attributes `P, L` and `U`, respectively.  
# 
# After that, implement `det` and `inverse` to compute the input matrix's determinant and inverse, respectively, with the $\mathbf{PLU}$ decomposition.  I've already implemented the forward and backward substitution methods and call them from a function called `solve`.  If the argument to `solve` is a one-dimensional NumPy array, then a single solution is returned.  However, if the input to solve is a two-dimensional NumPy array, then each *row* is interpreted as a unique right-hand side vector and a two-dimensional NumPy array is returned with each *row* being a solution vector corresponding to the row of the input argument.  **Hint**: You should be able to implement `inverse` with a single call to `solve`.
# 
# I am provided a `Matrix` class definition that has been extended from the one you implemented in [assignment12](https://github.com/PGE310-Students/assignment12).  This class is instantiated as the class attribute objects `P, L` and `U` and allows for indexing operations similar to Python lists and NumPy arrays as well as the row operation functions.  Please use this class and it's member functions to implement your functions when appropriate.  See the `forward/backward_substitution` functions for help using the class.

# In[1]:


import numpy as np

class Matrix(object):
    
    def __init__(self, array):
        
        if not isinstance(array, (list, np.ndarray)):
            raise TypeError('Input matrix must be a Python list or NumPy ndarray.')
        else:
            self.mat = np.array(array, dtype=np.double)
        
    def __str__(self):
        return str(self.mat)
    
    def __call__(self):
        return self.mat

    def __getitem__(self, key):
        return self.mat[key]
    
    def __setitem__(self, key, value):
        self.mat[key] = value
    
    def row_swap(self, i, j):
        temp_row = self.mat[j].copy()
        self.mat[j] = self.mat[i]
        self.mat[i] = temp_row
        return
    
    def row_multiply(self, i, factor):
        self.mat[i] *= factor
        return
        
    def row_combine(self, i, j, factor):
        self.mat[i] -= factor * self.mat[j]
        return


# In[2]:


class LU():
    
    def __init__(self, A):
        
        self.n = A.shape[0]
        
        #Instantiate P, L, and U as
        #Matrix objects and store them
        #as class attributes.
        self.U = Matrix(A.copy())
        self.L = Matrix(np.eye(self.n))
        self.P = Matrix(np.eye(self.n))
        
        #Perform the LU decomposition at
        #class instantiation
        self.decomp()
        
        return
    
            
    def decomp(self):
        #Perform the PLU decomposition and 
        #store the matrices P, L, and U
        #as class attributes
        
        #It might be useful to keep track
        #of the number of permutations that
        #will be performed on P
        self.number_of_permutations = 0
        
        #Loop over rows
        for i in range(self.n):
            
            #Permute rows if needed
            for k in range(i, self.n): 
                if ~np.isclose(self.U[i, i], 0.0):
                    break
                self.U.row_swap(k, k+1)
                self.P.row_swap(k, k+1)
                self.number_of_permutations += 1
                
            #Eliminate entries below i with row 
            #operations on U and #reverse the row 
            #operations to manipulate L
            for j in range(i+1, self.n):
                factor = self.U[j, i] / self.U[i, i]
                self.L[j, i] = factor
                self.U.row_combine(j, i, factor)
                
    def forward_substitution(self, b):
        
        #Permuting b consistent w/ P
        b = np.dot(self.P(), b)
    
        #Allocating space for the solution vector
        y = np.zeros_like(b, dtype=np.double);
    
        #Here we perform the forward-substitution.  
        #Initializing  with the first row.
        y[0] = b[0] / self.L[0, 0]
    
        #Looping over rows in reverse (from the bottom  up),
        #starting with the second to last row, because  the 
        #last row solve was completed in the last step.
        for i in range(1, self.n):
            y[i] = (b[i] - np.dot(self.L[i,:i], y[:i])) / self.L[i,i]
        
        return y
                
    def back_substitution(self, y):
    
        #Allocating space for the solution vector
        x = np.zeros_like(y, dtype=np.double);

        #Here we perform the back-substitution.  
        #Initializing with the last row.
        x[-1] = y[-1] / self.U[-1, -1]
    
        #Looping over rows in reverse (from the bottom up), 
        #starting with the second to last row, because the 
        #last row solve was completed in the last step.
        for i in range(self.n-2, -1, -1):
            x[i] = (y[i] - np.dot(self.U[i,i:], x[i:])) / self.U[i,i]
        
        return x
    
    def solve(self, b):
        
        #Ensure b is a NumPy array
        b = np.array(b)
        
        #If b is a single vector/array, add a
        #second dimension so that the function
        #call signature can be the same for a
        #single vector or multiple vectors
        if len(b.shape) == 1:
            b = b.reshape(1, -1)
        
        x = np.zeros_like(b, dtype=np.double)
        
        #Loop over all right-hand side vectors and 
        #store solution
        for i in range(b.shape[0]):
            y = self.forward_substitution(b[i])
            x[i] = self.back_substitution(y)
                
        if x.shape[0] == 1:
            return x[0]
        else:
            return x
    
    def inverse(self):
        n = self.U().shape[0]
        I = np.eye(n)
        #Return the inverse solution to
        #be in true matrix form
        return self.solve(I).T
    
    
    def det(self):
        if self.number_of_permutations % 2 == 0:
            return np.diagonal(self.U()).prod()
        else:
            return -np.diagonal(self.U()).prod()

