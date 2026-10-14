# libraries
from typing import Sequence

# project
from laplace_opt.model_construction import InputStructure
from laplace_opt.utils.get_ip import get_local_ip


class GasJetLongitudinal(InputStructure):
    '''
    Input definition for the longitudinal position of the gas jet.

    This class defines the optimization bounds, safe operating bounds,
    hardware address, and metadata associated with the gas jet position
    along the propagation axis.
    '''
    def __init__(self, bounds: Sequence[float]=(0, 15)):
        '''
        Initialize the gas jet longitudinal input.

        Args:
            bounds (Sequence[float]):
                Optimization bounds (min, max) in micrometers.
                These define the search space limits.
        '''
        name = "gas_jet_longitudinal"
        unit = "um"
        safe_bounds = (-2.0, 10.0)

        ip_tmp = get_local_ip()
        ip = ip_tmp if ip_tmp else "0.0.0.0"
        port = "5555"

        description = "Position of the gas jet along the propagation axis."
        symbol = "z_gas"

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
