import functools
import types
import httpx



def response_dispatch(func):
    registry = dict()
    registry[NotImplemented] = func
    
    @functools.wraps(func)
    def dispatch(response: httpx.Response):
        return registry.get(response.status_code, registry[NotImplemented])
        
    
    def register(status_code: int):
        def decorator(handler_func):
            if status_code in registry:
                raise ValueError(f"Handler already registered for status code {status_code}")
            registry[status_code] = handler_func
            return handler_func
        return decorator
    
    def wrapper(*args, **kwargs):
        if not args:
            raise TypeError(f"{func.__name__} requires at least 1 positional argument (httpx.Response)")
        response = args[0]
        if not isinstance(response, httpx.Response):
            raise TypeError(f"Expected httpx.Response, got {type(response).__name__}")
        return dispatch(response.status_code)(*args, **kwargs)
    
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = types.MappingProxyType(registry)
    functools.update_wrapper(wrapper, func)

    return wrapper
    
    
    





