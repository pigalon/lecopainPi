import wrapt
from flask_login import current_user

@wrapt.decorator
def admin_login_required(wrapped, instance, args, kwargs):
    if current_user.get_main_role() != 'admin_role':
        return "you need to be admin", 401
    return wrapped(*args, **kwargs)
        
        