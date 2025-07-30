import yaml
import os
from typing import Any
from NekUpload.NekData.data_type import SolverType

class NektarSolverConfig:
    def __init__(self,solver: str,equation_types:list[str]):
        self.solver_type = SolverType(solver)
        self.equation_types:list[str] = equation_types
        self.equation_type_field_vars: dict[str,list[list[str]]] = {}

    def add_variables(self,equation_type:str,var_1d: list[str], var_2d: list[str], var_3d: list[str]):

        field_variables_1d: list[str] = list(var_1d)
        field_variables_2d: list[str] = list(var_2d) 
        field_variables_3d: list[str] = list(var_3d) 
        self.equation_type_field_vars[equation_type] = [field_variables_1d,field_variables_2d,field_variables_3d] 

    def get_field_vars(self,equation_type: str,dim:int) -> list[str]:
        """

        Args:
            dim (int): 1,2,3 dimensional

        Returns:
            list[str]: _description_
        """
        field_vars = self.equation_type_field_vars.get(equation_type,[])

        if field_vars:
            return field_vars[dim-1]
        else:
            return []

    def __repr__(self):
        return f"NektarSolverConfig(solver_type={self.solver_type}, equation_types={self.equation_types})"

NEKTAR_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'nektar.yaml') #ensure path always correct

def _load_config(file_path: str=NEKTAR_CONFIG_FILE) -> list[NektarSolverConfig]:
    """Loads the config file containing Nektar solver setting information

    Args:
        file_path (str, optional): _description_. Defaults to NEKTAR_CONFIG_FILE.

    Returns:
        list[DatabaseConfig]: list of sepcified database configs
    """
    with open(file_path,"r") as file:
        raw_config: dict[str,Any] = yaml.safe_load(file)

    return _generate_nektar_solver_config_list(raw_config)

def _generate_nektar_solver_config_list(yaml_content:dict[str,Any]) -> list[NektarSolverConfig]:
    """Given a yaml dict, generate the nektar solver config. Adds custom defaults in.

    Args:
        yaml_content (dict[str,Any]): _description_

    Returns:
        list[NektarSolverConfig]: list of nektar solver configurations
    """
    solvers = []

    for solver_info in yaml_content.get("solvers",[]):
        for solver,item in solver_info.items():
            equations:list[str] = item["EQTYPE"]
            solver_config = NektarSolverConfig(solver,equations)

            variables: dict[str,Any] = item.get("VARIABLES",[])
            if variables:
                for variable_def in variables:
                    for key,value in variable_def.items():
                        if key == "ALL":
                            for eq in equations:
                                solver_config.add_variables(eq,value["1D"],value["2D"],value["3D"])
                        else:
                            #if targeting specific equation types
                            solver_config.add_variables(key,value["1D"],value["2D"],value["3D"])

            solvers.append(solver_config)
    return solvers

#useful values
#only need to calculate these once, then other files can load them in when needed
SOLVERS: list[NektarSolverConfig] = _load_config()
def _generate_map()->dict[str,SolverType]:
    mapping = {}
    for solver in SOLVERS:
        for eq in solver.equation_types:
            mapping[eq] = solver.solver_type

    return mapping
EQUATION_TYPE_TO_SOLVER: dict[str,SolverType] = _generate_map()

def _generate_field_vars(dim:int) -> dict[str,list[str]]:
    mapping = {}
    for solver in SOLVERS:
        for eq in solver.equation_types:
            if field_vars := solver.get_field_vars(eq,dim):
                mapping[eq] = field_vars

    return mapping

EQUATION_TYPE_TO_FIELD_VARS_1D: dict[str,list[str]] = _generate_field_vars(1)
EQUATION_TYPE_TO_FIELD_VARS_2D: dict[str,list[str]] = _generate_field_vars(2)
EQUATION_TYPE_TO_FIELD_VARS_3D: dict[str,list[str]] = _generate_field_vars(3)
