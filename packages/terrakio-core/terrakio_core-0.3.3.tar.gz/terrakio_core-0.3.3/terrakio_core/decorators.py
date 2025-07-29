# terrakio_core/decorators.py
def admin_only_params(*restricted_params):
    """
    Decorator factory for restricting method parameters to admin users only.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if hasattr(self, '_is_admin') and self._is_admin:
                return func(self, *args, **kwargs)
            
            admin_params_used = set(kwargs.keys()) & set(restricted_params)
            if admin_params_used:
                raise PermissionError(f"Parameters {admin_params_used} are only available to admin users")
            
            filtered_kwargs = {k: v for k, v in kwargs.items() if k not in restricted_params}
            return func(self, *args, **filtered_kwargs)
        return wrapper
    return decorator
