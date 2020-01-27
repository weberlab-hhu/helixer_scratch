#!/bin/bash
#PBS -l select=1:ncpus=1:mem=200mb
#PBS -l walltime=7:59:00
#PBS -A "HelixerOpt"

module load Python/3.6.5

/home/festi100/git/HelixerPrep/scripts/ensemble.py  -p /gpfs/project/festi100/jobs//IiFEB_11/Acomosus/predictions.h5 -p /gpfs/project/festi100/jobs//IiFEB/Acomosus/predictions.h5 -po ensemble_/gpfs/project/festi100/jobs//IiFEB_IiFEB_11/Acomosus/predictions.h5
