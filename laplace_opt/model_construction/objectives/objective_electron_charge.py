# project
from laplace_opt.model_construction import ObjectiveStructure
from laplace_opt.utils.get_ip import get_local_ip


class ElectronCharge(ObjectiveStructure):
    '''
    Objective definition for the electron beam charge.

    This class defines the optimization direction (minimize or maximize),
    the measurement address, the payload key, and the metadata associated 
    with the electron beam charge.
    '''
    def __init__(self, minimize: bool = False):
        '''
        Initialize the electron charge objective.

        Args:
            minimize (bool):
                If True, the objective will be minimized.
                If False, the objective will be maximized.
        '''
        name = "electron_charge"
        unit = "pC"

        description = "The electron charge"
        symbol = r"$Q$"

        ip_tmp = get_local_ip()
        ip = ip_tmp if ip_tmp else "0.0.0.0"
        port = "5556"

        output_key = "electron_charge"

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
