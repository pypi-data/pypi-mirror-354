import json
import asyncio
from io import BytesIO
from typing import Dict, Any, Optional, Union
from functools import wraps

import requests
import aiohttp
import pandas as pd
import geopandas as gpd
import xarray as xr
import nest_asyncio
from shapely.geometry import shape, mapping
from shapely.geometry.base import BaseGeometry as ShapelyGeometry
from google.cloud import storage
from .exceptions import APIError, ConfigurationError
from .decorators import admin_only_params
import logging
import textwrap


def require_api_key(func):
    """
    Decorator to ensure an API key is available before a method can be executed.
    Will check for the presence of an API key before allowing the function to be called.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Check if the API key is set
        if not self.key:
            error_msg = "No API key found. Please provide an API key to use this client."
            if not self.quiet:
                print(error_msg)
                print("API key is required for this function.")
                print("You can set an API key by either:")
                print("1. Loading from a config file")
                print("2. Using the login() method: client.login(email='your-email@example.com', password='your-password')")
            raise ConfigurationError(error_msg)
            
        # Check if URL is set (required for API calls)
        if not self.url:
            if not self.quiet:
                print("API URL is not set. Using default API URL: https://api.terrak.io")
            self.url = "https://api.terrak.io"
            
        return func(self, *args, **kwargs)
    
    # Mark as decorated to avoid double decoration
    wrapper._is_decorated = True
    return wrapper


class BaseClient:
    def __init__(self, url: Optional[str] = None,
                auth_url: Optional[str] = "https://dev-au.terrak.io",
                quiet: bool = False, config_file: Optional[str] = None,
                verify: bool = True, timeout: int = 300):
        nest_asyncio.apply()
        self.quiet = quiet
        self.verify = verify
        self.timeout = timeout
        self.auth_client = None
        # Initialize session early to avoid AttributeError
        self.session = requests.Session()
        self.user_management = None
        self.dataset_management = None
        self.mass_stats = None
        self._aiohttp_session = None
        
        # if auth_url:
        #     from terrakio_core.auth import AuthClient
        #     self.auth_client = AuthClient(
        #         base_url=auth_url,
        #         verify=verify,
        #         timeout=timeout
        #     )
        self.url = url
        self.key = None
        
        # Load configuration from file
        from terrakio_core.config import read_config_file, DEFAULT_CONFIG_FILE
        
        if config_file is None:
            config_file = DEFAULT_CONFIG_FILE
        
        # Get config using the read_config_file function that now handles all cases
        config = read_config_file(config_file, quiet=self.quiet)
        
        # If URL is not provided, try to get it from config
        if self.url is None:
            self.url = config.get('url')
            
        # Get API key from config file (never from parameters)
        self.key = config.get('key')

        self.token = config.get('token')
        
        # Update auth_client with token if it exists
        if self.auth_client and self.token:
            self.auth_client.token = self.token
            self.auth_client.session.headers.update({
                "Authorization": self.token
            })
        
        # If we have a key, we're good to go even if not logged in
        if self.key:
            # If URL is missing but we have a key, use the default URL
            if not self.url:
                self.url = "https://api.terrak.io"
            print("the token is! ", self.token)
            print("the key is! ", self.key)
            # Update session headers with the key
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': self.key
            }
            
            # Only add Authorization header if token exists and is not None
            if self.token:
                headers['Authorization'] = self.token
                
            self.session.headers.update(headers)
            print("the session headers are ", self.session.headers)

            
            if not self.quiet and config.get('user_email'):
                print(f"Using API key for: {config.get('user_email')}")
                
            return

        # Check if we have the required configuration
        if not self.key:
            # No API key available - inform the user
            if not self.quiet:
                print("API key is required to use this client.")
                print("You can set an API key by either:")
                print("1. Loading from a config file")
                print("2. Using the login() method: client.login(email='your-email@example.com', password='your-password')")
            return
            
        self.url = self.url.rstrip('/')
        if not self.quiet:
            print(f"Using Terrakio API at: {self.url}")
            
        # Update the session headers with API key
        self.session.headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self.key
        })

    @property
    @require_api_key
    async def aiohttp_session(self):
        if self._aiohttp_session is None or self._aiohttp_session.closed:
            self._aiohttp_session = aiohttp.ClientSession(
                headers={
                    'Content-Type': 'application/json',
                    'x-api-key': self.key
                },
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._aiohttp_session

    @require_api_key
    async def wcs_async(self, expr: str, feature: Union[Dict[str, Any], ShapelyGeometry],
                        in_crs: str = "epsg:4326", out_crs: str = "epsg:4326",
                        output: str = "csv", resolution: int = -1, buffer: bool = False, 
                        retry: int = 3, **kwargs):
        """
        Asynchronous version of the wcs() method using aiohttp.
        
        Args:
            expr (str): The WCS expression to evaluate
            feature (Union[Dict[str, Any], ShapelyGeometry]): The geographic feature
            in_crs (str): Input coordinate reference system
            out_crs (str): Output coordinate reference system
            output (str): Output format ('csv' or 'netcdf')
            resolution (int): Resolution parameter
            buffer (bool): Whether to buffer the request (default True)
            retry (int): Number of retry attempts (default 3)
            **kwargs: Additional parameters to pass to the WCS request
            
        Returns:
            Union[pd.DataFrame, xr.Dataset, bytes]: The response data in the requested format
        """
        if hasattr(feature, 'is_valid'):
            from shapely.geometry import mapping
            feature = {
                "type": "Feature",
                "geometry": mapping(feature),
                "properties": {}
            }

        payload = {
            "feature": feature,
            "in_crs": in_crs,
            "out_crs": out_crs,
            "output": output,
            "resolution": resolution,
            "expr": expr,
            "buffer": buffer,
            "resolution": resolution,
            **kwargs
        }
        print("the payload is ", payload)
        request_url = f"{self.url}/geoquery"
        for attempt in range(retry + 1):
            try:
                session = await self.aiohttp_session
                async with session.post(request_url, json=payload, ssl=self.verify) as response:
                    if not response.ok:
                        should_retry = False
                        if response.status in [408, 502, 503, 504]:
                            should_retry = True
                        elif response.status == 500:
                            try:
                                response_text = await response.text()
                                if "Internal server error" not in response_text:
                                    should_retry = True
                            except:
                                should_retry = True
                        
                        if should_retry and attempt < retry:
                            continue
                        else:
                            error_msg = f"API request failed: {response.status} {response.reason}"
                            try:
                                error_data = await response.json()
                                if "detail" in error_data:
                                    error_msg += f" - {error_data['detail']}"
                            except:
                                pass
                            raise APIError(error_msg)
                    
                    content = await response.read()
                    
                    if output.lower() == "csv":
                        import pandas as pd
                        df = pd.read_csv(BytesIO(content))
                        return df
                    elif output.lower() == "netcdf":
                        return xr.open_dataset(BytesIO(content))
                    else:
                        try:
                            return xr.open_dataset(BytesIO(content))
                        except ValueError:
                            import pandas as pd
                            try:
                                return pd.read_csv(BytesIO(content))
                            except:
                                return content
                                
            except aiohttp.ClientError as e:
                if attempt == retry:
                    raise APIError(f"Request failed: {str(e)}")
                continue
            except Exception as e:
                if attempt == retry:
                    raise
                continue

    @require_api_key
    async def close_async(self):
        """Close the aiohttp session"""
        if self._aiohttp_session and not self._aiohttp_session.closed:
            await self._aiohttp_session.close()
            self._aiohttp_session = None

    @require_api_key
    async def __aenter__(self):
        return self

    @require_api_key
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_async()

    def signup(self, email: str, password: str) -> Dict[str, Any]:
        if not self.auth_client:
            from terrakio_core.auth import AuthClient
            self.auth_client = AuthClient(
                base_url=self.url,
                verify=self.verify,
                timeout=self.timeout
            )
            self.auth_client.session = self.session
        return self.auth_client.signup(email, password)

    def login(self, email: str, password: str) -> Dict[str, str]:

        if not self.auth_client:
            from terrakio_core.auth import AuthClient
            self.auth_client = AuthClient(
                base_url=self.url,
                verify=self.verify,
                timeout=self.timeout
            )
            self.auth_client.session = self.session
        try:
            # First attempt to login
            token_response = self.auth_client.login(email, password)
            
            # Only proceed with API key retrieval if login was successful
            if token_response:
                # After successful login, get the API key
                api_key_response = self.auth_client.view_api_key()
                self.key = api_key_response
                
                # Make sure URL is set
                if not self.url:
                    self.url = "https://api.terrak.io"
                
                # Make sure session headers are updated with the new key
                self.session.headers.update({
                    'Content-Type': 'application/json',
                    'x-api-key': self.key
                })
                
                # Set URL if not already set
                if not self.url:
                    self.url = "https://api.terrak.io"
                    self.url = self.url.rstrip('/')
                
                # Save email and API key to config file
                import os
                import json
                config_path = os.path.join(os.environ.get("HOME", ""), ".tkio_config.json")
                try:
                    config = {"EMAIL": email, "TERRAKIO_API_KEY": self.key}
                    if os.path.exists(config_path):
                        with open(config_path, 'r') as f:
                            config = json.load(f)
                        config["EMAIL"] = email
                        config["TERRAKIO_API_KEY"] = self.key
                        config["PERSONAL_TOKEN"] = token_response
                    
                    os.makedirs(os.path.dirname(config_path), exist_ok=True)
                    with open(config_path, 'w') as f:
                        json.dump(config, f, indent=4)
                    
                    if not self.quiet:
                        print(f"Successfully authenticated as: {email}")
                        print(f"Using Terrakio API at: {self.url}")
                        print(f"API key saved to {config_path}")
                except Exception as e:
                    if not self.quiet:
                        print(f"Warning: Failed to update config file: {e}")
            
            return {"token": token_response} if token_response else {"error": "Login failed"}
        except Exception as e:
            if not self.quiet:
                print(f"Login failed: {str(e)}")
            raise

    @require_api_key
    def refresh_api_key(self) -> str:
        # If we have auth_client and it has a token, refresh the key
        if self.auth_client and self.auth_client.token:
            self.key = self.auth_client.refresh_api_key()
            self.session.headers.update({'x-api-key': self.key})
            
            # Update the config file with the new key
            import os
            config_path = os.path.join(os.environ.get("HOME", ""), ".tkio_config.json")
            try:
                config = {"EMAIL": "", "TERRAKIO_API_KEY": ""}
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                config["TERRAKIO_API_KEY"] = self.key
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=4)
                if not self.quiet:
                    print(f"API key generated successfully and updated in {config_path}")
            except Exception as e:
                if not self.quiet:
                    print(f"Warning: Failed to update config file: {e}")
            return self.key
        else:
            # If we don't have auth_client with a token but have a key already, return it
            if self.key:
                if not self.quiet:
                    print("Using existing API key from config file.")
                return self.key
            else:
                raise ConfigurationError("No authentication token available. Please login first to refresh the API key.")

    @require_api_key
    def view_api_key(self) -> str:
        # If we have the auth client and token, refresh the key
        if self.auth_client and self.auth_client.token:
            self.key = self.auth_client.view_api_key()
            self.session.headers.update({'x-api-key': self.key})
        
        return self.key

    @require_api_key
    def view_api_key(self) -> str:
        # If we have the auth client and token, refresh the key
        if not self.auth_client:
            from terrakio_core.auth import AuthClient
            self.auth_client = AuthClient(
                base_url=self.url,
                verify=self.verify,
                timeout=self.timeout
            )
            self.auth_client.session = self.session
        return self.auth_client.view_api_key()

    # @require_api_key
    # def get_user_info(self) -> Dict[str, Any]:
    #     return self.auth_client.get_user_info()
    @require_api_key
    def get_user_info(self) -> Dict[str, Any]:
        # Initialize auth_client if it doesn't exist
        if not self.auth_client:
            from terrakio_core.auth import AuthClient
            self.auth_client = AuthClient(
                base_url=self.url,
                verify=self.verify,
                timeout=self.timeout
            )
            # Use the same session as the base client
            self.auth_client.session = self.session
            
        return self.auth_client.get_user_info()

    @require_api_key
    def wcs(self, expr: str, feature: Union[Dict[str, Any], ShapelyGeometry], in_crs: str = "epsg:4326",
            out_crs: str = "epsg:4326", output: str = "csv", resolution: int = -1,
            **kwargs):
        if hasattr(feature, 'is_valid'):
            from shapely.geometry import mapping
            feature = {
                "type": "Feature",
                "geometry": mapping(feature),
                "properties": {}
            }
        payload = {
            "feature": feature,
            "in_crs": in_crs,
            "out_crs": out_crs,
            "output": output,
            "resolution": resolution,
            "expr": expr,
            **kwargs
        }
        request_url = f"{self.url}/geoquery"
        try:
            print("the request url is ", request_url)
            print("the payload is ", payload)
            response = self.session.post(request_url, json=payload, timeout=self.timeout, verify=self.verify)
            print("the response is ", response.text)
            if not response.ok:
                error_msg = f"API request failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                raise APIError(error_msg)
            if output.lower() == "csv":
                import pandas as pd
                return pd.read_csv(BytesIO(response.content))
            elif output.lower() == "netcdf":
                return xr.open_dataset(BytesIO(response.content))
            else:
                try:
                    return xr.open_dataset(BytesIO(response.content))
                except ValueError:
                    import pandas as pd
                    try:
                        return pd.read_csv(BytesIO(response.content))
                    except:
                        return response.content
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    # Admin/protected methods
    @require_api_key
    def _get_user_by_id(self, user_id: str):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.get_user_by_id(user_id)

    @require_api_key
    def _get_user_by_email(self, email: str):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.get_user_by_email(email)

    @require_api_key
    def _list_users(self, substring: str = None, uid: bool = False):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.list_users(substring=substring, uid=uid)

    @require_api_key
    def _edit_user(self, user_id: str, uid: str = None, email: str = None, role: str = None, apiKey: str = None, groups: list = None, quota: int = None):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.edit_user(
            user_id=user_id,
            uid=uid,
            email=email,
            role=role,
            apiKey=apiKey,
            groups=groups,
            quota=quota
        )

    @require_api_key
    def _reset_quota(self, email: str, quota: int = None):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.reset_quota(email=email, quota=quota)

    @require_api_key
    def _delete_user(self, uid: str):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.delete_user(uid=uid)

    # Dataset management protected methods
    @require_api_key
    def _get_dataset(self, name: str, collection: str = "terrakio-datasets"):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.get_dataset(name=name, collection=collection)

    @require_api_key
    def _list_datasets(self, substring: str = None, collection: str = "terrakio-datasets"):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.list_datasets(substring=substring, collection=collection)

    @require_api_key
    def _create_dataset(self, name: str, collection: str = "terrakio-datasets", **kwargs):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.create_dataset(name=name, collection=collection, **kwargs)

    @require_api_key
    def _update_dataset(self, name: str, append: bool = True, collection: str = "terrakio-datasets", **kwargs):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.update_dataset(name=name, append=append, collection=collection, **kwargs)

    @require_api_key
    def _overwrite_dataset(self, name: str, collection: str = "terrakio-datasets", **kwargs):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.overwrite_dataset(name=name, collection=collection, **kwargs)

    @require_api_key
    def _delete_dataset(self, name: str, collection: str = "terrakio-datasets"):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.delete_dataset(name=name, collection=collection)

    @require_api_key
    def close(self):
        """Close all client sessions"""
        self.session.close()
        if self.auth_client:
            self.auth_client.session.close()
        # Close aiohttp session if it exists
        if self._aiohttp_session and not self._aiohttp_session.closed:
            try:
                nest_asyncio.apply()
                asyncio.run(self.close_async())
            except ImportError:
                try:
                    asyncio.run(self.close_async())
                except RuntimeError as e:
                    if "cannot be called from a running event loop" in str(e):
                        # In Jupyter, we can't properly close the async session
                        # Log a warning or handle gracefully
                        import warnings
                        warnings.warn("Cannot properly close aiohttp session in Jupyter environment. "
                                    "Consider using 'await client.close_async()' instead.")
                    else:
                        raise
            except RuntimeError:
                # Event loop may already be closed, ignore
                pass

    @require_api_key
    def __enter__(self):
        return self

    @require_api_key
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @admin_only_params('location', 'force_loc', 'server')
    @require_api_key
    def execute_job(self, name, region, output, config, overwrite=False, skip_existing=False, request_json=None, manifest_json=None, location=None, force_loc=None, server="dev-au.terrak.io"):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.execute_job(name, region, output, config, overwrite, skip_existing, request_json, manifest_json, location, force_loc, server)


    @require_api_key
    def get_mass_stats_task_id(self, name, stage, uid=None):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.get_task_id(name, stage, uid)

    @require_api_key
    def track_mass_stats_job(self, ids: Optional[list] = None):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.track_job(ids)

    @require_api_key
    def get_mass_stats_history(self, limit=100):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.get_history(limit)

    @require_api_key
    def start_mass_stats_post_processing(self, process_name, data_name, output, consumer_path, overwrite=False):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.start_post_processing(process_name, data_name, output, consumer_path, overwrite)

    @require_api_key
    def download_mass_stats_results(self, id=None, force_loc=False, **kwargs):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.download_results(id, force_loc, **kwargs)

    @require_api_key
    def cancel_mass_stats_job(self, id):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.cancel_job(id)

    @require_api_key
    def cancel_all_mass_stats_jobs(self):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.cancel_all_jobs()

    @require_api_key
    def _create_pyramids(self, name, levels, config):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.create_pyramids(name, levels, config)

    @require_api_key
    def random_sample(self, name, **kwargs):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.random_sample(name, **kwargs)

    @require_api_key
    async def zonal_stats_async(self, gdb, expr, conc=20, inplace=False, output="csv", 
                               in_crs="epsg:4326", out_crs="epsg:4326", resolution=-1, buffer=False):
        """
        Compute zonal statistics for all geometries in a GeoDataFrame using asyncio for concurrency.
        
        Args:
            gdb (geopandas.GeoDataFrame): GeoDataFrame containing geometries
            expr (str): Terrakio expression to evaluate, can include spatial aggregations
            conc (int): Number of concurrent requests to make
            inplace (bool): Whether to modify the input GeoDataFrame in place
            output (str): Output format (csv or netcdf)
            in_crs (str): Input coordinate reference system
            out_crs (str): Output coordinate reference system  
            resolution (int): Resolution parameter
            buffer (bool): Whether to buffer the request (default True)
            
        Returns:
            geopandas.GeoDataFrame: GeoDataFrame with added columns for results, or None if inplace=True
        """
        if conc > 100:
            raise ValueError("Concurrency (conc) is too high. Please set conc to 100 or less.")
        
        # Process geometries in batches
        all_results = []
        row_indices = []
        
        # Calculate total batches for progress reporting
        total_geometries = len(gdb)
        total_batches = (total_geometries + conc - 1) // conc  # Ceiling division
        completed_batches = 0
        
        print(f"Processing {total_geometries} geometries with concurrency {conc}")
        
        async def process_geometry(geom, index):
            """Process a single geometry"""
            try:
                feature = {
                    "type": "Feature",
                    "geometry": mapping(geom),
                    "properties": {"index": index}
                }
                result = await self.wcs_async(expr=expr, feature=feature, output=output, 
                                            in_crs=in_crs, out_crs=out_crs, resolution=resolution, buffer=buffer)
                # Add original index to track which geometry this result belongs to
                if isinstance(result, pd.DataFrame):
                    result['_geometry_index'] = index
                return result
            except Exception as e:
                raise
        
        async def process_batch(batch_indices):
            """Process a batch of geometries concurrently using TaskGroup"""
            try:
                async with asyncio.TaskGroup() as tg:
                    tasks = []
                    for idx in batch_indices:
                        geom = gdb.geometry.iloc[idx]
                        task = tg.create_task(process_geometry(geom, idx))
                        tasks.append(task)
                
                # Get results from completed tasks
                results = []
                for task in tasks:
                    try:
                        result = task.result()
                        results.append(result)
                    except Exception as e:
                        raise
                
                return results
            except* Exception as e:
                # Get the actual exceptions from the tasks
                for task in tasks:
                    if task.done() and task.exception():
                        raise task.exception()
                raise
            
        # Process in batches to control concurrency
        for i in range(0, len(gdb), conc):
            batch_indices = range(i, min(i + conc, len(gdb)))
            try:
                batch_results = await process_batch(batch_indices)
                all_results.extend(batch_results)
                row_indices.extend(batch_indices)
                
                # Update progress
                completed_batches += 1
                processed_geometries = min(i + conc, total_geometries)
                print(f"Progress: {completed_batches}/{total_batches} completed ({processed_geometries}/{total_geometries} geometries processed)")
                
            except Exception as e:
                if hasattr(e, 'response'):
                    raise APIError(f"API request failed: {e.response.text}")
                raise
        
        print("All batches completed! Processing results...")
        
        if not all_results:
            raise ValueError("No valid results were returned for any geometry")
            
        # Combine all results
        combined_df = pd.concat(all_results, ignore_index=True)
        
        # Check if we have temporal results
        has_time = 'time' in combined_df.columns
        
        # Create a result GeoDataFrame
        if has_time:
            # For temporal data, we'll create a hierarchical index
            # First make sure we have the geometry index and time columns
            if '_geometry_index' not in combined_df.columns:
                raise ValueError("Missing geometry index in results")
            
            # Create hierarchical index on geometry_index and time
            combined_df.set_index(['_geometry_index', 'time'], inplace=True)
            
            # For each unique geometry index, we need the corresponding geometry
            geometry_series = gdb.geometry.copy()
            
            # Get columns that will become new attributes (exclude index/utility columns)
            result_cols = combined_df.columns
            
            # Create a new GeoDataFrame with multi-index
            result_rows = []
            geometries = []
            
            # Iterate through the hierarchical index
            for (geom_idx, time_val), row in combined_df.iterrows():
                # Create a new row with geometry properties + result columns
                new_row = {}
                
                # Add original GeoDataFrame columns (except geometry)
                for col in gdb.columns:
                    if col != 'geometry':
                        new_row[col] = gdb.loc[geom_idx, col]
                
                # Add result columns
                for col in result_cols:
                    new_row[col] = row[col]
                
                result_rows.append(new_row)
                geometries.append(gdb.geometry.iloc[geom_idx])
            
            # Create a new GeoDataFrame with multi-index
            multi_index = pd.MultiIndex.from_tuples(
                combined_df.index.tolist(),
                names=['geometry_index', 'time']
            )
            
            result_gdf = gpd.GeoDataFrame(
                result_rows, 
                geometry=geometries,
                index=multi_index
            )
            
            if inplace:
                # Can't really do inplace with multi-temporal results as we're changing the structure
                return result_gdf
            else:
                return result_gdf
        else:
            # Non-temporal data - just add new columns to the existing GeoDataFrame
            result_gdf = gdb.copy() if not inplace else gdb
            
            # Get column names from the results (excluding utility columns)
            result_cols = [col for col in combined_df.columns if col not in ['_geometry_index']]
            
            # Create a mapping from geometry index to result rows
            geom_idx_to_row = {}
            for idx, row in combined_df.iterrows():
                geom_idx = int(row['_geometry_index'])
                geom_idx_to_row[geom_idx] = row
            
            # Add results as new columns to the GeoDataFrame
            for col in result_cols:
                # Initialize the column with None or appropriate default
                if col not in result_gdf.columns:
                    result_gdf[col] = None
                
                # Fill in values from results
                for geom_idx, row in geom_idx_to_row.items():
                    result_gdf.loc[geom_idx, col] = row[col]
            
            if inplace:
                return None
            else:
                return result_gdf

    @require_api_key
    def zonal_stats(self, gdb, expr, conc=20, inplace=False, output="csv", 
                   in_crs="epsg:4326", out_crs="epsg:4326", resolution=-1, buffer=False):
        """
        Compute zonal statistics for all geometries in a GeoDataFrame.
        
        Args:
            gdb (geopandas.GeoDataFrame): GeoDataFrame containing geometries
            expr (str): Terrakio expression to evaluate, can include spatial aggregations
            conc (int): Number of concurrent requests to make
            inplace (bool): Whether to modify the input GeoDataFrame in place
            output (str): Output format (csv or netcdf)
            in_crs (str): Input coordinate reference system
            out_crs (str): Output coordinate reference system
            resolution (int): Resolution parameter
            buffer (bool): Whether to buffer the request (default True)
            
        Returns:
            geopandas.GeoDataFrame: GeoDataFrame with added columns for results, or None if inplace=True
        """
        if conc > 100:
            raise ValueError("Concurrency (conc) is too high. Please set conc to 100 or less.")
        import asyncio
        
        print(f"Starting zonal statistics computation for expression: {expr}")
        
        # Check if we're in a Jupyter environment or already have an event loop
        try:
            loop = asyncio.get_running_loop()
            # We're in an async context (like Jupyter), use create_task
            nest_asyncio.apply()
            result = asyncio.run(self.zonal_stats_async(gdb, expr, conc, inplace, output, 
                                                      in_crs, out_crs, resolution, buffer))
        except RuntimeError:
            # No running event loop, safe to use asyncio.run()
            result = asyncio.run(self.zonal_stats_async(gdb, expr, conc, inplace, output, 
                                                      in_crs, out_crs, resolution, buffer))
        except ImportError:
            # nest_asyncio not available, try alternative approach
            try:
                loop = asyncio.get_running_loop()
                # Create task in existing loop
                task = loop.create_task(self.zonal_stats_async(gdb, expr, conc, inplace, output, 
                                                             in_crs, out_crs, resolution, buffer))
                # This won't work directly - we need a different approach
                raise RuntimeError("Cannot run async code in Jupyter without nest_asyncio. Please install: pip install nest-asyncio")
            except RuntimeError:
                # No event loop, use asyncio.run
                result = asyncio.run(self.zonal_stats_async(gdb, expr, conc, inplace, output, 
                                                          in_crs, out_crs, resolution, buffer))
        
        # Ensure aiohttp session is closed after running async code
        try:
            if self._aiohttp_session and not self._aiohttp_session.closed:
                asyncio.run(self.close_async())
        except RuntimeError:
            # Event loop may already be closed, ignore
            pass
        
        print("Zonal statistics computation completed!")
        return result

    # Group access management protected methods
    @require_api_key
    def _get_group_users_and_datasets(self, group_name: str):
        if not self.group_access:
            from terrakio_core.group_access_management import GroupAccessManagement
            if not self.url or not self.key:
                raise ConfigurationError("Group access management client not initialized. Make sure API URL and key are set.")
            self.group_access = GroupAccessManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.group_access.get_group_users_and_datasets(group_name=group_name)

    @require_api_key
    def _add_group_to_dataset(self, dataset: str, group: str):
        if not self.group_access:
            from terrakio_core.group_access_management import GroupAccessManagement
            if not self.url or not self.key:
                raise ConfigurationError("Group access management client not initialized. Make sure API URL and key are set.")
            self.group_access = GroupAccessManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.group_access.add_group_to_dataset(dataset=dataset, group=group)

    @require_api_key
    def _add_group_to_user(self, uid: str, group: str):
        if not self.group_access:
            from terrakio_core.group_access_management import GroupAccessManagement
            if not self.url or not self.key:
                raise ConfigurationError("Group access management client not initialized. Make sure API URL and key are set.")
            self.group_access = GroupAccessManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.group_access.add_group_to_user(uid=uid, group=group)

    @require_api_key
    def _delete_group_from_user(self, uid: str, group: str):
        if not self.group_access:
            from terrakio_core.group_access_management import GroupAccessManagement
            if not self.url or not self.key:
                raise ConfigurationError("Group access management client not initialized. Make sure API URL and key are set.")
            self.group_access = GroupAccessManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.group_access.delete_group_from_user(uid=uid, group=group)

    @require_api_key
    def _delete_group_from_dataset(self, dataset: str, group: str):
        if not self.group_access:
            from terrakio_core.group_access_management import GroupAccessManagement
            if not self.url or not self.key:
                raise ConfigurationError("Group access management client not initialized. Make sure API URL and key are set.")
            self.group_access = GroupAccessManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.group_access.delete_group_from_dataset(dataset=dataset, group=group)

    # Space management protected methods
    @require_api_key
    def _get_total_space_used(self):
        if not self.space_management:
            from terrakio_core.space_management import SpaceManagement
            if not self.url or not self.key:
                raise ConfigurationError("Space management client not initialized. Make sure API URL and key are set.")
            self.space_management = SpaceManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.space_management.get_total_space_used()

    @require_api_key
    def _get_space_used_by_job(self, name: str, region: str = None):
        if not self.space_management:
            from terrakio_core.space_management import SpaceManagement
            if not self.url or not self.key:
                raise ConfigurationError("Space management client not initialized. Make sure API URL and key are set.")
            self.space_management = SpaceManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.space_management.get_space_used_by_job(name, region)

    @require_api_key
    def _delete_user_job(self, name: str, region: str = None):
        if not self.space_management:
            from terrakio_core.space_management import SpaceManagement
            if not self.url or not self.key:
                raise ConfigurationError("Space management client not initialized. Make sure API URL and key are set.")
            self.space_management = SpaceManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.space_management.delete_user_job(name, region)

    @require_api_key
    def _delete_data_in_path(self, path: str, region: str = None):
        if not self.space_management:
            from terrakio_core.space_management import SpaceManagement
            if not self.url or not self.key:
                raise ConfigurationError("Space management client not initialized. Make sure API URL and key are set.")
            self.space_management = SpaceManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.space_management.delete_data_in_path(path, region)
    
    @require_api_key
    def start_mass_stats_job(self, task_id):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.start_job(task_id)

    
    @require_api_key
    def generate_ai_dataset(
        self,
        name: str,
        aoi_geojson: str,
        expression_x: str,
        expression_y: str,
        samples: int,
        tile_size: int,
        crs: str = "epsg:4326",
        res: float = 0.001,
        region: str = "aus",
        start_year: int = None,
        end_year: int = None,
    ) -> dict:
        """
        Generate an AI dataset using specified parameters.

        Args:
            name (str): Name of the dataset to generate
            aoi_geojson (str): Path to GeoJSON file containing area of interest
            expression_x (str): Expression for X variable (e.g. "MSWX.air_temperature@(year=2021, month=1)")
            expression_y (str): Expression for Y variable with {year} placeholder
            samples (int): Number of samples to generate
            tile_size (int): Size of tiles in degrees
            crs (str, optional): Coordinate reference system. Defaults to "epsg:4326"
            res (float, optional): Resolution in degrees. Defaults to 0.001
            region (str, optional): Region code. Defaults to "aus"
            start_year (int, optional): Start year for data generation. Required if end_year provided
            end_year (int, optional): End year for data generation. Required if start_year provided
            overwrite (bool, optional): Whether to overwrite existing dataset. Defaults to False

        Returns:
            dict: Response from the AI dataset generation API

        Raises:
            ValidationError: If required parameters are missing or invalid
            APIError: If the API request fails
        """

        # we have the parameters, let pass the parameters to the random sample function
        # task_id = self.random_sample(name, aoi_geojson, expression_x, expression_y, samples, tile_size, crs, res, region, start_year, end_year, overwrite)
        config = {
            "expressions" : [{"expr": expression_x, "res": res, "prefix": "x"}],
            "filters" : []
        }
        config["expressions"].append({"expr": expression_y, "res" : res, "prefix": "y"})

        expression_x = expression_x.replace("{year}", str(start_year))
        expression_y = expression_y.replace("{year}", str(start_year))
        print("the aoi geojson is ", aoi_geojson)
        with open(aoi_geojson, 'r') as f:
            aoi_data = json.load(f)
        print("the config is ", config)
        task_id = self.random_sample(
            name=name,
            config=config,
            aoi=aoi_data,
            samples=samples,
            year_range=[start_year, end_year],
            crs=crs,
            tile_size=tile_size,
            res=res,
            region=region,
            output="netcdf",
            server=self.url,
            bucket="terrakio-mass-requests",
            overwrite=True
        )["task_id"]
        print("the task id is ", task_id)

        # Wait for job completion
        import time
        
        while True:
            result = self.track_mass_stats_job(ids=[task_id])
            status = result[task_id]['status']
            print(f"Job status: {status}")
            
            if status == "Completed":
                break
            elif status == "Error":
                raise Exception(f"Job {task_id} encountered an error")
                
            # Wait 30 seconds before checking again
            time.sleep(30)

        # print("the result is ", result)
        # after all the random sample jos are done, we then start the mass stats job
        task_id = self.start_mass_stats_job(task_id)
        # now we hav ethe random sampel

        # print("the task id is ", task_id)
        return task_id

    @require_api_key
    def train_model(self, model_name: str, training_dataset: str, task_type: str, model_category: str, architecture: str, region: str, hyperparameters: dict = None) -> dict:
        """
        Train a model using the external model training API.
        
        Args:
            model_name (str): The name of the model to train.
            training_dataset (str): The training dataset identifier.
            task_type (str): The type of ML task (e.g., regression, classification).
            model_category (str): The category of model (e.g., random_forest).
            architecture (str): The model architecture.
            region (str): The region identifier.
            hyperparameters (dict, optional): Additional hyperparameters for training.
            
        Returns:
            dict: The response from the model training API.
        """
        payload = {
            "model_name": model_name,
            "training_dataset": training_dataset,
            "task_type": task_type,
            "model_category": model_category,
            "architecture": architecture,
            "region": region,
            "hyperparameters": hyperparameters
        }
        endpoint = f"{self.url.rstrip('/')}/train_model"
        print("the payload is ", payload)
        try:
            response = self.session.post(endpoint, json=payload, timeout=self.timeout, verify=self.verify)
            if not response.ok:
                error_msg = f"Model training request failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except Exception:
                    if response.text:
                        error_msg += f" - {response.text}"
                raise APIError(error_msg)
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Model training request failed: {str(e)}")

    # Mass Stats methods
    @require_api_key
    def combine_tiles(self, 
        data_name: str,
        usezarr: bool,
        overwrite: bool,
        output : str) -> dict:

        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.combine_tiles(data_name, usezarr, overwrite, output)
    


    @require_api_key
    def create_dataset_file(
        self,
        name: str,
        aoi: str,
        expression: str,
        output: str,
        tile_size: float = 128.0,
        crs: str = "epsg:4326",
        res: float = 0.0001,
        region: str = "aus",
        to_crs: str = "epsg:4326",
        overwrite: bool = True,
        skip_existing: bool = False,
        non_interactive: bool = True,
        usezarr: bool = False,
        poll_interval: int = 30,
        download_path: str = "/home/user/Downloads",
    ) -> dict:
        
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        
        
        from terrakio_core.generation.tiles import tiles
        import tempfile
        import time

        body, reqs, groups = tiles(
            name = name, 
            aoi = aoi, 
            expression = expression,
            output = output,
            tile_size = tile_size,
            crs = crs,
            res = res,
            region = region,
            to_crs = to_crs,
            fully_cover = True,
            overwrite = overwrite,
            skip_existing = skip_existing,
            non_interactive = non_interactive
        )

        # Create temp json files before upload
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tempreq:
            tempreq.write(reqs)
            tempreqname = tempreq.name
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tempmanifest:
            tempmanifest.write(groups)
            tempmanifestname = tempmanifest.name
        
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )

        task_id = self.mass_stats.execute_job(
            name=body["name"],
            region=body["region"],
            output=body["output"],
            config = {},
            overwrite=body["overwrite"],
            skip_existing=body["skip_existing"],
            request_json=tempreqname,
            manifest_json=tempmanifestname,
        )

        ### Start combining tiles when generation-tiles job is done
        start_time = time.time()
        status = None
        
        while True:
            try:
                taskid = task_id['task_id']
                trackinfo = self.mass_stats.track_job([taskid])
                status = trackinfo[taskid]['status']
                
                # Check completion states
                if status == 'Completed':
                    print('Tiles generated successfully!')
                    break
                elif status in ['Failed', 'Cancelled', 'Error']:
                    raise RuntimeError(f"Job {taskid} failed with status: {status}")
                else:
                    # Job is still running
                    elapsed_time = time.time() - start_time
                    print(f"Job status: {status} - Elapsed time: {elapsed_time:.1f}s", end='\r')
                    
                    # Sleep before next check
                    time.sleep(poll_interval)
                    
                    
            except KeyboardInterrupt:
                print(f"\nInterrupted! Job {taskid} is still running in the background.")
                raise
            except Exception as e:
                print(f"\nError tracking job: {e}")
                raise

        # Clean up temporary files
        import os
        os.unlink(tempreqname)
        os.unlink(tempmanifestname)


        # return self.mass_stats.combine_tiles(body["name"], usezarr, body["overwrite"], body["output"])
    
        # Start combining tiles
        combine_result = self.mass_stats.combine_tiles(body["name"], usezarr, body["overwrite"], body["output"])
        combine_task_id = combine_result.get("task_id")

        # Poll combine_tiles job status
        combine_start_time = time.time()
        while True:
            try:
                trackinfo = self.mass_stats.track_job([combine_task_id])
                download_file_name = trackinfo[combine_task_id]['folder'] + '.nc'
                bucket = trackinfo[combine_task_id]['bucket']
                combine_status = trackinfo[combine_task_id]['status']
                if combine_status == 'Completed':
                    print('Tiles combined successfully!')
                    break
                elif combine_status in ['Failed', 'Cancelled', 'Error']:
                    raise RuntimeError(f"Combine job {combine_task_id} failed with status: {combine_status}")
                else:
                    elapsed_time = time.time() - combine_start_time
                    print(f"Combine job status: {combine_status} - Elapsed time: {elapsed_time:.1f}s", end='\r')
                    time.sleep(poll_interval)
            except KeyboardInterrupt:
                print(f"\nInterrupted! Combine job {combine_task_id} is still running in the background.")
                raise
            except Exception as e:
                print(f"\nError tracking combine job: {e}")
                raise

        # Download the resulting file
        if download_path:
            self.mass_stats.download_file(body["name"], bucket, download_file_name, download_path)
        else:
            path = f"{body['name']}/combinedOutput/{download_file_name}"
            print(f"Combined file is available at {path}")

        return {"generation_task_id": task_id, "combine_task_id": combine_task_id}


        # taskid = self.mass_stats.get_task_id(job_name, stage).get('task_id')
        # trackinfo = self.mass_stats.track_job([taskid])
        # bucket = trackinfo[taskid]['bucket']
        # return self.mass_stats.download_file(job_name, bucket, file_name, output_path)


    @require_api_key
    def deploy_model(self, dataset: str, product:str, model_name:str, input_expression: str, model_training_job_name: str, uid: str, dates_iso8601: list):
        script_content = self._generate_script(model_name, product, model_training_job_name, uid)
        script_name = f"{product}.py"
        self._upload_script_to_bucket(script_content, script_name, model_training_job_name, uid)
        self._create_dataset(name = dataset, collection = "terrakio-datasets", products = [product], path = f"gs://terrakio-mass-requests/{uid}/{model_training_job_name}/inference_scripts", input = input_expression, dates_iso8601 = dates_iso8601, padding = 0)

    @require_api_key
    def _generate_script(self, model_name: str, product: str, model_training_job_name: str, uid: str) -> str:
        return textwrap.dedent(f'''
            import logging
            from io import BytesIO

            import numpy as np
            import pandas as pd
            import xarray as xr
            from google.cloud import storage
            from onnxruntime import InferenceSession

            logging.basicConfig(
                level=logging.INFO
            )

            def get_model():
                logging.info("Loading model for {model_name}...")

                client = storage.Client()
                bucket = client.get_bucket('terrakio-mass-requests')
                blob = bucket.blob('{uid}/{model_training_job_name}/models/{model_name}.onnx')

                model = BytesIO()
                blob.download_to_file(model)
                model.seek(0)

                session = InferenceSession(model.read(), providers=["CPUExecutionProvider"])
                return session

            def {product}(*bands, model):
                logging.info("start preparing data")
                print("the bands are ", bands)
                
                data_arrays = list(bands)
                
                print("the data arrays are ", [da.name for da in data_arrays])
                
                reference_array = data_arrays[0]
                original_shape = reference_array.shape
                logging.info(f"Original shape: {{original_shape}}")
                
                if 'time' in reference_array.dims:
                    time_coords = reference_array.coords['time']
                    if len(time_coords) == 1:
                        output_timestamp = time_coords[0]
                    else:
                        years = [pd.to_datetime(t).year for t in time_coords.values]
                        unique_years = set(years)
                        
                        if len(unique_years) == 1:
                            year = list(unique_years)[0]
                            output_timestamp = pd.Timestamp(f"{{year}}-01-01")
                        else:
                            latest_year = max(unique_years)
                            output_timestamp = pd.Timestamp(f"{{latest_year}}-01-01")
                else:
                    output_timestamp = pd.Timestamp("1970-01-01")

                averaged_bands = []
                for data_array in data_arrays:
                    if 'time' in data_array.dims:
                        averaged_band = np.mean(data_array.values, axis=0)
                        logging.info(f"Averaged band from {{data_array.shape}} to {{averaged_band.shape}}")
                    else:
                        averaged_band = data_array.values
                        logging.info(f"No time dimension, shape: {{averaged_band.shape}}")

                    flattened_band = averaged_band.reshape(-1, 1)
                    averaged_bands.append(flattened_band)

                input_data = np.hstack(averaged_bands)

                logging.info(f"Final input shape: {{input_data.shape}}")

                output = model.run(None, {{"float_input": input_data.astype(np.float32)}})[0]

                logging.info(f"Model output shape: {{output.shape}}")

                if len(original_shape) >= 3:
                    spatial_shape = original_shape[1:]
                else:
                    spatial_shape = original_shape

                output_reshaped = output.reshape(spatial_shape)

                output_with_time = np.expand_dims(output_reshaped, axis=0)

                if 'time' in reference_array.dims:
                    spatial_dims = [dim for dim in reference_array.dims if dim != 'time']
                    spatial_coords = {{dim: reference_array.coords[dim] for dim in spatial_dims if dim in reference_array.coords}}
                else:
                    spatial_dims = list(reference_array.dims)
                    spatial_coords = dict(reference_array.coords)

                result = xr.DataArray(
                    data=output_with_time.astype(np.float32),
                    dims=['time'] + list(spatial_dims),
                    coords={
                        'time': [output_timestamp.values],
                        'y': spatial_coords['y'].values,
                        'x': spatial_coords['x'].values
                    }
                )
                return result
            ''').strip()
    
    @require_api_key
    def _upload_script_to_bucket(self, script_content: str, script_name: str, model_training_job_name: str, uid: str):
        """Upload the generated script to Google Cloud Storage"""

        client = storage.Client()
        bucket = client.get_bucket('terrakio-mass-requests')
        blob = bucket.blob(f'{uid}/{model_training_job_name}/inference_scripts/{script_name}')
        blob.upload_from_string(script_content, content_type='text/plain')
        logging.info(f"Script uploaded successfully to {uid}/{model_training_job_name}/inference_scripts/{script_name}")




    @require_api_key
    def download_file_to_path(self, job_name, stage, file_name, output_path):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )

        # fetch bucket info based on job name and stage

        taskid = self.mass_stats.get_task_id(job_name, stage).get('task_id')
        trackinfo = self.mass_stats.track_job([taskid])
        bucket = trackinfo[taskid]['bucket']
        return self.mass_stats.download_file(job_name, bucket, file_name, output_path)


# Apply the @require_api_key decorator to ALL methods in BaseClient
# except only the absolute minimum that shouldn't require auth
def _apply_api_key_decorator():
    # Only these methods can be used without API key
    skip_auth_methods = [
        '__init__', 'login', 'signup'
    ]
    
    # Get all attributes of BaseClient
    for attr_name in dir(BaseClient):
        # Skip special methods and methods in skip list
        if attr_name.startswith('__') and attr_name not in ['__enter__', '__exit__', '__aenter__', '__aexit__'] or attr_name in skip_auth_methods:
            continue
            
        # Get the attribute
        attr = getattr(BaseClient, attr_name)
        
        # Skip if not callable (not a method) or already decorated
        if not callable(attr) or hasattr(attr, '_is_decorated'):
            continue
            
        # Apply decorator to EVERY method not in skip list
        setattr(BaseClient, attr_name, require_api_key(attr))
        # Mark as decorated to avoid double decoration
        getattr(BaseClient, attr_name)._is_decorated = True

# Run the decorator application
_apply_api_key_decorator()