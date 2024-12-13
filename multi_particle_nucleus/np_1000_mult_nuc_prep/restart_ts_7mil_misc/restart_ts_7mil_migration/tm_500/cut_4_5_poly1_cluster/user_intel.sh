#!/bin/bash

#SBATCH --job-name=sandipan-lammps-job 
#SBATCH --partition=compute
#SBATCH -D ./
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH -t 06:00:00

# loading modules
module load intel-oneAPI
module load mpi/2021.2.0
module load compiler/2021.2.0
module load mkl/2021.2.0

# run the job with 64 cores
mpirun -np 16 lmp_intel_cpu_intelmpi -in in.mig_equil_900_100.txt
 
exit 0
