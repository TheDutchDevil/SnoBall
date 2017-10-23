# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 16:17:22 2017

@author: s135509
"""

from sklearn.externals import joblib

author_cluster_dict = joblib.load('author_cluster_dictionary') # key is author id, 
cluster_author_dict = joblib.load('cluster_author_dictionary') # key is cluster ID

