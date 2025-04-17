import easyvvuq as uq
import chaospy as cp
from easyvvuq.actions import CreateRunDirectory, Encode, Decode, Actions
import os
import pandas as pd
import numpy as np


class CustomDecoder:
    def __init__(self, target_filename=None, output_columns=None):
        self.target_filename = target_filename
        self.output_columns = output_columns
        self.n_timesteps = None 
        self.time_list = None

    def _get_output_path(self, run_info=None, outfile=None):
        run_path = run_info['run_dir']
        if not os.path.isdir(run_path):
            raise RuntimeError(f"Run directory does not exist: {run_path}")
        return os.path.join(run_path, outfile)

    def parse_sim_output(self, run_info={}):
        out_path = self._get_output_path(run_info, self.target_filename)
        time_list = []
        force_list = []
        with open(out_path, "r") as logfile:
            reading_forces = False
            for line in logfile:
                if "Step Temp f_indn[1] f_indn[2] f_indn[3]" in line:
                    # initiate reading from next line on
                    reading_forces = True
                    continue
                if "Loop time of" in line:
                    reading_forces = False
                if reading_forces:
                    line_list = line.split()
                    time = 1e-3 * float(line_list[0])
                    force = float(line_list[4])
                    time_list.append(time)
                    force_list.append(force)
        # check if forces could be read
        if len(force_list) == 0:
            # number of timesteps not yet known
            if self.n_timesteps is None:
                raise RuntimeError("First simulation run failed, cannot guess number of timesteps.")
            # copy previous time list
            time_list = self.time_list
            # set all forces to NaN
            force_list = [np.nan] * self.n_timesteps
        else:
            self.n_timesteps = len(force_list)
            self.time_list = time_list

        return {"time": time_list, "force": force_list}


params = {"Rcell": {"type": "float", "default": 10.0},
          "pd": {"type": "float", "default": 0.74},
          "N": {"type": "integer", "default": 1000},
          "rho": {"type": "float", "default": 2.0},
          "eta0": {"type": "float", "default": 0.005},
          "kappa0": {"type": "float", "default": 0.005},
          "mylambda": {"type": "float", "default": 0.75},
          "kappa_nuc": {"type": "float", "default": 0.06},
          "eta_nuc": {"type": "float", "default": 0.22},
          "k_ind": {"type": "float", "default":500000},
          "k12": {"type": "float", "default":1.5},
          }

vary = {
    "eta0": cp.Normal(0.055, 0.0055),
    #"eta0": cp.Uniform(0.0025, 0.0075),
    "kappa0": cp.Normal(0.015, 0.0015),
    #"kappa0": cp.Uniform(0.0025, 0.0075),
    #"k_ind": cp.Normal(500000,50000),
    "eta_nuc": cp.Normal(0.22, 0.022),
    "kappa_nuc": cp.Normal(0.06, 0.006),
    "mylambda": cp.Normal(0.75, 0.075),
    "k12": cp.Normal(1.5, 0.15),
}

# encoder for input file
encoder = uq.encoders.JinjaEncoder(template_fname='in.ind_cell_mult_nuc_template.jinja', target_filename='in.ind_cell_mult_nuc')
'''
jinja_encoder = uq.encoders.JinjaEncoder(template_fname='in.ind_cell_mult_nuc_template.jinja', target_filename='in.ind_cell_mult_nuc')
copy_encoder = uq.encoders.CopyEncoder('cell_rect_mult_nuc.restart', '/tmp/cell_rect_mult_nuc.restart')
encoder = uq.encoders.MultiEncoder(jinja_encoder, copy_encoder)
'''

decoder = CustomDecoder(target_filename='log.lammps', output_columns=['time', "force"])

print('Starting campaign')
execute = uq.actions.ExecuteLocal(f"/home/chattaraj_s/LAMMPS/29Oct20/lammps-29Oct20/src/lmp_serial -echo none -screen none -in in.ind_cell_mult_nuc")
actions = Actions(CreateRunDirectory('/home/chattaraj_s/vvuq/np_1000/cell_height_9/order_four_six_params/tmp', flatten=True),
                  Encode(encoder), execute, Decode(decoder))
target_dir = '/home/chattaraj_s/vvuq/np_1000/cell_height_9/order_four_six_params/tmp'
if not os.path.exists(target_dir):
                    os.mkdir(target_dir)
campaign = uq.Campaign(name='sem', params=params, actions=actions, work_dir='/home/chattaraj_s/vvuq/np_1000/cell_height_9/order_four_six_params/tmp')

print('Campaign done')

print('Sampling')
campaign.set_sampler(uq.sampling.PCESampler(vary=vary, polynomial_order=4, regression=True))
print('Collate')
campaign.execute().collate()

print('Samples done')

df_result = campaign.get_collation_result()

print('Got result')
df_result.to_csv("result_list.csv", index=False)
# TODO analyse results
results = campaign.analyse(qoi_cols=["force"])

mean = results.describe("force", "mean")
p_10 = results.describe("force", "10%")
p_90 = results.describe("force", "90%")
std = results.describe("force", "std")
sobols_first = results.sobols_first("force")
sobols_total = results.sobols_total("force")


def write_sobol_to_dict(df, sobol_dict, order):
    for key in sobol_dict:
        df['sobol_' + order + '_'  + key] = sobol_dict[key]

results_dict = {'mean': mean, 'p_10': p_10, 'p_90': p_90, 'std': std} 
write_sobol_to_dict(results_dict, sobols_first, 'first')
write_sobol_to_dict(results_dict, sobols_total, 'total')
df = pd.DataFrame(results_dict)
df.to_csv("results_force.csv", index=False)

print('Mutual interaction')
sobols_second = results.sobols_second("force")
print(sobols_second)
