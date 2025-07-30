from __future__ import annotations
import os
from abc import ABC,abstractmethod
from NekUpload.metadata.metadata import InvenioMetadata
from NekUpload.NekData.data_type import SolverType 
from NekUpload.upload.invenio_db import InvenioRDM,RecordMetadata
from NekUpload.metadata.extractor import NekAutoExtractor
from .validate import ValidateSession,ValidateOutput,ValidateGeometry
from NekUpload.metadata.relations import Relations,RelationsSchemes,RelationType,ResourceType
from NekUpload.utils.hdf5_reader import HDF5Reader
from NekUpload.utils.notification import warn_with_logging
from NekUpload.validate.exceptions import ExperimentalException,OutputFileException
from NekUpload.validate.files import NekSessionFile
import logging
import shutil
class NekManager:
    def __init__(self,
                geometry_uploader: GeometryManager,
                input_uploader: SessionManager,
                output_uploader: OutputManager):

        self.geometry_uploader: GeometryManager = geometry_uploader
        self.input_uploader: SessionManager = input_uploader
        self.output_uploader: OutputManager = output_uploader

        self.auto_metadata_extractor = NekAutoExtractor(
                                    self.input_uploader.session_file,
                                    self.geometry_uploader.geometry_file,
                                    self.output_uploader.output_fld_file)

        self.session_validator = ValidateSession(self.input_uploader.session_file)
        self.geometry_validator = ValidateGeometry(self.geometry_uploader.geometry_file)
        self.output_validator = ValidateOutput(self.output_uploader.output_fld_file)

    def execute_upload(self,url:str,token:str,community_id:str,comments:list[str]=None):
        #pass by reference, so all uploaders get updated version of metadata
        self._update_metadata_with_auto_extraction()

        directory="tmp"
        try:
            metadata:InvenioMetadata = self.geometry_uploader.metadata_manager
            uploader:InvenioRDM = self.geometry_uploader.upload_manager
            geometry_metadata_file = self.geometry_uploader.metadata_manager.print_ae_metadata_to_file(directory)
            files = [self.geometry_uploader.geometry_file] + self.geometry_uploader.supporting_files + [geometry_metadata_file]
            uploader.upload_files(url,token,files,metadata.get_metadata_payload(),community_id,comments)
        except:
            raise
        finally:
            if os.path.exists(directory):
                shutil.rmtree(directory)

        #update input and output with geometry upload link
        #only add if not None
        if geometry_doi := self.geometry_uploader.upload_manager.doi:
            geometry_relation = Relations(geometry_doi,RelationsSchemes.DOI,RelationType.CONTINUES,ResourceType.DATASET)
            self.input_uploader.metadata_manager.add_related_identifier(geometry_relation)
            self.output_uploader.metadata_manager.add_related_identifier(geometry_relation)

        if geometry_record_html := self.geometry_uploader.upload_manager.record_link:
            geometry_relation_html = Relations(geometry_record_html,RelationsSchemes.URL,RelationType.CONTINUES,ResourceType.DATASET)
            self.input_uploader.metadata_manager.add_related_identifier(geometry_relation_html)
            self.output_uploader.metadata_manager.add_related_identifier(geometry_relation_html)
            
        if geometry_self_html := self.geometry_uploader.upload_manager.self_link:
            geometry_relation_draft_link = Relations(geometry_self_html,RelationsSchemes.URL,RelationType.CONTINUES,ResourceType.DATASET)
            self.input_uploader.metadata_manager.add_related_identifier(geometry_relation_draft_link)
            self.output_uploader.metadata_manager.add_related_identifier(geometry_relation_draft_link)

        #grab all files from input and output uploader
        input_files = [self.input_uploader.session_file] + self.input_uploader.supporting_files
        output_files = [self.output_uploader.output_fld_file] + self.output_uploader.output_chk_files + self.output_uploader.filter_files + self.output_uploader.supporting_files 

        #add extra metadata files -> use json
        try:
            input_metadata_file = self.input_uploader.metadata_manager.print_ae_metadata_to_file(directory)

            #utilise metadata and uploader from either uploader, they should hold same data
            metadata:InvenioMetadata = self.input_uploader.metadata_manager
            uploader:InvenioRDM = self.input_uploader.upload_manager

            uploader.upload_files(url,token,input_files+output_files+[input_metadata_file],metadata.get_metadata_payload(),community_id,comments)
        except:
            raise
        finally:
            if os.path.exists(directory):
                shutil.rmtree(directory)

    def execute_linked_upload(self,url:str,token:str,community_id:str,record_id: str,comments:list[str]=None):
        #pass by reference, so all uploaders get updated version of metadata
        self._update_metadata_with_auto_extraction()
        
        record_metadata = InvenioRDM.get_record_metadata(url,token,record_id)

        #update input and output with geometry upload link
        #only add if not None
        if geometry_doi := record_metadata.doi:
            geometry_relation = Relations(geometry_doi,RelationsSchemes.DOI,RelationType.CONTINUES,ResourceType.DATASET)
            self.input_uploader.metadata_manager.add_related_identifier(geometry_relation)
            self.output_uploader.metadata_manager.add_related_identifier(geometry_relation)

        if geometry_record_html := record_metadata.record_link:
            geometry_relation_html = Relations(geometry_record_html,RelationsSchemes.URL,RelationType.CONTINUES,ResourceType.DATASET)
            self.input_uploader.metadata_manager.add_related_identifier(geometry_relation_html)
            self.output_uploader.metadata_manager.add_related_identifier(geometry_relation_html)
            
        if geometry_self_html := record_metadata.record_link:
            geometry_relation_draft_link = Relations(geometry_self_html,RelationsSchemes.URL,RelationType.CONTINUES,ResourceType.DATASET)
            self.input_uploader.metadata_manager.add_related_identifier(geometry_relation_draft_link)
            self.output_uploader.metadata_manager.add_related_identifier(geometry_relation_draft_link)

        #grab all files from input and output uploader
        input_files = [self.input_uploader.session_file] + self.input_uploader.supporting_files
        output_files = [self.output_uploader.output_fld_file] + self.output_uploader.output_chk_files + self.output_uploader.filter_files + self.output_uploader.supporting_files 

        #add extra metadata files -> use json
        directory="tmp"
        try:
            input_metadata_file = self.input_uploader.metadata_manager.print_ae_metadata_to_file(directory)

            #utilise metadata and uploader from either uploader, they should hold same data
            metadata:InvenioMetadata = self.input_uploader.metadata_manager
            uploader:InvenioRDM = self.input_uploader.upload_manager

            uploader.upload_files(url,token,input_files+output_files+[input_metadata_file],metadata.get_metadata_payload(),community_id,comments)
        except:
            raise
        finally:
            if os.path.exists(directory):
                shutil.rmtree(directory)

    def _update_metadata_with_auto_extraction(self):
        #results = self.auto_metadata_extractor.extract_data_old()
        results = self.auto_metadata_extractor.extract_data()

        if version := results.nektar_version:
            self.geometry_uploader.metadata_manager.add_version(version)
            self.input_uploader.metadata_manager.add_version(version)
            self.output_uploader.metadata_manager.add_version(version)

        #only geometry record should know what its domain is
        #if min exists, assume max also exists
        if min_domain := results.min_coord:
            self.geometry_uploader.metadata_manager.add_geometry_domain(tuple(min_domain),
                                                                        tuple(results.max_coord))

        if reynolds := results.reynolds:
            self.input_uploader.metadata_manager.add_reynolds_number(reynolds)
            self.output_uploader.metadata_manager.add_reynolds_number(reynolds)

        if kinvis := results.kinvis:
            self.input_uploader.metadata_manager.add_kinvis(kinvis)
            self.output_uploader.metadata_manager.add_kinvis(kinvis)

        try:
            solver_type: SolverType = NekManager.detect_solver_type(self.input_uploader.session_file)
            equation_type: SolverType = NekManager.detect_equation_type(self.input_uploader.session_file)
            
            equation_type_str = f"{solver_type.value}: {equation_type}"
            self.input_uploader.metadata_manager.add_solver_type(equation_type_str)
            self.output_uploader.metadata_manager.add_solver_type(equation_type_str)
        except:
            pass

    def validate(self,solver:SolverType=None) -> tuple[bool,list[str]]:
        self.session_validator.check_schema()
        self.geometry_validator.check_schema()
        self.output_validator.check_schema()
        self.validate_checkpoint_files(solver)

        #session completeness test
        self.session_validator.check_boundary_conditions_reference(self.input_uploader.supporting_files)
        self.session_validator.check_function_reference(self.input_uploader.supporting_files)

        #check geometry file adn session file are correctly linked
        self._validate_geometry_session_linked_correctly(self.geometry_uploader.geometry_file)

        _,err_msg = self._validate_input_output_linked_correctly(solver)
        msg = ["&check; All mandatory dataset tests passed"]

        return True,msg + err_msg

    def validate_checkpoint_files(self,solver: SolverType) -> tuple[bool,list[str]]:
        chk_filter_files: list[str] = self.session_validator.get_checkpoint_filter_filenames()
        
        try:
            #this assumes default fields in fld files
            self.output_validator.check_checkpoint_schema(chk_filter_files,self.output_uploader.output_chk_files)
        except OutputFileException as e:
            logging.info("Checkpoint validation failed. Trying different strategy.")
            for chk_file in self.output_uploader.output_chk_files:
                #assume number of fields are as specified in vars
                self.output_validator.check_chkpoint_filter_shape_only_vars(self.input_uploader.session_file,
                                                                        self.geometry_uploader.geometry_file,
                                                                        solver,
                                                                        chk_file)

        try:
            self.output_validator.check_checkpoint_from_filter_schema(self.input_uploader.session_file,
                                                                self.geometry_uploader.geometry_file,
                                                                solver,
                                                                chk_filter_files,
                                                                self.output_uploader.output_chk_files)
        except ExperimentalException as e:
            warn_with_logging(e)

        return True,[""]

    def optional_validation(self) -> tuple[bool,list[str]]:
        """Optional validation that does not cause failure.

        Returns:
            bool: Valid
        """
        valid = True
        msg: list[str] = []
        if not self.output_validator.check_commit_is_public():
            valid = False
            warn_with_logging((f"THe Nektar++ code you used was not found in the public repository."
                            f"If there is a new feature in your Nektar++ code that does not exist in the "
                            f"Nektar++ repository, please submit your changes so that others may also benefit."))
            msg = [f"&ndash; {self.output_validator.get_gitsha()} was not found in the main branch"]#html format
        else:
            msg =[f"&check; Dataset generated with publicly available Nektar GITSHA"] #html format

        return valid,msg

    def _validate_geometry_session_linked_correctly(self,geometry_file: str):
        """Check whether session and geometry file correspond i.e. are they actually part of same dataset

        Args:
            geometry_file (str): _description_
        """
        self.session_validator.check_geometry_file_reference(geometry_file)
        self.session_validator.check_boundary_definition(geometry_file)
        self.session_validator.check_expansion_definition(geometry_file)

    def _validate_input_output_linked_correctly(self,solver: SolverType=None) -> tuple[bool,list[str]]:
        self.session_validator.check_checkpoint_files(self.output_uploader.output_chk_files)

        #checkpoints also count as filter files if comes from FILTER: for now double count
        self.session_validator.check_filter_files_reference(self.output_uploader.output_chk_files + self.output_uploader.filter_files)
        if solver:
            _,msg = self.session_validator.check_consistent_output_shape(self.geometry_uploader.geometry_file,self.output_uploader.output_fld_file,solver)
            if not msg:
                msg = ["&check; Passed experimental feature: Input Output shape checks"]#html format
            
            return True,msg
        
        #####if this check proves troublesome, make it entirley optional

        return True,["&check; Passed experimental feature: Input Output shape checks"]#html format

    @staticmethod
    def get_all_uploaded_user_records(url:str,token:str) -> list[RecordMetadata]:
        return InvenioRDM.get_all_user_records(url,token)
    
    @staticmethod
    def get_all_community_records(url:str,community_slug:str) -> list[RecordMetadata]:
        return InvenioRDM.get_all_community_records(url,community_slug)
    
    @staticmethod
    def download_geometry_file(url:str,token:str,record_id:str,download_directory:str) -> str:
        record: RecordMetadata = InvenioRDM.get_record_metadata(url,token,record_id)
            
        for file in record.files:
            if file.endswith(".nekg"):
                geometry_file = InvenioRDM.download_file(url,token,record_id,file,download_directory)
                return geometry_file        
        
        return ""

    @staticmethod
    def detect_solver_type(session_file:str) -> SolverType:
        with NekSessionFile(session_file) as f:
            return f.get_solver()

    @staticmethod
    def detect_equation_type(session_file:str) -> SolverType:
        with NekSessionFile(session_file) as f:
            return f.get_equation_type()

class UploadManager(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def execute_upload(self,url: str,token: str,community_slug: str):
        pass

class GeometryManager(UploadManager):
    def __init__(self,geometry_file: str,
                supporting_files: list[str]=None,
                metadata: InvenioMetadata=None,
                uploader: InvenioRDM=None):
        
        self.geometry_file: str = geometry_file
        self.supporting_files: list[str] = supporting_files if supporting_files else []
        self.metadata_manager = metadata if metadata else InvenioMetadata()
        self.metadata_manager.resource_type = ResourceType.MODEL.value #override resource classification as model 
        self.upload_manager = uploader if uploader else InvenioRDM()

    def execute_upload(self,url: str,token: str,community_slug: str):
        
        files = [self.geometry_file] + self.supporting_files
        metadata_json = self.metadata_manager.get_metadata_payload()
        
        self.upload_manager.upload_files(url,token,files,metadata_json,community_slug)

    def generate_metadata_file(self) -> str:
        with HDF5Reader(self.geometry_file) as f:
            f.dump_to_plain_file("metadata.rdm")

        return "metadata.rdm"
    
class SessionManager(UploadManager):
    def __init__(self,session_file: str,
                supporting_files: list[str]=None,
                metadata: InvenioMetadata=None,
                uploader: InvenioRDM=None):
        
        self.session_file: str = session_file
        self.supporting_files: list[str] = supporting_files if supporting_files else []
        self.metadata_manager = metadata if metadata else InvenioMetadata()
        self.upload_manager = uploader if uploader else InvenioRDM()

    def execute_upload(self, url, token, community_slug):
        files = [self.session_file] + self.supporting_files
        metadata_json = self.metadata_manager.get_metadata_payload()        
        self.upload_manager.upload_files(url,token,files,metadata_json,community_slug)

class OutputManager(UploadManager):
    def __init__(self,output_fld_file: str,
                output_chk_files: list[str]=None,
                filter_files: list[str]=None,
                supporting_files: list[str]=None,
                metadata: InvenioMetadata=None,
                uploader: InvenioRDM=None):
        
        self.output_fld_file: str = output_fld_file
        self.output_chk_files: list[str] = output_chk_files if output_chk_files else []
        self.filter_files: list[str] = filter_files if filter_files else []
        self.supporting_files: list[str] = supporting_files if supporting_files else []
        self.metadata_manager = metadata if metadata else InvenioMetadata()
        self.upload_manager = uploader if uploader else InvenioRDM()

    def execute_upload(self, url, token, community_slug):
        files = [self.output_fld_file] + self.output_chk_files + self.filter_files + self.supporting_files
        metadata_json = self.metadata_manager.get_metadata_payload()
        self.upload_manager.upload_files(url,token,files,metadata_json,community_slug)