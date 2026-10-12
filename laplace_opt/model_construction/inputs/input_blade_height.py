# libraries
from typing import Sequence

# project
from laplace_opt.model_construction import InputStructure
from laplace_opt.utils.get_ip import get_local_ip


class BladeHeight(InputStructure):
    '''
    Input definition for the vertical position of the blade.

    This class specifies the optimization bounds, safe operating bounds,
    hardware address, and metadata associated with the blade height
    control parameter.
    '''
    def __init__(self, bounds: Sequence[float]=(150, 15000)):
        '''
        Initialize the blade height input.

        Args:
            bounds (Sequence[float]): 
                Optimization bounds (min, max) in micrometers.
                These define the search space limits.
        '''
        name = "blade_height"
        unit = "um"
        safe_bounds = (100, 25000)

        ip_tmp = get_local_ip()
        ip = ip_tmp if ip_tmp else "0.0.0.0"
        port = "5555"
        
        description = "Vertical position of the blade."
        symbol = "y_blade"

        position_index = 10
        
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
