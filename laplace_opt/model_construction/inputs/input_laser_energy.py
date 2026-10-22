# libraries
from typing import Sequence

from laplace_server.get_ip import get_ip

# project
from laplace_opt.model_construction import InputStructure


class LaserEnergy(InputStructure):
    '''
    Input definition for the laser energy parameter.

    This class defines the optimization bounds, safe operating bounds,
    hardware address, and metadata associated with the laser energy
    control variable.
    '''
    def __init__(self, bounds: Sequence[float]=(0, 5)):
        '''
        Initialize the laser energy input.

        Args:
            bounds (Sequence[float]):
                Optimization bounds (min, max) in joules.
                These define the search space limits.
        '''
        name = "laser_energy"
        unit = "J"
        safe_bounds = (0.0, 100.0)

        ip = get_ip(name="opt")
        port = "5556"

        description = "Laser energy"
        symbol = "E_laser"

        position_index = 1
        
        InputStructure.__init__(
            self, 
            name=name, 
            bounds=bounds, 
            safe_bounds=safe_bounds, 
            unit=unit, 
            ip=ip,
            port=port,
            description=description,
            symbol=symbol,
            position_index=position_index
        )
