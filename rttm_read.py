#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 16:04:06 2020

@author: austinhushower
"""
__all__ = ['format_rttm', 'spkr_time_stamps', 'time_stamp_list']

def format_rttm(path):
    """
    This function inputs a path to an NIST rttm file  and returns its contents

    Parameters
    ----------
    path : String
        Direct file path to a NIST RTTM file

    Returns
    -------
    speaker_dict: a dictionary where an invidual speaker is mapped to a two dimensional array, where the outer array
                represents a line in the rttm file and the inner array holds all elements of the line as a string.
                
    speaker_info: a dictionary where an individual speaker is mapped to a array holding the contents of their speaker
                info line.

    """
    speakers_file = open(path, "r")
    
    if speakers_file.mode == "r":
        speakers_data = speakers_file.read()
        
    # print(speakers)
    
    #breaks the file into component speakers
    speakers = speakers_data.split("SPKR-INFO ")
    
    #removes the first instance as it is empty
    speakers.pop(0)
    
    "Data formatting below"
    
    # the speaker is represented by an integer >= 1
    speakers_dict = {}
    
    # generates a dictionary where the key is the person and the item is a list of all the times in which they spoke
    counter = 1
    for speaker in speakers:
        speakers_dict[counter] = speaker.split("SPEAKER")
        counter = counter + 1
    
   # a dictionary which will contain the speaker information line for all speakers. Speaker represented by an integer >= 1
    speaker_info = {}
    
    # adds identification line for each speaker to speaker_info

    for key, speaker_data in speakers_dict.items(): # pulling out and formatting speaker info line
        speaker = speaker_data.pop(0).split(" ")
        
        if speaker[-1][-1:] == "\n":                # removing \n and \t from the end of the lines
            speaker[-1] = speaker[-1][0:-1]
            
        if speaker[-1][-1:] == "\t":
            speaker[-1] = speaker[-1][0:-1]
        
        speaker_info[key] = speaker

    # removes extra space at the beginning of each line and makes the item which the speaker number matches to a 2d array.
    # The outer array represents line number and the inner array is each word in the line, with no spaces on either side
        
    for speaker, speaker_data in speakers_dict.items(): #loops through the individual speakers
        new_speaker_data = []                           #list which new speaker data is put in to
        for line_string in speaker_data:                #loops through every line of the current speaker data
            if line_string[0] == " ":                   #checks and removes space at the beginning of the line
                new_line = line_string[1:]
                words = new_line.split(" ")             #breaks the single line string into a list of the indivual elements of the line
            else:
                words = line_string.split(" ")
            
            # remove \n at the end of the line            
            if words[-1][-1:] =="\n":
                words[-1] = words[-1][0:-1]
            
            new_speaker_data.append(words)
   
        speakers_dict[speaker] = new_speaker_data       #replacing what is currently in speaker data with the formatted time data
        
        
    return speakers_dict, speaker_info

def isFloat(str):
    """
    Determines if a string is a valid floating point number
    """
    if str.replace('.','',1).isdigit():
        return True
    else:
        return False   
    
def spkr_time_stamps(path):
    """
    Generates time stamps for all speech blocks from rttm data for the audio clip and classifies them by speaker

    Parameters
    ----------
    path : path to a rttm file which one wants to extract a list of time stamps
        DESCRIPTION.

    Returns
    -------
    time_stamps: Dictionary
        A dictionary where the key is the unique speaker id and the value is a list of tuples
        representing speech blocks where the tuple is: (start_time, speech_block_duration)

    """
    formatted_rttm, speaker_info = format_rttm(path) #speaker_info not used
    
    time_stamps = {}
    
    speaker_counter = 1                                 # a unique number for every speaker
    for speaker, speaker_data in formatted_rttm.items():
        this_speaker_stamps = []
        for line_list in speaker_data:
            
            numbers = []                                #a list which will contain all valid numbers in the line
            for element in line_list:                   #finding and attaching all numbers to numbers list
                if isFloat(element):
                    numbers.append(float(element))
                
            num_tuple = tuple(numbers[1:])              #removing the first number as it is a channel identifier
                
            this_speaker_stamps.append(num_tuple)
        
        time_stamps[speaker_counter] = this_speaker_stamps
        speaker_counter = speaker_counter + 1 
        
    return time_stamps
  
def time_stamp_list(path, sort_factor):
    """
    Creates a list of the time stamps sorted base off of a sort factor
        0- sort by start time
        1- sort by duration
        2- sort by end_time

    Parameters
    ----------
    path : string
        file path to a rttm file
        
    sort_factor : Int
        An integer [0,2] which denotes how to order the time stamps

    Returns
    -------
    sorted : a sorted list of tuples based on the sort_factor

    """
    assert sort_factor in (0, 1, 2)
    time_stamps_dict = spkr_time_stamps(path)
    
    time_stamps = []
    
    for speaker_stamp_list in time_stamps_dict.values():
        time_stamps.extend(speaker_stamp_list)
        
    if sort_factor == 0 or sort_factor == 1:
        return sorted(time_stamps, key=lambda x: x[sort_factor])
    else:
        return sorted(time_stamps, key=lambda x: x[0]+x[1])
        
    return time_stamps