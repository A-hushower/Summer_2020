#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:39:36 2020

@author: austinhushower
"""

from pretrained_pipeline import PretrainedPipeline
from pmetrics_grader import calculate_der

# available pretrained pipelines are "dia", "dia_ami", "dia_dihard"
pipeline_type = "dia_ami"

pipeline = PretrainedPipeline(pipeline_type)

# path to various needed directories
experiment_path = "path/to/folder"

pipeline.generate_diarizations(experiment_path)

# calculate der with no collar and no overlap skipping
normal_der = calculate_der(experiment_path, 0.0, False)

# calculate der with a collar of 250ms and overlap skipping
assisted_der = calculate_der(experiment_path, .25, True)
