#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 16:51:42 2020

@author: austinhushower
"""
import os
from pyannote.core import Segment, Annotation

from rttm_format import spkr_time_stamps

def generate_annotation(rttm_path):
    """
    Inputs an rttm path and generates a pyannote.core style annotation

    Parameters
    ----------
    rttm_path : Str
        Path to a valid .rttm file.

    Returns
    -------
    this_annotation : Pyannote.Core Annotation
        Annotation holds the time stamps and speaker ids for der calculation.

    """
    
    # Generating hypothesis pyannote.core annotation object --------------------------
        
    file_name = os.path.basename(rttm_path)
    
    # dictionary containing spkr ids as keys and time stamp tuple list as values
    time_stamps = spkr_time_stamps(rttm_path)
    
    this_annotation = Annotation(uri=file_name)
    
    # iterate over all speakers
    for spkr_id, stamps in time_stamps.items():
        
        # iterate over
        for stamp in stamps:
            start = stamp[0]
            duration = stamp[1]
            
            this_annotation[Segment(start, start + duration)] = spkr_id
            
    return this_annotation