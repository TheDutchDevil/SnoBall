#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 15:06:53 2017

@author: hildeweerts
"""
""" Comparing matrices """
#%%
working_dir = '/Users/hildeweerts/downloads/'
os.chdir(working_dir)

import numpy as np
cosine_sim = np.load('cosine_similarity1.npy')

#%%
cosine_sim2 = cosine_sim[0:-1, 0:-1]
cocitation_matrix2 = cocitation_matrix[0:-1, 0:-1]

#%%
print("\nIncluding all elements:")
print("Standard deviation cocitation matrix")
print(np.std(cocitation_matrix2.flatten()))
print("Mean cocitation matrix")
print(np.mean(cocitation_matrix2.flatten()))
print("Standard deviation cosine similarity matrix")
print(np.std(cosine_sim2.flatten()))
print("Mean cosine similarity matrix")
print(np.mean(cosine_sim2.flatten()))
print("Correlation")
correlation = np.corrcoef(cocitation_matrix2.flatten(), cosine_sim2.flatten())
print(correlation[0,1])

nonzeros = np.nonzero(cocitation_matrix2.flatten())[0]
nonzero_coc = cocitation_matrix2.flatten()[nonzeros]
nonzero_cos = cosine_sim.flatten()[nonzeros]

print("\n Only including nonzero cocitation elements:")
print("Standard deviation cocitation matrix")
print(np.std(nonzero_coc))
print("Mean  cocitation matrix")
print(np.mean(nonzero_coc))
print("Standard deviation cosine similarity matrix")
print(np.std(nonzero_cos))
print("Mean cosine similarity matrix")
print(np.mean(nonzero_cos))
print("Correlation")
correlation = np.corrcoef(nonzero_coc, nonzero_cos)
print(correlation[0,1])

#%%
"""
Including all elements:
Standard deviation cocitation matrix
0.00576446643764
Mean cocitation matrix
2.78387120761e-05
Standard deviation cosine similarity matrix
0.0881481250916
Mean cosine similarity matrix
0.147719741552
Correlation
0.000527969288998

 Only including nonzero cocitation elements:
Standard deviation cocitation matrix
0.350006478499
Mean  cocitation matrix
1.08025247971
Standard deviation cosine similarity matrix
0.0905238798519
Mean cosine similarity matrix
0.141783209713
Correlation
0.0343657559557
"""