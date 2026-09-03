#!/bin/bash
#SBATCH --account=pk_tmobench
#SBATCH --job-name=measure-bandwidth
#SBATCH --partition=gpu
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=4000
#SBATCH --gres=gpu:1
#SBATCH --output=measure-bandwidth.log

module load singularity
export TMPDIR=/tmp
singularity exec --nv -B /opt/cray:/opt/cray -B /project/pk_tmobench/tomography-benchmarks:/tomography-benchmarks -B /scratch/pk_tmobench:/scratch/pk_tmobench tomobenchmarks.sif bash -c '. /miniconda3/bin/activate && cd /tomography-benchmarks && just measure-bandwidth'
