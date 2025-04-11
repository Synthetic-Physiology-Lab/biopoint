HOW TO CITE

Sandipan Chattaraj, Julius Zimmermann, Francesco Silvio Pasqualini, “BIOPOINT: A particle-based model for probing nuclear mechanics and cell-ECM interactions via experimentally derived parameters.”
 
CSI and NSI calculations:
    
    Open the folder "NSI_CSI", followed by the folder "five_params_1_5_optim_run236", followed by the folder "pot12_1_5". Open the file "csi_nsi_mult_ts" and for circular pattern we have in line 9,
    file1=open("cell_circ.xyz","r") 
    and in line 84 we have 
    df.to_csv('nsi_csi_circle.csv', index = False)
    Run this script to generate the file nsi_csi_circle.csv. Similarly for square, triangular, rectangle(1:3), rectangle(1:17) and rectangle(1:19) we should have in line 9
    the fiename as "cell_sq.xyz", "cell_tri.xyz, "cell_rec_1_3.xyz", "cell_rec_1_7.xyz" and "cell_rec_1_19.xyz" respectively. These are the dump files generated from the spreading on pattern simulations
    performed in LAMMPS.
    In line 84 we should have the filename as "nsi_csi_square.csv", "nsi_csi_triangle.csv", "nsi_csi_rect_1_3.csv", "nsi_csi_rect_1_7.csv" and "nsi_csi_rect_1_19.csv", respectively.
    The file "nsi_csi_data.xlsx" contains the digitized experimental data from Versaevel et al. (2012) and Sarikhani et al. (2024). We should now run the Python file "plot_csi_nsi.py" which will
    generate the plots "csi_time.pdf", nsi_time.pdf", "csi_nsi.pdf" and the data file "csi_nsi_1_5.csv". A similar procedure should be followed for the folders "pot12_1_55", "pot12_1_6" and
    "pot12_1_65".
    Then, copy the data files named "csi_nsi_1_5.csv", "csi_nsi_1_55.csv", "csi_nsi_1_6.csv" and "csi_nsi_1_65.csv" from the respective folders and paste them inside the folder named "mean_std". This
    folder should also contain the experimental data file "nsi_csi_data.xlsx". Finally run the Python file "plot_csi_nsi_mean_std.py" to generate the final plots "csi_nsi.pdf".
    
Ellipticity calculations:

    Open the folder "ellipticity" followed by the folder "five_params_1_5_optim_run236". Run the Python file "nuc_ellipticity_nsi.py". This code uses an existing Python script named "ellipsoid.fit"
    fom Bazhin A. -- Ellipsoid fit python. 2024, "https://github.com/aleksandrbazhin/ellipsoid_fit_python".
    
Migration through constriction analysis:

    Open the folder "exp_sim_constriction_analysis". Run the Python file "compute_nsi_compare.py". This requires the digitized data from the experiments of Keys et al. (2024), which is there in the
    files "exp_shape_1.csv" etc. The output file from the LAMMPS simulations, containing coordinates of particles, named cell.xyz is necessary to run this Python script.
    
Migration through constriction -- nuclear stress analysis:

    Open the folder "migration_constriction_nuclear_stress". Run the Python file "spatial_binning.py". This requires the spatial binning data, generated from a stress analysis in OVITO or any other
    visualization software. This data consists of average volumetric stress per particle in 1D spatial bins along the direction of migration.

Nuclear stress analysis of spreading and indentation simulations:

    Open the folder "spreading_indentation_nuclear_stress". Run the Python file "spatial_binning.py". This requires the spatial binning data, generated from a stress analysis in OVITO or any other
    visualization software. This data consists of average normal stress per particle in 1D spatial bins along the x axis.
    
Nuclear Phase Separation Data Plotting:

    Open the folder "nuc_phase_separation". Run the Python file "nuc_phase_sep.py". This script already has the hard coded values of number of cytoplasmic particles inside nuclear envelope computed
    in the visualization software OVITO Pro.
