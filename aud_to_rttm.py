#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 00:39:14 2020

@authors: germa and austinhushower
"""


import os

__main__ = ["aud_rttm", "aud_rttm_lst"]
       
def aud_rttm(in_path, out_path, name = ""):
    """
    Gernerates an rttm file for a single audacity generated labels text file

    Parameters
    ----------
    in_path : Str
        Path to the audacity file
    out_path : Str
        Path to write the rttm file to. 
    name: Str, optional
        Name of the file. Defaults to "". If no file name is found, the file 
        name of the rttm is scraped and used
    
    Returns
    -------
    Writes a file at exp_dir

    """
    # Ensuring existence of output path
    assert os.path.exists(in_path), f"Error: Path DNE\nPath:{in_path}"
    
    # If no name is given, we will scrape the name of the rttm file
    if name == "":
        # Note this method will not work on windows
        name = os.path.basename(in_path)
        
    # Removing the .txt from the name of the file
    if name[-4:] == ".txt":
        name = name[0:-4]
    
    # number of speakers in the file
    speaker_counter = 0   
        
    with open(in_path, 'r') as file:

        # Two dimensional array: outer is line, inner is element
        file_lines = [line.split() for line in file]
        
        speakers = {}
        speaker_data = {}
        
        for line in file_lines:
            
            # Line[2] is the persons name
            if line[2] not in speakers:
                
                speaker_counter += 1
                speakers[line[2]] = speaker_counter
                speaker_data[line[2]] = []
        
            # rounding time stamps to third decimal place
            line[0] = round(float(line[0]), 3)
            line[1] = round(float(line[1]), 3)
            
            # adding this speakers speech block to others
            stamp = (line[0], line[1])
            speaker_data[line[2]].append(tuple(stamp))
            
    with open(os.path.join(out_path, f'{name}.rttm'), 'w+') as file:
        
        for speaker, spkr_number in speakers.items():
            
            stamps = speaker_data[speaker]
            
            identifier = f"PER-{spkr_number}"
            
            # Adding speaker info line
            # Example Line:
            #   SPKR-INFO Seq12-3P-S1M1 1 <NA> <NA> <NA> unknown PER-03 <NA>
            file.write(f'SPKR-INFO {name} 1 <NA> <NA> <NA> unknown {identifier} <NA>\n')
             
            for time_stamp in stamps:
                start = time_stamp[0]
                duration = round(time_stamp[1] - start, 3)
                
                # Example Line:
                #   SPEAKER Seq06-2P-S1M0 1 25.658 1.550 <NA> <NA> PER-2 <NA>
                file.write(f"SPEAKER {name} 1 {start} {duration} <NA> <NA> {identifier} <NA>\n")

def aud_rttm_lst(out_path, directory):
    """
    Generate rttms for a large amount of audacity txt files

    Parameters
    ----------
    out_path : Str
        Path to write the rttm file to. 
    directory : Str
        Path to a directory containing the raw text files.

    Returns
    -------
    None. Generates rttm files at out_path location

    """   
    assert os.path.isdir(directory), f"Error: Directory DNE\nDirectory: {directory}"
    
    files = os.listdir(directory)
    
    for file_name in files:
        if file_name.endswith(".txt"):
            file_path = f"{directory}/{file_name}"
            
            #generate rttm file for this path
            aud_rttm(file_path, out_path)
 


