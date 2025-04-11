HOW TO CITE

Sandipan Chattaraj, Julius Zimmermann, Francesco Silvio Pasqualini, “BIOPOINT: A particle-based model for probing nuclear mechanics and cell-ECM interactions via experimentally derived parameters.”
Instructions for Installation

To compile

    Dowload LAMMPS version stable_29Oct2020

    Unpack and cd into src folder

    build LAMMPS by running make serial and make mpi

    In this repository: Unpack USER-SEM.tar.gz and cp USER-SEM into LAMMPS src directory

    Add the package to the makefile by appending user-sem to this line in the Makefile in the LAMMPS src directory: PACKUSER = user-adios user-atc user-awpmd user-bocs user-cgdna user-cgsdk user-colvars \ user-diffraction user-dpd user-drude user-eff user-fep user-h5md \ user-intel user-lb user-manifold user-meamc user-mesodpd user-mesont \ user-mgpt user-misc user-mofff user-molfile \ user-netcdf user-omp user-phonon user-plumed user-ptm user-qmmm \ user-qtb user-quip user-reaction user-reaxc user-scafacos user-smd user-smtbq \ user-sdpd user-sph user-tally user-uef user-vtk user-yaff user-sem

    Add the package by make yes-user-sem. It will throw a lot of warnings. Enter y to every open point.

    also add the molecule package make yes-molecule

    apply make package-update

    copy the content of the original USER-SEM/src_changed folder as downloaed from GitHub to src/USER-SEM/src_changed

    run make yes-user-sem (again y to all) and make package-update

    recompile LAMMPS with make serial and make mpi

    either copy LAMMPS binaries lmp_serial and lmp_mpi to a directory included in PATH or add the src directory to PATH

Ovito installation

    Download the ovito binaries from their website
    Add the bin directory to the path


Instructions for Running Simulations

First: unpack the example_simulations.tar.xz folder.
Multi-particle cell preparation:


    Open the folder multi_particle_nucleus. Here the folders are organized as per timesteps 0-1, 1-2, etc. up to 6-7. Open the folder for 0 to 1 million timesteps (ts_0_1_mil) and run the input file
    in.rand_cysce900_nusce_100.txt using the following command: mpirun -np 4 PATH_TO_LAMMPS_src/lmp_mpi -in in.rand_cysce900_nusce_100.txt. It will create 900 cytoplasmic particles and 100 nuclear
    particles randomly in a cylindrical region of space and run Brownian dynamics (BD) on them -> result stored as cysce900_nusce100_ts1m.restart. 
    Serial alternative: PATH_TO_LAMMPS_src/lmp_serial -in in.rand_cysce900_nusce_100.txt
    Copy cysce900_nusce100_ts1m.restart in the next folder (ts_1_2_mil) and run the file in.rand_cysce900_nusce_100.txt. It will run BD after removing the cylindrical constraint and generate the restart
    file cysce900_nusce100_ts2m.restart. Copy this restart file in the next folder (ts_2_3_mil) and continue this process up to ts_6_7_mil. Please note that since particle dynamics simulations are not
    deterministic, you might have to run simulations up to different number of timesteps and follow a slightly different protocol to obtain phase separation.
    Each of these simulations generate a .xyz file: dumpGrowN.xyz, which dump the coordinates of all particles in a cell after every N timesteps (N=10000 here). These cells can be viewed in a
    visualization software such as Ovito.
    
    *PATH_TO_LAMMPS_src is the path to the LAMMPS src folder.
    
Spreading on large ECM substrate:
    Open the "ECM_spreading" folder. Ensure that the seven atomfiles are there in the folder, containing the types, position coordinates and velocities (x, y and z) of all cellular particles.
    Open the folder "nuc_centered_medium" folder. Run the input file in.mig_900_100_nuc_cen_rect with similar commands as mentioned earlier. The output trajectories will be created in the
    .xyz files. The cell.xyz and ecm_glass.xyz consists of the coordinates of the cellular particles, ecm and inert glass particles. The cell and ECM can be viewed in a visualization software such as
    Ovito. Follow the same set of steps by going to the "nuc_centered_weak" folder.

Indentation:

    Open the "indentation" folder. Ensure that the restart file cell_mult_nuc_1.restart is there in the folder. Run the input file in.ind_cell_mult_nuc with similar commands as mentioned earlier.
    The output trajectories will be created in the .xyz files. The cell.xyz, ecm_glass.xyz, and peri_particles.xyz consists of the coordinates of the cellular particles, ecm and inert glass particles,
    and perimeter particles which are constrained from moving and mimic focal adhesion. The cell and ECM can be viewed in a visualization software such as Ovito.
    

Spreading on ECM Patterns:

    Open the "patterns" folder. Ensure that the seven atomfiles are there in the folder, containing the types, position coordinates and velocities (x, y and z) of all cellular particles. Then, open the
    circle folder, followed by the folder "pot12_1_5". Run the input file in.spread_900_100_nuc_cen_circle with similar commands as mentioned earlier. The output trajectories will be created in the
    .xyz files. The cell.xyz and ecm_glass.xyz consists of the coordinates of the cellular particles, ecm and inert glass particles. The cell and ECM can be viewed in a visualization software such as
    Ovito. Follow the same steps for the input scripts in all the folders inside "circle" and then follow similar steps for "square", "triangle" and "rectangle" folders.
    
Migration through constriction:

    Open the "migration_constriction" folder. Ensure that the seven atomfiles are there in the folder, containing the types, position coordinates and velocities (x, y and z) of all cellular particles.
    Run the input file in.mig_900_100_nuc_cen_rectangle with similar commands as mentioned earlier. The output trajectories will be created in the .xyz files. The cell.xyz and ecm_glass.xyz consists of
    the coordinates of the cellular particles, ecm and inert glass particles. The cell_stress.xyz consists of the per-particle values of the components of the stress tensor. The cell and ECM can be
    viewed in a visualization software such as Ovito. The stresses can ve visualized from the cell_stress.xyz file. Follow the same steps for the input scripts in the folders "nuc_stiffer_5x" and
    "nuc_stiffer_7x".
    
Optimization:

    Open the "optimization" folder, followed by the "five_params_1_5" folder. Run the optimization python file "optim_1.py". Once the optimization is complete, place all the output folders
    tmp_1, tmp_2 etc. inside a folder named "runs". Then, open the python file plot_results.py". Change the value of the variable "num_iterations" to the current number of iterations. Then, run the
    python file "plot_results.py".
    
UQ:
    
    PTH_CURR_DIR is the path to the current directory
    Open the folder "uq", followed by the folder "six_params". Open the file "easyvvuq_production_early_py" and in lines 94, 96 and 99, replace
    "/home/chattaraj_s/vvuq/np_1000/cell_height_9/six_params/" with the path to the current directory. In line 93, replace "/home/chattaraj_s/LAMMPS/29Oct20/lammps-29Oct20/src" with PATH_TO_LAMMPS_src.
    Run the python file "easyvvuq_production_early_py". Once the UQ run is complete the files "result_list.csv" and "results_force.csv" will be generated. Once this is done, run the python file
    "plot_results_statistics.py".
