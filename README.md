# Biopoint reproducibility repository

# Installation

Install SEM2 as described here: https://github.com/Synthetic-Physiology-Lab/sem2.git
**Make sure that you install the version that is used for migration.**

We used Ovito Pro for visualization: https://www.ovito.org/
1. Download Ovito binaries from [https://www.ovito.org/](https://www.ovito.org/)
2. Add the `bin` directory to your system `PATH`

&#128308; All required Python packages are summarized in the `requirements.txt` file.

# Running Simulations

## Multi-particle Cell Preparation

- Unpack `example_simulations.tar.xz`
- Go to `multi_particle_nucleus/`
- Simulations are organized by time ranges: `ts_0_1_mil`, `ts_1_2_mil`, etc.
- In `ts_0_1_mil`:
  
     ```
     mpirun -np 4 PATH_TO_LAMMPS_src/lmp_mpi -in in.rand_cysce900_nusce_100.txt
     ```
  
     Or use serial version:
  
     ```
     PATH_TO_LAMMPS_src/lmp_serial -in in.rand_cysce900_nusce_100.txt
     ```

- Repeat simulation by moving restart files to the next folder.
- Output `.xyz` files (e.g., `dumpGrowN.xyz`) contain particle coordinates.
- View with OVITO.

## Spreading on Large ECM Substrate

- Go to `ECM_spreading/`
- Ensure seven atomfiles are present
- Run input file `in.mig_900_100_nuc_cen_rect` in:
  
     ```
     ECM_spreading/nuc_centered_medium/
     ```

- Also run in `nuc_centered_weak/`

##  Indentation

- Go to `indentation/`
- Run input file `in.ind_cell_mult_nuc` with:
  - Restart file: `cell_mult_nuc_1.restart`
  - Output: `.xyz` files with cell, ECM, and perimeter particles
  - Visualize in OVITO

## Spreading on ECM Patterns

- Go to `patterns/`
- Verify presence of atomfiles
- Start with `circle/pot12_1_5/` and run:
  
     ```
     in.spread_900_100_nuc_cen_circle
     ```

- Repeat for all folders inside `circle/`, then for `square/`, `triangle/`, and `rectangle/`

## Migration Through Constriction

- Go to `migration_constriction/`
- Run input file `in.mig_900_100_nuc_cen_rectangle`
- Output includes:
  - `cell.xyz`, `ecm_glass.xyz`, and `cell_stress.xyz`
- Also run scripts in:
  - `nuc_stiffer_5x/`
  - `nuc_stiffer_7x/`

## Optimization

- Go to `optimization/five_params_1_5/`
- Run:

     ```
     python optim_1.py
     ```

- Place `tmp_1`, `tmp_2`, etc. into a `runs/` folder
- Edit and run:

    ```
    plot_results.py
    ```

  - Set `num_iterations` to the number of iterations used

## Uncertainty Quantification (UQ)

- Go to `uq/six_params/`
- Edit `easyvvuq_production_early_py`:
  - Replace paths in lines 93–99 with:
    - `PTH_CURR_DIR` = current directory path
    - `PATH_TO_LAMMPS_src` = path to LAMMPS `src`
- Run:

     ```
     python easyvvuq_production_early_py
     ```

- After completion, run:

     ```
     python plot_results_statistics.py
     ```TODO

# Post-processing


## CSI and NSI Calculations

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

## Ellipticity Calculations

1. Navigate to:  
   `ellipticity/five_params_1_5_optim_run236/`

2. Run `nuc_ellipticity_nsi.py`.

3. This script uses **A. Bazhin's** ellipsoid fitting tool:  
   [ellipsoid_fit_python (2024)](https://github.com/aleksandrbazhin/ellipsoid_fit_python)

---

## Migration Through Constriction Analysis

1. Navigate to:  
   `exp_sim_constriction_analysis/`

2. Run `compute_nsi_compare.py`.

3. Required data:
   - Experimental CSVs (e.g., `exp_shape_1.csv`) from Keys et al. (2024), DOI: 10.1242/jcs.260623
   - LAMMPS output `cell.xyz` containing particle coordinates

---

## Nuclear Stress During Migration Through Constriction

1. Navigate to:  
   `migration_constriction_nuclear_stress/`

2. Run `spatial_binning.py`.

3. Requires:
   - Spatial binning data from OVITO or similar software
   - Data must contain average volumetric stress per particle in 1D spatial bins (along migration direction)

---

## Nuclear Stress During Spreading & Indentation

1. Navigate to:  
   `spreading_indentation_nuclear_stress/`

2. Run `spatial_binning.py`.

3. Requires:
   - Spatial binning data from OVITO (or other)
   - Data must contain average normal stress per particle in 1D bins (along x-axis)

---

## Nuclear Phase Separation Plotting

1. Navigate to:  
   `nuc_phase_separation/`

2. Run `nuc_phase_sep.py`.

3. This script includes hardcoded values for:
   - Cytoplasmic particle count inside the nuclear envelope (as measured via OVITO Pro)
