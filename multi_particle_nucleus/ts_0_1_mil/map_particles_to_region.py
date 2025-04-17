from ovito.data import *
import numpy as np 

def modify(frame: int, data: DataCollection):
    
    # https://www.ovito.org/docs/current/python/modules/ovito_data.html#ovito.data.SurfaceMesh.locate_point
    mesh = data.surfaces['surface']
    particle_region = data.particles_.create_property("Region", components = 1, data = 0)
    for i, pos in enumerate(data.particles.positions):
        yield i/data.particles.count
        particle_region[i] = mesh.locate_point(pos)
        
    particle_count = np.bincount(data.particles["Region"][:], minlength = mesh.regions.count)    
    for region in range(mesh.regions.count):
        print(f"Region ID {region} contains {particle_count[region]} particles.")
        
           