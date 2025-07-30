from NekUpload.NekData.data_type import SolverType
from NekUpload.NekData.config import EQUATION_TYPE_TO_SOLVER,EQUATION_TYPE_TO_FIELD_VARS_1D,EQUATION_TYPE_TO_FIELD_VARS_2D,EQUATION_TYPE_TO_FIELD_VARS_3D

class SolverInfo:
    def __init__(self,solver: SolverType,dimension: int,equation_type: str):
        self.solver: SolverType = solver
        self.dimension: int = dimension
        self.equation_type: str = equation_type

    def get_var_num(self) -> int:
        return len(_get_variables(self.equation_type,self.dimension))

_mapping: dict[str,list[list[str]]] = {1: EQUATION_TYPE_TO_FIELD_VARS_1D,
                                2: EQUATION_TYPE_TO_FIELD_VARS_2D,
                                3: EQUATION_TYPE_TO_FIELD_VARS_3D}

def _get_variables(equation_type: str,dim: int) -> list[str]:
    try:
        result = _mapping[dim][equation_type]
        return result
    except KeyError as e:
        if equation_type in EQUATION_TYPE_TO_SOLVER:
            raise NotImplementedError(msg=f"Equation Type {equation_type} {dim}D field variables have not been listed in the nektar.yaml configuration file")
        else:
            raise KeyError(e)
