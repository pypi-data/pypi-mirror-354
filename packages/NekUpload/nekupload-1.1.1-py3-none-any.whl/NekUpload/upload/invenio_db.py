from __future__ import annotations
from typing import Any
import requests
import logging
import os
from . import invenio_rdm_api as InvenioAPI
from NekUpload.metadata.data_types import ResourceType

# Note that all private functions will return requests.Response for flexibility and testing purposes
# Each member function is responsible for handling that requests.Response and parsing relevant data, stored in class files

#TODO Need to refactor
# 1. Relying on side effects to instantiate class is annoying
# 2. Keep the upload method? and also have builder methods if users want to customise the upload process?
# 3. In which case, need way of returning necessary information?
class InvenioRDM:
    """Responsible for InvenioRDM database upload logic.
    """
    def __init__(self) -> None:
        """Class initialiser
        """
        #instantiated after draft record is created
        self.record_id: str = None

        #community uuid extracted from get_community
        self.community_uuid: str = None

        #acquired after submitting request to community
        self.request_id: str = None

        #acquired after reserving doi during draft creation 
        self.doi: str=None
        self.record_link: str=None
        self.self_link: str=None

    def upload_files(self,url: str, token: str, file_paths: list[str], metadata: dict[str,Any],community_id: str,extra_comments:list[str]=None) -> None:  
        """Upload files to an InvenioRDM repository and submit to community for review. Full workflow.

        Args:
            url (str): Base URL to the InvenioRDM repository.  For example: "https://my-invenio-rdm.example.com"            
            token (str): User access token
            file_paths (list[str]): list of paths of files to be uploaded
            metadata (dict[str,Any]): Metadata to be uploaded
            community_id (str): Invenio community id for upload or slug
        """        
        #prevent mixup of files from previous uploads
        self._clear()

        self.create_record(url,token,file_paths,metadata)
        self.submit_to_community(url,token,community_id,extra_comments)

    def create_record(self,url: str, token: str, file_paths: list[str], metadata: dict[str,Any]):
        """Create a draft record with the files

        Args:
            url (str): _description_
            token (str): _description_
            file_paths (List[str]): _description_
            metadata (Dict[str,Any]): _description_
        """
        #create the draft
        create_record_response = InvenioAPI.create_draft_record(url,token,metadata)
        self._handle_create_draft_response(create_record_response)
        logging.info(f"Record draft {self.record_id} has been created.")

        #after creation of draft, if any api calls fail, clean up the draft to prevent clutter
        try: 
            #set up the file locations in the record
            file_name_list = [self._get_file_name(file) for file in file_paths]
            InvenioAPI.prepare_file_upload(url,token,self.record_id,file_name_list) #does batch
            logging.info(f"Draft {self.record_id} now ready for file uploads.")

            #some test instances don't have doi reservation capabilities
            try:
                doi_response = InvenioAPI.reserve_doi_draft(url,token,self.record_id)
                self._handle_doi_response(doi_response)
            except Exception:
                pass

            #upload each file and commit
            for file,filename in zip(file_paths,file_name_list):
                InvenioAPI.upload_file(url,token,self.record_id,file)
                InvenioAPI.commit_file_upload(url,token,self.record_id,filename)
                logging.info(f"File {file} has been uploaded and committed to record {self.record_id}")

        except Exception as e:
            InvenioAPI.delete_draft(url,token,self.record_id)
            logging.info(f"Record draft {self.record_id} has been deleted due to error: {e}")
            raise

    def submit_to_community(self,url:str,token:str,community_id:str,extra_comments:list[str]=None):
        """Submit draft record for community review

        Args:
            url (str): _description_
            token (str): _description_
            community_id (str): _description_
        """
        #now try submitting to community, if fails here, ask user to manuallyu submit to community
        try:
            #get community uuid, then submit record to communtiy for review
            community_request = InvenioAPI.get_community(url,token,community_id)
            self._handle_community_response(community_request)
            create_review_request_response = InvenioAPI.submit_record_to_community(url,token,self.community_uuid,self.record_id)
            self._handle_create_review_request_response(create_review_request_response)

            base_msg = "This record was submitted via the Nektar++ validation and upload pipeline"
            if extra_comments:
                for comment in extra_comments:
                    base_msg += f"<br> {comment}" #use html tag <br> for new line

            payload = {
                "content": base_msg,
                "format": "html"
            } #this is a comment for the reviewer as to what this record is
            
            InvenioAPI.submit_record_for_review(url,token,self.record_id,payload)
            logging.info(f"Record {self.record_id} has been submitted to community {self.community_uuid} for review")
        except Exception as e:
            logging.info(f"Failed to submit to community, please manually attempt on IvenioRDM, due to error: {e}")
            raise e

    @staticmethod
    def get_all_user_records(url:str,token:str) -> list[RecordMetadata]:
        """Get all records uploaded by user, draft or published. 

        Args:
            url (str): _description_
            token (str): _description_

        Returns:
            list[RecordMetadata]: _description_
        """
        
        try:
            response = InvenioAPI.get_all_user_drafts_and_records(url,token)
            data = response.json()
            
            hits: dict[str,Any] = data["hits"]["hits"]
            
            return InvenioRDM._process_get_records_hits_list(hits)
        except Exception as e:
            logging.info(f"Failed to retrieve user drafts and records due to error {e}")
            raise

    @staticmethod
    def get_all_community_records(url:str,community_slug:str) -> list[RecordMetadata]:
        """Get all records published in a community

        Args:
            url (str): _description_
            community_slug (str): _description_

        Returns:
            list[RecordMetadata]: _description_
        """

        try:
            response = InvenioAPI.get_community_records(url,community_slug)
            data = response.json()
            
            hits: dict[str,Any] = data["hits"]["hits"]

            return InvenioRDM._process_get_records_hits_list(hits)
        except Exception as e:
            logging.info(f"Failed to retrieve user drafts and records due to error {e}")
            raise

    @staticmethod
    def get_record_metadata(url:str,token:str,record_id:str) -> RecordMetadata:
        """Get record metadata. Both draft and published

        Args:
            url (str): _description_
            token (str): _description_
            record_id (str): _description_

        Returns:
            RecordMetadata: _description_
        """

        try:
            response = InvenioAPI.get_draft_record(url,token,record_id)
            data = response.json()
            
            return InvenioRDM._process_record(data)
        except Exception as e:
            logging.info(f"Failed to retrieve record {record_id}: {e}")
            raise

    @staticmethod
    def download_file(url:str,token:str,record_id:str,filename:str,target_directory:str) -> str:
        """Downloads a file from a record or draft

        Args:
            url (str): _description_
            token (str): _description_
            record_id (str): _description_
            filename (str): _description_

        Returns:
            str: Path to download location 
        """
        try:
            _,output_filename = InvenioAPI.download_draft_file(url,token,record_id,filename,target_directory)

            return output_filename
        except Exception as e:
            logging.info(f"Failed to download file {filename} from record {record_id}: {e}")
            raise e

    def _get_community_uuid(self) -> str:
        """Get community UUID

        Returns:
            str: Community UUID
        """
        return self.community_uuid

    def _get_file_name(self,file_path: str) -> str:
        """Given a file path, extract the file name

        Args:
            file_path (str): Path to file

        Returns:
            str: File name
        """
        file_name = os.path.basename(file_path)
        return file_name

    def _handle_create_draft_response(self,response: requests.Response) -> None:
        """Handles response from creation of draft. Reads useful information into class variables

        Args:
            response (requests.Response): Create draft response
        """
        data = response.json()
        self.record_id = data["id"]
        self.record_link = data["links"]["record_html"]
        self.self_link = data["links"]["self_html"]

    def _handle_community_response(self,response: requests.Response) -> None:
        """Handles get community request response

        Args:
            response (requests.Response): Get Community response
        """
        data = response.json()
        self.community_uuid = data["id"]

    def _handle_doi_response(self,response: requests.Response) -> None:
        """Handles the doi reservation request response

        Args:
            response (requests.Response): DOI reservation request response
        """
        data: dict[str,Any] = response.json()
        
        self.doi = data["pids"]["doi"]["identifier"]
        self.record_link = data["links"]["record_html"]
        self.self_link = data["links"]["self_html"]

    def _handle_create_review_request_response(self,response: requests.Response) -> None:
        """Handles create review request response

        Args:
            response (requests.Response): Create review request response
        """
        data = response.json()
        self.request_id = data["id"]

    def _clear(self) -> None:
        """Reset internal state of the invenioRDM uploader
        """
        self.record_id = None
        self.community_uuid = None
        self.request_id = None
        self.doi = None
        self.record_link = None
        self.self_link = None

    @staticmethod
    def _process_get_records_hits_list(hits: dict[str,Any]) -> list[RecordMetadata]:
        record_list: list[RecordMetadata] = []
        for hit in hits:
            record_id: str = hit["id"]
            record_link: str = hit["links"]["self_html"]
            is_draft: bool = hit["is_draft"]
            is_published: bool = hit["is_published"]
            resource_type: str = hit["metadata"]["resource_type"]["id"]
            title: str = hit["metadata"]["title"]

            record_metadata = RecordMetadata(record_id,
                                            record_link,
                                            is_draft,
                                            is_published,
                                            resource_type,
                                            title)
            
            #add files if they exist
            files: dict[str,Any] = hit["files"]["entries"]
            file_list: list[str] = []
            for file in files.keys():
                file_list.append(file)
            record_metadata.add_files(file_list)

            #add doi if exists
            doi = hit["pids"].get("doi",None)
            if doi:
                id = doi["identifier"]
                record_metadata.add_doi(id)

            record_list.append(record_metadata)

        return record_list

    @staticmethod
    def _process_record(record: dict[str,Any]) -> RecordMetadata:
        hits = [record]
        record_list: list[RecordMetadata] = InvenioRDM._process_get_records_hits_list(hits)
        return record_list[0]

class RecordMetadata:
    def __init__(self,record_id: str,record_link: str,is_draft: bool,
                is_published: bool,resource_type: str,title: bool):
        self.record_id:str = record_id
        self.record_link:str = record_link
        self.is_draft:bool = is_draft
        self.is_published:bool = is_published
        self.resource_type:bool = resource_type
        self.title:bool = title

        #optional fields
        self.files: list[str] = []
        self.doi: str = "" 

    def add_files(self,files:list[str]) -> None:
        self.files = files

    def add_doi(self,doi:str) -> None:
        self.doi = doi

    def __str__(self) -> str:
        return f"Record ID: {self.record_id}"
    