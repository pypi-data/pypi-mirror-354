from typing import Any
from .user import InvenioUserInfo,InvenioUserInfoFactory
from .relations import Relations
from .data_types import ResourceType
import json
import os

class InvenioMetadata:
    """Metadata model for handling metadata as prescribed in InvenioRDM. Uses a builder OOP style to 
    allow clients to enhance the metadata description.
    """
    def __init__(self,title: str,
                publication_date:str,
                creators: list[InvenioUserInfo],
                resource_type: ResourceType=ResourceType.DATASET):
        """Class Initialiser

        Args:
            title (str): Title of file uploads
            publication_date (str): Date of publication, in format YYYY-MM-DD
            creators (list[InvenioUserInfo]): list of authors
            resource_type (ResourceType, optional): Type of resource to be uploaded. Defaults to ResourceType.DATASET.
        """
        #mandatory fields
        self.title = title
        self.publication_date = publication_date
        self.creators: list[InvenioUserInfo] = creators
        self.resource_type = resource_type.value

        #optional fields
        self.version: str = None
        self.description: str = None
        self.publisher: str = None
        self.related_identifiers: list[Relations] = []

        #optional enhance AE Datastore only 
        self.reynolds: float | None= None
        self.geometry_domain_max: tuple[int,int,int] = None
        self.geometry_domain_min: tuple[int,int,int] = None
        self.solver_type: str = None
        self.kinvis: float | None = None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, InvenioMetadata):
            return False
        
        return (self.title == other.title and
                self.publication_date == other.publication_date and
                self.creators == other.creators and
                self.resource_type == other.resource_type and
                self.version == other.version and
                self.description == other.description and
                self.publisher == other.publisher and
                self.related_identifiers == other.related_identifiers)
    
    def __repr__(self):
        main_repr = (f"Title: {self.title}, "
                f"Publication Date: {self.publication_date}, "
                f"Creators: {[creator.name for creator in self.creators]}, "
                f"Resource Type: {self.resource_type}")

        if self.version:
            main_repr += f", Version: {self.version}"
        
        if self.description:
            main_repr += f", Description: {self.description}"
        
        if self.publisher:
            main_repr += f", Publisher: {self.publisher}"
        
        if self.related_identifiers:
            main_repr += f", Related Identifiers: {[relation.identifier for relation in self.related_identifiers]}"

        return main_repr

    def get_metadata_payload(self) -> dict[str,Any]:
        """Get the metadata payload formatted in way InvenioRDM expects

        Returns:
            dict[str,Any]: Metadata json payload
        """
        creators_payload: list[dict[str,Any]] = [{"person_or_org": creator.get_info()} for creator in self.creators]
        
        data = {
            "title": self.title,
            "publication_date": self.publication_date,
            "resource_type": {"id": self.resource_type},
            "creators": creators_payload
        }

        #only add to payload if they exist
        if self.version:
            data["version"] = self.version
        
        if self.description:
            data["description"] = self.description

        if self.publisher:
            data["publisher"] = self.publisher

        if self.related_identifiers:
            relation_list_json = [relation.to_json() for relation in self.related_identifiers]
            data["related_identifiers"] = relation_list_json

        data = self._add_ae_datastore_params(data)

        return data

    #TODO not sure if actually modelling this correctly
    def _add_ae_datastore_params(self,data) -> dict[str,Any]:
        data["domain-metadata"] = {} #this holds custom metadata in AE Datastore
        domain = data["domain-metadata"]

        if self.reynolds:
            if "reference-values" not in domain:
                domain["reference-values"] = {}
            domain["reference-values"]["reynolds"] = self.reynolds

        if self.kinvis:
            if "reference-values" not in domain:
                domain["reference-values"] = {}
            domain["reference-values"]["kinvis"] = self.kinvis

        if self.geometry_domain_max:
            if "geometry" not in domain:
                domain["geometry"] = {}
            domain["geometry"]["min-domain"] = self.geometry_domain_min
            domain["geometry"]["max-domain"] = self.geometry_domain_max

        if self.solver_type:
            if "solver-info" not in domain:
                domain["solver-info"] = {}
            domain["solver-info"]["equation-type"] = self.solver_type

        return data

    def add_version(self, version: str) -> None:
        """Add the version number (of the software or dataset). Semantic versioning is recommended.

        Args:
            version (str): Version number
        """
        self.version = version

    def add_description(self, description: str) -> None:
        """Add a description of the record to be uploaded

        Args:
            description (str): Description
        """
        self.description = description

    def add_publisher(self, publisher: str="InvenioRDM") -> None:
        """Add publisher 

        Args:
            publisher (str, optional): Add publisher name. Defaults to "InvenioRDM".
        """
        self.publisher = publisher

    def add_related_identifier(self,relation: Relations):
        """Add related persistent identifiers

        Args:
            relation (Relations): A related identifier
        """
        self.related_identifiers.append(relation)

    def add_reynolds_number(self,reynolds: float) -> None:
        """Add reynolds number of flow

        Args:
            reynolds (float): _description_
        """
        self.reynolds = reynolds

    def add_geometry_domain(self,min_coord: tuple[int,int,int],max_coord: tuple[int,int,int]):
        """Add domian of goemetyr

        Args:
            min_coord (tuple[int,int,int]): _description_
            max_coord (tuple[int,int,int]): _description_
        """
        self.geometry_domain_min = min_coord
        self.geometry_domain_max = max_coord

    def add_solver_type(self,solver_type: str):
        self.solver_type = solver_type

    def add_kinvis(self,kinvis: float):
        self.kinvis=kinvis

    def to_json_serialisable(self) -> dict[str,Any]:        
        """Serialise the object as JSON

        Returns:
            dict[str,Any]: Serialised json object
        """
        data = {
            "title": self.title,
            "publication_date": self.publication_date,
            "resource_type": self.resource_type,
            "creators": [creator.to_json_serialisable() for creator in self.creators]
        }

        if self.version:
            data["version"] = self.version
        
        if self.description:
            data["description"] = self.description

        if self.publisher:
            data["publisher"] = self.publisher

        if self.related_identifiers:
            relation_list_json = [relation.to_json() for relation in self.related_identifiers]
            data["related_identifiers"] = relation_list_json

        if self.reynolds:
            data["reynolds"] = self.reynolds

        if self.kinvis:
            data["kinvis"] = self.kinvis

        if self.geometry_domain_min:
            data["geometry_domain_min"] = self.geometry_domain_min

        if self.geometry_domain_max:
            data["geometry_domain_max"] = self.geometry_domain_max

        if self.solver_type:
            data["solver_type"] = self.solver_type

        return data    
    
    @classmethod
    def from_json(cls,data: dict[str,Any]) -> 'InvenioMetadata':
        """Reconstruct object from JSON serialisation

        Args:
            data (dict[str,Any]): Serialised JSON data

        Returns:
            InvenioMetadata: Reconstructed object
        """
        title = data["title"]
        publication_date = data["publication_date"]
        resource_type: ResourceType = ResourceType(data["resource_type"])
        creators: list[InvenioUserInfo] = [InvenioUserInfoFactory.create_from_json(creator) for creator in data["creators"]]

        metadata = InvenioMetadata(title,publication_date,creators,resource_type)

        #only add the following optional data if present in serialisation
        if version := data.get("version",None):
            metadata.add_version(version)

        if description := data.get("description",None):
            metadata.add_description(description)

        if publisher := data.get("publisher",None):
            metadata.add_publisher(publisher)

        if related_identifiers := data.get("related_identifiers",None):
            for identifier_json in related_identifiers:
                metadata.add_related_identifier(Relations.from_json(identifier_json))

        if reynolds := data.get("reynolds",None):
            metadata.add_reynolds_number(reynolds)

        if kinvis := data.get("kinvis",None):
            metadata.add_reynolds_number(kinvis)
        
        if geometry_domain_min := data.get("geometry_domain_min"):
            metadata.geometry_domain_min = geometry_domain_min

        if geometry_domain_max := data.get("geometry_domain_max"):
            metadata.geometry_domain_max = geometry_domain_max

        if solver_type := data.get("solver_type"):
            metadata.add_solver_type(solver_type)

        return metadata
    
    def print_ae_metadata_to_file(self,target_directory:str) -> str:
        """Print AE Datastore specific metadata to file

        Args:
            target_directory (str): directory to store file

        Returns:
            str: Path to created file
        """
        data = {}
        data = self._add_ae_datastore_params(data)
        os.makedirs(target_directory, exist_ok=True)
        filename = os.path.join(target_directory, "metadata.json")
        with open(filename, "w") as file:  # Fixed: using open() function instead of string method
            json.dump(data, file, indent=4)

        return filename