# libraries
from laplace_server.get_ip import get_ip

# project
from laplace_opt.model_construction import ObjectiveStructure


class ElectronEnergyStd(ObjectiveStructure):
    '''
    Objective definition for the electron energy standard deviation.

    This class defines the optimization direction (minimize or maximize),
    the measurement address, the payload key, and the metadata associated 
    with the electron energy spread.
    '''
    def __init__(self, minimize: bool = True):
        '''
        Initialize the electron energy standard deviation objective.

        Args:
            minimize (bool):
                If True, the objective will be minimized.
                If False, the objective will be maximized.
        '''
        name = "electron_energy_std"
        unit = "MeV"
        
        description = "The spectrum energy standard deviation"
        symbol = r"$\sigma_E$"

        ip = get_ip(name="opt")
        port = "5556"

        output_key = "electron_energy_std"
        
        ObjectiveStructure.__init__(
            self, 
            name=name, 
            unit=unit, 
            minimize=minimize, 
            description=description, 
            symbol=symbol, 
            ip=ip, 
            port=port, 
            output_key=output_key
        )
