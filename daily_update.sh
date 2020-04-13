#!/bin/zsh

# Allow the script to exit on error
set -e

# Pull potential changes in remote repo
git pull

# Pull new data from remote repos
git submodule foreach --recursive 'git pull'

# Activate anaconda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate jupyter

# Create new plots
python ./projections_covid2019_world.py || \
    (echo "Error while processing world data " && exit 1)
python ./projections_covid2019_italy.py || \
    (echo "Error while processing italian data " && exit 1)

# Change the date in README.md
sed -i "s/^**Updated.*/**Updated $(date +%d\\/%m\\/%Y -d yesterday)**/" README.md

# Stage submodules, plots and README.md
git add data-ita data-world plots README.md

# Commit
git commit -m "Daily udpate ($(date +%d/%m/%Y -d yesterday))" || exit 1

# Push changes
git push

# Send a notification
notify-send "Pushed daily update on COVID data"
