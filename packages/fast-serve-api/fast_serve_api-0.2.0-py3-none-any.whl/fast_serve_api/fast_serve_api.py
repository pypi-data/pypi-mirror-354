from fastapi import FastAPI, status
import inspect
from typing import get_type_hints, Any
from fastapi.responses import JSONResponse
from pydantic import create_model
import re
from pydantic import BaseModel
from typing import Union
import traceback

from .models.fast_serve_api_model import FastServeApiModel
from .models.fast_serve_api_list_model import FastServeApiListModel
from .models.fast_serve_api_error_model import FastServeApiErrorModel


class FastServeApi:
    """Base class that automatically converts static methods to FastAPI endpoints"""
    
    _app: FastAPI = None
    
    @classmethod
    def initialize(cls, app: FastAPI):
        """Initialize the service with a FastAPI app instance and register endpoints"""
        cls._app = app
        cls._register_endpoints()
    
    @classmethod  
    def _register_endpoints(cls):
        """Register all static methods as FastAPI endpoints"""
        if cls._app is None:
            raise ValueError(f"{cls.__name__} must be initialized with a FastAPI app instance using {cls.__name__}.initialize(app)")
        
        # Get the service name from class name (convert CamelCase to snake_case)
        service_name = cls._camel_to_snake(cls.__name__)
        
        # Find all static methods
        for method_name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if method_name.startswith('_'):
                continue
                
            # Create endpoint path
            endpoint_path = f"/{service_name}/{method_name}"
            
            # Get method signature and type hints
            sig = inspect.signature(method)
            type_hints = get_type_hints(method)
            
            # Create Pydantic model for request body
            fields = {}
            for param_name, param in sig.parameters.items():
                param_type = type_hints.get(param_name, Any)
                default_value = param.default if param.default != inspect.Parameter.empty else ...
                fields[param_name] = (param_type, default_value)
            
            # Create dynamic Pydantic model
            request_model = create_model(f"{cls.__name__}{method_name.title()}Request", **fields)
            
            # Get return type
            base_return_type = type_hints.get('return', Any)

            # If base_return_type is not Any, create a Union type
            if base_return_type != Any:
                return_type = Union[base_return_type, FastServeApiErrorModel]
            else:
                return_type = FastServeApiErrorModel
            
            # Create the endpoint function
            def create_endpoint(static_method, fields, req_model):
                async def endpoint(request: req_model): # type: ignore
                    # Convert request model to dict and call the static method
                    kwargs = request.dict()
                    # treat Pydantic models parameters
                    for key, value in kwargs.items():
                        param_type = fields[key][0]
                        # Check if param_type is a subclass of BaseModel (i.e., a Pydantic model)
                        if isinstance(value, dict) and isinstance(param_type, type) and issubclass(param_type, BaseModel):
                            kwargs[key] = param_type(**value)
                    try:
                        result = static_method(**kwargs)
                        # If the result is a Pydantic model, convert it to dict
                        if isinstance(result, BaseModel):
                            # check if result is a subclass of FastServeApiModel or FastServeApiListModel
                            if issubclass(result.__class__, FastServeApiModel) or issubclass(result.__class__, FastServeApiListModel):
                                result = result.model_dump()
                            else:
                                raise TypeError(f"Return type must be a subclass of FastServeApiModel or FastServeApiListModel.")
                    except Exception as e:
                        # Handle exceptions and return a proper error response
                        result = {
                            "success": False,
                            "message": str(e),
                            "stack_trace": "".join(traceback.format_exception(type(e), e, e.__traceback__)),
                            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR # every exception will return a JSONResponse with status 500
                        }
                    
                    if isinstance(result, dict):
                        status_code = result.get('status_code') or status.HTTP_200_OK
                    else:
                        status_code = status.HTTP_200_OK

                    return JSONResponse(
                        status_code=status_code,
                        content=result
                    )

                return endpoint
            
            # Register the endpoint
            endpoint_func = create_endpoint(method, fields, request_model)
            endpoint_func.__name__ = f"{service_name}_{method_name}"
            
            # Add the POST endpoint to FastAPI app
            cls._app.post(
                endpoint_path,
                response_model=return_type if return_type != Any else None,
                name=f"{service_name}_{method_name}"
            )(endpoint_func)


    @staticmethod
    def _camel_to_snake(name: str) -> str:
        """Convert CamelCase to snake_case"""
        # Remove 'Service' suffix if present
        if name.endswith('Service'):
            name = name[:-7]
        
        # Convert CamelCase to snake_case
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


    @classmethod
    def get_app(cls) -> FastAPI:
        """Get the FastAPI application instance"""
        if cls._app is None:
            raise ValueError(f"{cls.__name__} has not been initialized. Call {cls.__name__}.initialize(app) first.")
        return cls._app
