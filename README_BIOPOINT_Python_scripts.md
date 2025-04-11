# How to Cite

**Chattaraj, S., Zimmermann, J., & Pasqualini, F. S.**  
**"BIOPOINT: A particle-based model for probing nuclear mechanics and cell-ECM interactions via experimentally derived parameters."**

**Attention: All following analyses are conducted in the folder `post_processing_scripts`.**

---

# CSI and NSI Calculations

1. Navigate to:  
   `NSI_CSI/five_params_1_5_optim_run236/pot12_1_5/`

2. Open the file `csi_nsi_mult_ts.py`.

3. Depending on the pattern (e.g., circular, square), update **line 9** with the corresponding `.xyz` file:  
   - Circular: `"cell_circ.xyz"`  
   - Square: `"cell_sq.xyz"`  
   - Triangle: `"cell_tri.xyz"`  
   - Rectangle 1:3: `"cell_rec_1_3.xyz"`  
   - Rectangle 1:7: `"cell_rec_1_7.xyz"`  
   - Rectangle 1:19: `"cell_rec_1_19.xyz"`

4. Update **line 84** with the output `.csv` filename:
   - Circular: `"nsi_csi_circle.csv"`  
   - Square: `"nsi_csi_square.csv"`  
   - Triangle: `"nsi_csi_triangle.csv"`  
   - Rectangle 1:3: `"nsi_csi_rect_1_3.csv"`  
   - Rectangle 1:7: `"nsi_csi_rect_1_7.csv"`  
   - Rectangle 1:19: `"nsi_csi_rect_1_19.csv"`

5. These `.xyz` files are generated from LAMMPS simulations.

6. Run `csi_nsi_mult_ts.py` to generate the corresponding `.csv` files.

7. The file `nsi_csi_data.xlsx` contains digitized experimental data from:
   - Versaevel et al. (2012), DOI: 10.1038/ncomms1668
   - Sarikhani et al. (2024), DOI: 10.1021/acsnano.4c03743

8. Run `plot_csi_nsi.py` to generate:
   - `csi_time.pdf`
   - `nsi_time.pdf`
   - `csi_nsi.pdf`
   - `csi_nsi_1_5.csv`

9. Repeat the process for these folders:
   - `pot12_1_55`
   - `pot12_1_6`
   - `pot12_1_65`

10. Copy the resulting `.csv` files:
    - `csi_nsi_1_5.csv`
    - `csi_nsi_1_55.csv`
    - `csi_nsi_1_6.csv`
    - `csi_nsi_1_65.csv`  
    into the `mean_std` folder, along with `nsi_csi_data.xlsx`.

11. Run `plot_csi_nsi_mean_std.py` to generate the final `csi_nsi.pdf`.

---

# Ellipticity Calculations

1. Navigate to:  
   `ellipticity/five_params_1_5_optim_run236/`

2. Run `nuc_ellipticity_nsi.py`.

3. This script uses **A. Bazhin's** ellipsoid fitting tool:  
   [ellipsoid_fit_python (2024)](https://github.com/aleksandrbazhin/ellipsoid_fit_python)

---

# Migration Through Constriction Analysis

1. Navigate to:  
   `exp_sim_constriction_analysis/`

2. Run `compute_nsi_compare.py`.

3. Required data:
   - Experimental CSVs (e.g., `exp_shape_1.csv`) from Keys et al. (2024), DOI: 10.1242/jcs.260623
   - LAMMPS output `cell.xyz` containing particle coordinates

---

# Nuclear Stress During Migration Through Constriction

1. Navigate to:  
   `migration_constriction_nuclear_stress/`

2. Run `spatial_binning.py`.

3. Requires:
   - Spatial binning data from OVITO or similar software
   - Data must contain average volumetric stress per particle in 1D spatial bins (along migration direction)

---

# Nuclear Stress During Spreading & Indentation

1. Navigate to:  
   `spreading_indentation_nuclear_stress/`

2. Run `spatial_binning.py`.

3. Requires:
   - Spatial binning data from OVITO (or other)
   - Data must contain average normal stress per particle in 1D bins (along x-axis)

---

# Nuclear Phase Separation Plotting

1. Navigate to:  
   `nuc_phase_separation/`

2. Run `nuc_phase_sep.py`.

3. This script includes hardcoded values for:
   - Cytoplasmic particle count inside the nuclear envelope (as measured via OVITO Pro)
