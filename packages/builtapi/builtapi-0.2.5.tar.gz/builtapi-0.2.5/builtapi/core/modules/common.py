import functools

from pydantic import BaseModel

from builtapi.session import BuiltAPISession


class AuthenicationException(Exception):
    pass


class AuthorizationException(Exception):
    pass


class ResourceNotFoundException(Exception):
    pass


class ServerErrorException(Exception):
    pass


class APIException(Exception):
    pass


def trpc_api_call(url: str, method: str, return_type: BaseModel = None, schema_class: BaseModel = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            input_data = func(self, *args, **kwargs)

            if not isinstance(input_data, (schema_class, dict)):
                raise ValueError(f'Input should be {schema_class.__name__} or a valid dict')
            if isinstance(input_data, dict):
                input_data = schema_class(**input_data)

            formated_url = url.format(**input_data.dict())

            response = None
            if method.lower() == "get":
                response = self.session.get(formated_url,
                                            params={"input": input_data.model_dump_json(exclude_unset=True, exclude_none=True)})
            elif method.lower() == "post":
                response = self.session.post(formated_url, json=input_data.model_dump(
                    mode="json", exclude_unset=True, exclude_none=True))
            elif method.lower() == "put":
                response = self.session.put(formated_url, json=input_data.model_dump(
                    mode="json", exclude_unset=True, exclude_none=True))
            elif method.lower() == "delete":
                response = self.session.delete(formated_url,
                                               params={"input": input_data.model_dump_json(exclude_unset=True, exclude_none=True)})
            else:
                raise ValueError(f'HTTP method {method} is not supported.')

            raise_if_error(response)

            data = response.json().get('result', {}).get('data', {})
            
            if return_type is not None and isinstance(data, dict):
                return return_type(**data)
            return data

        return wrapper

    return decorator


def rest_api_call(url: str, method: str, return_type: BaseModel = None, schema_class: BaseModel = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            input_data = func(self, *args, **kwargs)

            if not isinstance(input_data, (schema_class, dict)):
                raise ValueError(f'Input should be {schema_class.__name__} or a valid dict')
            if isinstance(input_data, dict):
                input_data = schema_class(**input_data)

            formated_url = url.format(**input_data.dict())

            response = None
            if method.lower() == "get":
                response = self.session.get(formated_url,
                                            params={"input": input_data.model_dump_json(exclude_unset=True, exclude_none=True)})
            elif method.lower() == "post":
                response = self.session.post(formated_url, json=input_data.model_dump(
                    mode="json", exclude_unset=True, exclude_none=True))
            elif method.lower() == "put":
                response = self.session.put(formated_url, json=input_data.model_dump(
                    mode="json", exclude_unset=True, exclude_none=True))
            elif method.lower() == "delete":
                response = self.session.delete(formated_url, json=input_data.model_dump(
                    mode="json", exclude_unset=True, exclude_none=True))
            elif method.lower() == "patch":
                response = self.session.patch(formated_url, json=input_data.model_dump(
                    mode="json", exclude_unset=True, exclude_none=True))
            else:
                raise ValueError(f'HTTP method {method} is not supported.')

            raise_if_error(response)

            data = response.json()
            return return_type(**data) if return_type else data

        return wrapper

    return decorator


def raise_if_error(response):
    if response.status_code != 200:
        if response.status_code == 401:
            error = response.json().get('error', {})
            raise AuthenicationException(f"Authentication failed. Error: {error}")
        if response.status_code == 403:
            error = response.json().get('error', {})
            raise AuthorizationException(f"Authorization failed. Error: {error}")
        if response.status_code == 404:
            error = response.json().get('error', {})
            raise ResourceNotFoundException(f"Resource not found. Error: {error}")
        if response.status_code == 500:
            raise ServerErrorException(f"Server error. Error: {response.text}")

        raise APIException(f"API call failed. Details: {response.text}")


class BaseModule:
    def __init__(self, session: BuiltAPISession):
        self.session = session
