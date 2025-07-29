import requests
from typing import Optional, Dict, Any, List
import json
import json as json_lib
import gzip

class MassStats:
    def __init__(self, base_url: str, api_key: str, verify: bool = True, timeout: int = 60):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.verify = verify
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': self.api_key
        })

    def _upload_file(self, file_path: str, url: str, use_gzip: bool = False):
        """
        Helper method to upload a JSON file to a signed URL.
        
        Args:
            file_path: Path to the JSON file
            url: Signed URL to upload to
            use_gzip: Whether to compress the file with gzip
        """
        try:
            with open(file_path, 'r') as file:
                json_data = json_lib.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {file_path}: {e}")
        
        # Check if using simplejson and support ignore_nan
        if hasattr(json_lib, 'dumps') and 'ignore_nan' in json_lib.dumps.__code__.co_varnames:
            dumps_kwargs = {'ignore_nan': True}
        else:
            dumps_kwargs = {}
        
        if use_gzip:
            # Serialize and compress the JSON data
            body = gzip.compress(json_lib.dumps(json_data, **dumps_kwargs).encode('utf-8'))
            headers = {
                'Content-Type': 'application/json',
                'Content-Encoding': 'gzip'
            }
        else:
            body = json_lib.dumps(json_data, **dumps_kwargs).encode('utf-8')
            headers = {
                'Content-Type': 'application/json'
            }
        
        # Make the PUT request to the signed URL
        response = requests.put(
            url,
            data=body,
            headers=headers
        )
        
        return response
    

    def download_file(self, job_name: str, bucket:str, file_name: str, output_path: str) -> str:
        """
        Download a file from mass_stats using job name and file name.
        
        Args:
            job_name: Name of the job
            file_name: Name of the file to download
            output_path: Path where the file should be saved
            
        Returns:
            str: Path to the downloaded file
        """
        import os
        from pathlib import Path
        
        endpoint_url = f"{self.base_url}/mass_stats/download_files"
        request_body = {
            "job_name": job_name,
            "bucket": bucket,
            "file_name": file_name
        }
        
        try:
            # Get signed URL
            response = self.session.post(
                endpoint_url, 
                json=request_body, 
                verify=self.verify, 
                timeout=self.timeout
            )
            signed_url = response.json().get('download_url')
            if not signed_url:
                raise Exception("No download URL received from server")    
            print(f"Generated signed URL for download")
            
            # Create output directory if it doesn't exist
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Download the file using the signed URL
            download_response = self.session.get(
                signed_url,
                verify=self.verify,
                timeout=self.timeout,
                stream=True  # Stream for large files
            )
            download_response.raise_for_status()

            # Check if file exists in the response (content-length header)
            content_length = download_response.headers.get('content-length')
            if content_length and int(content_length) == 0:
                raise Exception("File appears to be empty")
            
            # Write the file
            with open(output_path, 'wb') as file:
                for chunk in download_response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            
            # Verify file was written
            if not os.path.exists(output_path):
                raise Exception(f"File was not written to {output_path}")
                
            file_size = os.path.getsize(output_path)
            print(f"File downloaded successfully to {output_path} (size: {file_size / (1024 * 1024):.4f} mb)")
            
            return output_path
            
        except self.session.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                error_detail = e.response.text
                raise Exception(f"Error getting signed URL: {e}. Details: {error_detail}")
            raise Exception(f"Error in download process: {e}")
        except IOError as e:
            raise Exception(f"Error writing file to {output_path}: {e}")
        except Exception as e:
            # Clean up partial file if it exists
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass
            raise
    



    def upload_request(
        self,
        name: str,
        size: int,
        region: List[str],
        output: str,
        config: Dict[str, Any],
        location: Optional[str] = None,
        force_loc: Optional[bool] = None,
        overwrite: bool = False,
        server: Optional[str] = None,
        skip_existing: bool = False,
    ) -> Dict[str, Any]:
        """
        Initiate a mass stats upload job.
        
        Args:
            name: Name of the job
            size: Size of the job
            region: Region to run job [aus, eu, us]
            output: Output type
            config: Configuration dictionary
            location: (Optional) Location for the upload
            force_loc: Force location usage
            overwrite: Overwrite existing data
            server: Optional server
            skip_existing: Skip existing files
        """
        

        
        # Step 2: Create the upload job and get signed URLs
        url = f"{self.base_url}/mass_stats/upload"
        
        data = {
            "name": name,
            "size": size,
            "region": region,
            "output": output,
            "config": config,
            "overwrite": overwrite,
            "skip_existing": skip_existing
        }
        
        if location is not None:
            data["location"] = location
        if force_loc is not None:
            data["force_loc"] = force_loc
        if server is not None:
            data["server"] = server
        response = self.session.post(
            url, 
            json=data, 
            verify=self.verify, 
            timeout=self.timeout
        )      
        return response.json()



    
    def execute_job(
        self,
        name: str,
        region: str,
        output: str,
        config: Dict[str, Any],
        overwrite: bool = False,
        skip_existing: bool = False,
        request_json: Optional[str] = None,
        manifest_json: Optional[str] = None,
        location: Optional[str] = None,
        force_loc: Optional[bool] = None,
        server: Optional[str] = None
    ) -> Dict[str, Any]:
        # Step 1: Calculate size from request JSON file if provided
        size = 0
        if request_json is not None:
            try:
                with open(request_json, 'r') as file:
                    request_data = json_lib.load(file)
                
                if isinstance(request_data, list):
                    size = len(request_data)
                else:
                    raise ValueError(f"Request JSON file {request_json} should contain a list of dictionaries")
                    
            except FileNotFoundError:
                raise FileNotFoundError(f"Request JSON file not found: {request_json}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in request file {request_json}: {e}")
            
        upload_result = self.upload_request(name, size, region, output, config, location, force_loc, overwrite, server, skip_existing)
        
        # Step 3: Upload JSON files if provided
        if request_json is not None or manifest_json is not None:
            requests_url = upload_result.get('requests_url')
            manifest_url = upload_result.get('manifest_url')
            
            if request_json is not None:
                if not requests_url:
                    raise ValueError("No requests_url returned from server for request JSON upload")
                
                try:
                    requests_response = self._upload_file(request_json, requests_url, use_gzip=True)
                    if requests_response.status_code not in [200, 201, 204]:
                        print(f"Requests upload error: {requests_response.text}")
                        raise Exception(f"Failed to upload request JSON: {requests_response.text}")
                except Exception as e:
                    raise Exception(f"Error uploading request JSON file {request_json}: {e}")
            
            if manifest_json is not None:
                if not manifest_url:
                    raise ValueError("No manifest_url returned from server for manifest JSON upload")
                
                try:
                    manifest_response = self._upload_file(manifest_json, manifest_url, use_gzip=False)
                    if manifest_response.status_code not in [200, 201, 204]:
                        print(f"Manifest upload error: {manifest_response.text}")
                        raise Exception(f"Failed to upload manifest JSON: {manifest_response.text}")
                except Exception as e:
                    raise Exception(f"Error uploading manifest JSON file {manifest_json}: {e}")
            

        start_job_task_id =self.start_job(upload_result.get("id"))
        return start_job_task_id


    def start_job(self, task_id: str) -> Dict[str, Any]:
        """
        Start a mass stats job by task ID.
        """
        url = f"{self.base_url}/mass_stats/start/{task_id}"
        response = self.session.post(url, verify=self.verify, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_task_id(self, name: str, stage: str, uid: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the task ID for a mass stats job by name and stage (and optionally user ID).
        """
        url = f"{self.base_url}/mass_stats/job_id?name={name}&stage={stage}"
        if uid is not None:
            url += f"&uid={uid}"
        response = self.session.get(url, verify=self.verify, timeout=self.timeout)
        #print("response text is ", response.text)
        return response.json()

    def track_job(self, ids: Optional[list] = None) -> Dict[str, Any]:
        """
        Track the status of one or more mass stats jobs.
        If ids is None, gets progress for all of the user's jobs.
        """
        url = f"{self.base_url}/mass_stats/track"
        data = {"ids": ids} if ids is not None else {}
        response = self.session.post(url, json=data, verify=self.verify, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_history(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get the history of mass stats jobs.
        """
        url = f"{self.base_url}/mass_stats/history"
        params = {"limit": limit}
        response = self.session.get(url, params=params, verify=self.verify, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def start_post_processing(
        self,
        process_name: str,
        data_name: str,
        output: str,
        consumer_path: str,
        overwrite: bool = False
    ) -> Dict[str, Any]:
        """
        Start post processing for a mass stats job.
        Args:
            process_name: Folder to store output
            data_name: Name of job used to create data
            output: Output type
            consumer_path: Path to the post processing script (Python file)
            overwrite: Overwrite existing post processing output in same location
        Returns:
            Dict with task_id
        """
        url = f"{self.base_url}/mass_stats/post_process"
        files = {
            'consumer': (consumer_path, open(consumer_path, 'rb'), 'text/x-python')
        }
        data = {
            'process_name': process_name,
            'data_name': data_name,
            'output': output,
            'overwrite': str(overwrite).lower()
        }
        response = self.session.post(url, data=data, files=files, verify=self.verify, timeout=self.timeout)
        print("the response is ", response.text)
        # response.raise_for_status()
        return response.json()

    def download_results(
        self,
        id: Optional[str] = None,
        force_loc: bool = False,
        bucket: Optional[str] = None,
        location: Optional[str] = None,
        output: Optional[str] = None,
        file_name: Optional[str] = None
    ) -> bytes:
        """
        Download results from a mass stats job or arbitrary results if force_loc is True.
        Returns the content of the .zip file.
        """
        url = f"{self.base_url}/mass_stats/download"
        data = {}
        if id is not None:
            data["id"] = id
        if force_loc:
            data["force_loc"] = True
            if bucket is not None:
                data["bucket"] = bucket
            if location is not None:
                data["location"] = location
            if output is not None:
                data["output"] = output
        if file_name is not None:
            data["file_name"] = file_name
        response = self.session.post(url, json=data, verify=self.verify, timeout=self.timeout)
        print("the response is ", response.text)
        # response.raise_for_status()
        print("the response content is ", response.content)
        return response.content

    def cancel_job(self, id: str) -> Dict[str, Any]:
        """
        Cancel a mass stats job by ID.
        """
        url = f"{self.base_url}/mass_stats/cancel/{id}"
        response = self.session.post(url, verify=self.verify, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def cancel_all_jobs(self) -> Dict[str, Any]:
        """
        Cancel all mass stats jobs for the user.
        """
        url = f"{self.base_url}/mass_stats/cancel"
        response = self.session.post(url, verify=self.verify, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def create_pyramids(self, name: str, levels: int, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create pyramids for a dataset.
        Args:
            name: Name for the pyramid job
            levels: Number of zoom levels to compute
            config: Dataset config (mapping)
        Returns:
            Dict with task_id
        """
        url = f"{self.base_url}/pyramids/create"
        data = {
            "name": name,
            "levels": levels,
            "config": config
        }
        response = self.session.post(url, json=data, verify=self.verify, timeout=self.timeout)
        print("the url is   ", url)
        print("the response is ", response.text)
        print("the response status code is ", response.status_code)
        # response.raise_for_status()
        return response.json()

    def random_sample(
        self,
        name: str,
        config: dict,
        aoi: dict,
        samples: int,
        year_range: list,
        crs: str,
        tile_size: int,
        res: float,
        output: str,
        server: str,
        region: str,
        bucket: str,
        overwrite: bool = False
    ) -> Dict[str, Any]:
        """
        Submit a random sample job.
        """
        if year_range is None or len(year_range) != 2:
            raise ValueError("year_range must be a list of two integers")
        start_year, end_year = year_range
        if start_year is None or end_year is None:
            raise ValueError("Both start_year and end_year must be provided for year_range.")

        url = f"{self.base_url}/random_sample"
        data = {
            "name": name,
            "overwrite": overwrite,
            "config": config,
            "aoi": aoi,
            "samples": samples,
            "year_range": [start_year, end_year],
            "crs": crs,
            "tile_size": tile_size,
            "res": res,
            "output": output,
            "server": server,
            "region": region,
            "bucket": bucket
        }
        print("the data is ", data)
        print("the url is ", url)
        response = self.session.post(url, json=data, verify=self.verify, timeout=self.timeout)
        print("Status code:", response.status_code)
        print("Response text:", response.text)
        # response.raise_for_status()
        return response.json() 


    ### Adding the wrapper function to call endpoint /mass_stats/combine_tiles
    def combine_tiles(
        self, 
        data_name: str,
        usezarr: bool = False,
        overwrite: bool = True,
        output : str = "netcdf"
    ) -> Dict[str, Any]:

        url = f"{self.base_url}/mass_stats/combine_tiles"
        request_body = {
            'data_name': data_name,
            'usezarr': str(usezarr).lower(),
            'output': output,
            'overwrite': str(overwrite).lower()
        }
        print(f"Request body: {json.dumps(request_body, indent=2)}")
        response = self.session.post(url, json=request_body, verify=self.verify, timeout=self.timeout)
        print(f"Response text: {response.text}")
        return response.json()



  


    
