#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --gres=gpu:2
#SBATCH --n=5
#SBATCH -c=1
#SBATCH --account=GS79-10
#SBATCH -J NLP
#SBATCH -o EUTERPE_run%j.out

cd /home/marek357/EUTERPE
python3 main.py 
