#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:52:41 2020

@author: lbishal
"""


import soundfile as sf
import os
import resampy

data_dir      = "Directory containing Audio files"
out_dir       = "Directory to write resampled audio files to"
suffix        = "Add a unique suffix after the file name"

if(not os.path.exists(out_dir)):
    os.makedirs(out_dir)
    
all_wavfiles = os.listdir(data_dir)

for each_wavfile in all_wavfiles:
    if each_wavfile.endswith(".WAV"):
        wavfile    = os.path.join(data_dir,each_wavfile)
        resample_fs     = 16000
        signal, sr      = sf.read(wavfile)
        signal_resamp   = resampy.resample(signal,sr,resample_fs)
        outfile_resamp  = os.path.join(out_dir,each_wavfile.split('.')[0]+ suffix +'.wav')
        sf.write(outfile_resamp,signal_resamp,resample_fs)