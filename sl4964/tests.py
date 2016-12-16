'''
This module has all unit tests for the package.
Created on Dec 11, 2016
@author: ShashaLin
'''
import unittest
from midi_to_dataframe import *
from os import getcwd
from path_list import *
from process_master import *
from Classifier import featureExtract


class Test(unittest.TestCase):

    def setUp(self):
        self.song1path = getcwd() + '/ToClassify/ToClassify/Jem/They.mid'
        self.song2path = getcwd() + '/ToClassify/ToClassify/Mika/grace_kelly.mid'
        self.song3path = getcwd() + '/ToClassify/ToClassify/Radiohead/Creep.mid'
        self.folderpath = getcwd() + '/ToClassify'
        self.songdf1 = midi_to_dataframe(self.song1path,1).result()
        self.songfeature1 = featureExtract(self.songdf1)
    
    def test_midi2df(self):
        self.assertIsInstance(midi_to_dataframe(self.song1path,1), midi_to_dataframe)
        self.assertIsInstance(midi_to_dataframe(self.song2path,1), midi_to_dataframe)
        self.assertEqual(midi_to_dataframe(self.song3path,1).result().shape[1], 15)
    
    def test_pathlist(self):
        self.assertEqual(len(path_list(self.folderpath).result()), 34)
    
    def test_process(self):
        self.assertEqual(process_master(self.folderpath, 3).result().shape[1], 16)
    
    def test_classifier(self):
        self.assertEqual(self.songfeature1.shape[1], 5)
    
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()