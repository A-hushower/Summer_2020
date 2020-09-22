#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 16:03:10 2020

@author: austinhushower
"""
import torch
import os

from path_generate import audio_paths

# list of all avavilable models and pipelines
AVAILABLE = torch.hub.list('pyannote/pyannote-audio')
     
class PretrainedPipeline():
    
    def __init__(self, pipeline):
        self.set_pipeline(pipeline)
    
    def set_pipeline(self, pipeline):
        # model name verification 
        assert pipeline[0:3] == "dia", f"{pipeline} is not a pipeline"
        assert pipeline in AVAILABLE, f"{pipeline} pipeline does not exist"
        
        self._pipeline = pipeline
        
    def get_pipeline(self):
        return self._pipeline

    def generate_diarizations(self, experiment_path):
        """
        Generate a list of diarization objects

        Parameters
        ----------
        experiment_path : Str
            Path to a folder to where the experiment is located. This folder should
            include an audio sub-folder and a reference sub-folder. A predictions
            folder will be created to hold predicted rttms.

        Returns
        -------
        .rttm files save the predicted annotations in the {experiment_path}/predictions directory. 

        """
        # Input verifications through assertions
        
        assert os.path.exists(experiment_path), "Path given for experiment does not exist"
        
        audio_path = experiment_path + "/audio"
        
        # audio path
        assert os.path.exists(audio_path), f"Error: audio_path DNE\nPath:{audio_path}"
        
        # Making a folder for the diarization outputs
        export_dir = experiment_path + "/predictions"
        os.mkdir(export_dir)
        
        # creating list of audio file paths and audio clip names
        wav_paths, file_names = audio_paths(audio_path)
        
        # Diarization generation
        pipeline = torch.hub.load('pyannote/pyannote-audio', self._pipeline)
            
        for file_counter in range(len(file_names)):
            
            out_path = export_dir + "/" + file_names[file_counter] + ".rttm.txt"
            
            file_name = file_names[file_counter]
            wav = wav_paths[file_counter]
            
            print("\nProcessing file", file_name)
            
            # generate predictions
            this_diarization = pipeline({'uri': file_names[file_counter], 'audio': wav})
    
            # dump result to disk using RTTM format
            with open(out_path, 'w') as f:
                this_diarization.write_rttm(f)
                
            print("finished generating prediction for", file_name, "\n")
         
        
    
    

