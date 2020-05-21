#!/usr/bin/env python
# coding: utf-8

# Implement image lossy compresssion/decompression method using DCT (JPEG standard). 
# 
# Evaluate the image quality (using both objective and subjective criteria) 
# 
# and processing time for different compression ratio.

# In[1]:


def dct_coeff():
    T = np.zeros([8,8])
    for i in range(8):
        for j in range(8):
            if i==0:
                T[i,j] = 1/np.sqrt(8)
            elif i>0:
                T[i,j] = np.sqrt(2/8)*np.cos((2*j+1)*i*np.pi/16)
    return T


# In[2]:


def quantization_level(n):
    Q50 = np.zeros([8,8])

    Q50 = np.array([[16, 11, 10, 16, 24, 40, 52, 61],
               [12, 12, 14, 19, 26, 58, 60, 55],
               [14, 13, 16, 24, 40, 57, 69, 56],
               [14, 17, 22, 29, 51, 87, 80, 62],
               [18, 22, 37, 56, 68, 109, 103, 77],
               [24, 35, 55, 64, 81, 104, 113, 92],
               [49, 64, 78, 87, 103, 121, 120, 101],
               [72, 92, 95, 98, 112, 100, 103, 99]])

    Q = np.zeros([8,8])
    for i in range(8):
        for j in range(8):
            if n>50:
                Q[i,j]= min(np.round((100-n)/50*Q50[i,j]),255)
            else:
                Q[i,j]= min(np.round(50/n *Q50[i,j]),255)
    return Q


# In[3]:


def dct(M,T,T_prime):
    tmp = np.zeros(M.shape)
    mask = np.zeros([8,8])
    for i in range(M.shape[0]//8):
        for j in range(M.shape[1]//8):
            mask = M[8*i:8*i+8,8*j:8*j+8]
            tmp[8*i:8*i+8,8*j:8*j+8] = T @ mask @ T_prime
            
    return (tmp)


# In[4]:


def quantiz_div(a,b):
    tmp = np.zeros(a.shape)
    for i in range(8):
        for j in range(8):
            tmp[i,j] = np.round(a[i,j]/b[i,j])
    return tmp


# In[5]:


def quantiz(D,Q):
    tmp = np.zeros(D.shape)
    mask = np.zeros([8,8])
    for i in range(D.shape[0]//8):
        for j in range(D.shape[1]//8):
            mask = quantiz_div(D[8*i:8*i+8,8*j:8*j+8],Q)
            tmp[8*i:8*i+8,8*j:8*j+8] = mask
    return (tmp)


# In[6]:


def decompress_mul(a,b):
    tmp = np.zeros(a.shape)
    for i in range(8):
        for j in range(8):
            tmp[i,j] = a[i,j]*b[i,j]
    return tmp


# In[7]:


def decompress(C,Q,T,T_prime):
    R = np.zeros(C.shape) 
    mask = np.zeros([8,8])
    for i in range(C.shape[0]//8):
        for j in range(C.shape[1]//8):
            mask = decompress_mul(C[8*i:8*i+8,8*j:8*j+8],Q)
            R[8*i:8*i+8,8*j:8*j+8] = mask
    
    N = np.zeros(C.shape)
    
    for i in range(R.shape[0]//8):
        for j in range(R.shape[1]//8):
            mask = T_prime @ R[8*i:8*i+8,8*j:8*j+8] @ T
            N[8*i:8*i+8,8*j:8*j+8] = np.round(mask) + 128*np.ones([8,8])
    
    return N


# In[8]:


def Compress_img(file,level):

    I = cv2.imread(file)
    
    B, G, R = cv2.split(I)
    
    H = I.shape[0]  
    W = I.shape[1]  
    
    print("Image size: ",I.shape)

    B = B - 128*np.ones([H,W])
    G = G - 128*np.ones([H,W])
    R = R - 128*np.ones([H,W])
    
    T = dct_coeff()
    T_prime = inv(T)
    Q = quantization_level(level)
    
    D_R = dct(R,T,T_prime)
    D_G = dct(G,T,T_prime)
    D_B = dct(B,T,T_prime)

    tmp = cv2.merge((D_B, D_G, D_R))

    cv2.imwrite('DCT_'+str(level)+'.jpg',tmp)
    
    C_R = quantiz(D_R,Q)
    C_R[C_R==0] = 0
    C_G = quantiz(D_G,Q)
    C_G[C_G==0] = 0
    C_B = quantiz(D_B,Q)
    C_B[C_B==0] = 0
    
    tmp = cv2.merge((C_B,C_G,C_R))

    cv2.imwrite('After_Quantiz_'+str(level)+'.jpg',tmp)
    return C_B,C_G,C_R,Q,T,T_prime
    


# In[9]:


def Decompress_img(C_B,C_G,C_R,Q,T,T_prime,fileout):
    N_R = decompress(C_R,Q,T,T_prime)
    N_G = decompress(C_G,Q,T,T_prime)
    N_B = decompress(C_B,Q,T,T_prime)

    N_I = cv2.merge((N_B, N_G, N_R))
    cv2.imwrite(fileout,N_I)


# In[10]:


def Evaluate(file,fileout):
    
    I = cv2.imread(file)
    
    I1 = cv2.imread(fileout)
    
    m,n,k = I1.shape
    
    rms = np.sqrt(np.sum(np.square(I1-I)))/(m*n)
    
    snr = np.sum(np.square(I1))/np.sum(np.square(I1-I))

    return rms, snr


# In[12]:


import numpy as np
import cv2
from matplotlib import pyplot as plt
from numpy.linalg import inv
import time
import sys

file = sys.argv[1]
level = int(sys.argv[2])
print("Filename: ",file)
print("Level of compression: ",level)
fileout = str("Decompress_" + str(level) + ".jpg")

print("Compressing....")
start = time.time()
C_B,C_G,C_R,Q,T,T_prime = Compress_img(file,level)
time_comp = time.time()
print("Compression Time: ",np.round(time_comp - start,1)," sec")

print("Decompressing...")
Decompress_img(C_B,C_G,C_R,Q,T,T_prime,fileout)
time_decomp = time.time()

print("Decompression Time: ",np.round(time_decomp - time_comp,1)," sec")

end = time.time()
print("Total: ",np.round(end - start,1)," sec")
rms, snr = Evaluate(file,fileout)
print("RMS: ",np.round(rms,4))
print("SNR: ",np.round(snr,4))