'''
Created on Dec 16, 2016

@author: Kate Wu
'''
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def visual_Vel(df, genre):

    fig = plt.figure(figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k').gca(projection='3d')
    
    
    composer_vel = df['Velocity']
    composer_note = df['Note']
    xs = np.random.choice(composer_vel,1000)
    ys = np.random.choice(composer_note,1000)
    a = pd.DataFrame(xs) #for index for the x axis
    fig.set_xlabel('Time Sequence')
    fig.set_ylabel('Velocity (volume of notes)')
    fig.set_zlabel('Pitch (notes)')
    fig.scatter(a.index, xs, ys)
    if genre == 1:
        
        plt.title('The song you picked has a Jazzy style', fontsize=20)
    else:
        
        plt.title('The song you picked has a Classical style', fontsize=20)
    plt.show()

