#!/bin/bash

#SBATCH --job-name=rclone_copy
#SBATCH --mincpus=12
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=64gb
#SBATCH --time=50:00:00
#SBATCH --partition=standard
#SBATCH --account=guangyao
#SBATCH --output=%x.out

#Directory contianing the evidence files
base_dir="/xdisk/guangyao/michellewei/PMC_OA_Processed"
#Number of subdirectories
n_dir=18
#Name of rclone remote
rclone_remote="aws"
#Name of AWS bucket
aws_bucket="pmc-oa-biogrid"

for i in {0..$n_dir};
do
    rclone copy ${base_dir}/ev_${i} ${rclone_remote}:${aws_bucket} --progress -vv --transfers=100
done
