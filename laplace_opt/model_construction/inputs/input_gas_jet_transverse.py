# libraries
from typing import Sequence

from laplace_server.get_ip import get_ip

# project
from laplace_opt.model_construction import InputStructure


class GasJetTransverse(InputStructure):
    '''
    Input definition for the transver position of the gas jet.

    This class defines the optimization bounds, safe operating bounds,
    hardware address, and metadata associated with the gas jet position
    along the transverse axis.
    '''
    def __init__(self, bounds: Sequence[float]=(0, 15)):
        '''
        Initialize the gas jet transerse input.

        Args:
            bounds (Sequence[float]):
                Optimization bounds (min, max) in millimeters.
                These define the search space limits.
        '''
        
        name = "gas_jet_transverse"
        unit = "um"
        safe_bounds = (0.0, 15.0)

        ip_tmp = get_ip(name="opt")
        ip = ip_tmp if ip_tmp else "0.0.0.0"
        port = "5555"

        description = "Transverse position of the gas jet."
        symbol = "x_gas"

        position_index = 2
        
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
