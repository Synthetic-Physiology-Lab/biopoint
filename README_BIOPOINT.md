# How to Cite

**Chattaraj, S., Zimmermann, J., & Pasqualini, F. S.**  
**"BIOPOINT: A particle-based model for probing nuclear mechanics and cell-ECM interactions via experimentally derived parameters."**

---

# Ovito Installation

1. Download Ovito binaries from [https://www.ovito.org/](https://www.ovito.org/)
2. Add the `bin` directory to your system `PATH`

---

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
     ```
