# libraries
from laplace_server.get_ip import get_ip

# project
from laplace_opt.model_construction import ObjectiveStructure


class ElectronCountsOut(ObjectiveStructure):
    '''
    Objective definition for the electron counts out.

    This class defines the optimization direction (minimize or maximize),
    the measurement address, the payload key, and the metadata associated 
    with the electron counts out.
    '''
    def __init__(self, minimize: bool = True):
        '''
        Initialize the electron counts out objective.

        Args:
            minimize (bool):
                If True, the objective will be minimized.
                If False, the objective will be maximized.
        '''
        name = "electron_count_out"
        unit = "pC"

        description = "The electron counts out"
        symbol = r"$Q_{Out}$"

        ip = get_ip(name="opt")
        port = "5558"

        output_key = "counts_out"

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
