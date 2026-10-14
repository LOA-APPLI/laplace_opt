# project
from laplace_opt.model_construction import ObjectiveStructure
from laplace_opt.utils.get_ip import get_local_ip


class ElectronCountsIn(ObjectiveStructure):
    '''
    Objective definition for the electron counts in.

    This class defines the optimization direction (minimize or maximize),
    the measurement address, the payload key, and the metadata associated 
    with the electron counts in.
    '''
    def __init__(self, minimize: bool = False):
        '''
        Initialize the electron counts in objective.

        Args:
            minimize (bool):
                If True, the objective will be minimized.
                If False, the objective will be maximized.
        '''
        name = "electron_count_in"
        unit = "pC"

        description = "The electron counts in"
        symbol = r"$Q_{In}$"

        ip_tmp = get_local_ip()
        ip = ip_tmp if ip_tmp else "0.0.0.0"
        port = "5556"

        output_key = "counts_in"

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
