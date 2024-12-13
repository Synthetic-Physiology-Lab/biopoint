#import chaospy as cp
import os
import pandas as pd
import numpy as np
import subprocess
import time
import shlex
#import jinja2
from jinja2 import Template
from scipy.interpolate import interp1d
from scipy.optimize import minimize
import math
import shutil
 
class customEncoder:
    #def get_input_info(self):
     #   target_filename='in.ind_cell_mult_nuc'
     #   restart_filename='cell_rect_mult_nuc.restart'
     #   template_fname=''
     #   return {"input_filename": target_filename, "restart_fname": restart_filename}
    
    def __init__(self, params, target_dir, template_fname="in.ind_cell_mult_nuc_template.jinja",
                 target_filename="in.ind_cell_mult_nuc"):

        self.target_filename = target_filename
        self.template_fname = template_fname
        self.fixture_support = True
        self.encode(params, target_dir=target_dir)    

    def encode(self, params, target_dir):
        """Substitutes `params` into a template application input, saves in
        `target_dir`

        Parameters
        ----------
        params        : dict
            Parameter information in dictionary.
        target_dir    : str
            Path to directory where application input will be written.
        """

        local_params = params
        print(self.template_fname)

        try:
            with open(self.template_fname, 'r') as template_file:
                template_txt = template_file.read()
                self.template = Template(template_txt, autoescape=True)
        except FileNotFoundError:
            raise RuntimeError(
                "the template file specified ({}) does not exist".format(self.template_fname))

        if not target_dir:
            raise RuntimeError('No target directory specified to encoder')

        try:
            print(local_params)
            app_input_txt = self.template.render(local_params)
        except KeyError as e:
            self._log_substitution_failure(e)

        # Write target input file
        target_file_path = os.path.join(target_dir, self.target_filename)
        print(target_file_path)
        with open(target_file_path, 'w') as fp:
            fp.write(app_input_txt)
    
    def _log_substitution_failure(self, exception):
        reasoning = (f"\nFailed substituting into template "
                     f"{self.template_fname}.\n"
                     f"KeyError: {str(exception)}.\n")

        raise KeyError(reasoning)

class ExecuteLammps:
    def __init__(self,target_dir):
            time0 = time.time()
            command_line="/home/chattaraj_s/LAMMPS/29Oct20/lammps-29Oct20/src/lmp_serial -echo none -screen none -in "+ target_dir +"/in.ind_cell_mult_nuc"
            args=shlex.split(command_line)
            print(args)
            #subprocess.run(["/home/user/LAMMPS/lammps-29Oct20/src/lmp_serial", "-echo", "none", "-screen", "none", "-in", "in.ind_cell_mult_nuc"])
            subprocess.run(args)
            time1 = time.time() - time0
            print(f"Took {time1} seconds to complete.")


class CustomDecoder:
    def __init__(self, target_filename=None, output_columns=None):
        self.target_filename = target_filename
        self.output_columns = output_columns
        self.n_timesteps = None 
        self.time_list = None
        self.parse_sim_output()

    def _get_output_path(self, run_info=None, outfile=None):
        #run_path = run_info['run_dir']
        #run_path="/home/chattaraj_s/optimizer/take_8"
        run_path = os.getcwd()
        print('run_path:', run_path)
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
                    force = 1e-6 *float(line_list[4])
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

def compute_rmse(myargs):
        eta0 = myargs[0]
        kappa0 = myargs[1]
        eta_nuc = myargs[2]
        kappa_nuc = myargs[3]
        k12 = myargs[4]
        params = {"Rcell": 10.0,
          "pd": 0.74,
          "N": 1000,
          "rho": 2.0,
          "eta0": eta0,
          "kappa0": kappa0,
          "mylambda": 0.75,
          "kappa_nuc": kappa_nuc,
          "eta_nuc": eta_nuc,
          "k_ind": 500000,
          "k12": k12
          }
        global function_calls
        function_calls = function_calls + 1
        #target_dir = f"/home/chattaraj_s/optimizer/take_8/tmp_{function_calls}"
        target_dir = os.path.join(os.getcwd(), f"tmp_{function_calls}")
        print('target_dir:', target_dir)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        encoder =  customEncoder(params, target_dir)
        exec_lammps = ExecuteLammps(target_dir)
        shutil.move(os.path.join(os.getcwd(), "log.lammps"), os.path.join(target_dir, "log.lammps"))
        decoder = CustomDecoder(target_filename=os.path.join(target_dir, "log.lammps"), output_columns=['time', "force"])
        my_time=decoder.parse_sim_output()
        dumpfreq = 100
        timestep = 0.001
        time_incr = dumpfreq*timestep
        sim_time_values = my_time["time"]
        sim_force_values = my_time["force"]
        timestep /= 1000
        exp_data = pd.read_csv("hobson_exp_force_time.csv")
        exp_time=exp_data['time'].values
        exp_force=exp_data['force'].values
        exp_time=exp_time-exp_time[0]
        f = interp1d(exp_time, exp_force)
        force_list=list()
        time_list=list()
        time=0
        for i in range(len(sim_force_values)):
            if sim_force_values[i] !=0 and sim_force_values[i]!=sim_force_values[(i-1)]:
                force_list.append(sim_force_values[i])
                time_list.append(time)
                time = time + time_incr
        MSE = np.square(np.subtract(f(time_list),force_list)).mean() 
        RMSE = math.sqrt(MSE)
        print('RMSE:',RMSE)
        print('time increment:',time_incr)
        print("time at call : ", function_calls, " ", time_list)
        #function_calls =+ 1
        return RMSE


function_calls = 0

def main():
    #cur_rmse=compute_rmse()
    eta0=0.05
    kappa0=0.012
    eta_nuc=0.2
    kappa_nuc=0.045
    k12=1.5
    #k_nuc=4.69282032302755
    #k_ind=413397.459621556
    myargs = [eta0, kappa0, eta_nuc, kappa_nuc,k12]
    optim_result=minimize(compute_rmse, myargs, method="Nelder-Mead")
    print(optim_result)
    #res=minimize(compute_rmse, 
    #print(cur_rmse)

if __name__ == "__main__":
    main()
