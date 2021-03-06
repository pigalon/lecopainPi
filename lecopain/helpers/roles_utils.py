import wrapt
from lecopain.app import app
from flask_login import current_user

@wrapt.decorator
def admin_login_required(wrapped, instance, args, kwargs):
    if app.config['TESTING']:
        return wrapped(*args, **kwargs)

    if current_user.get_main_role() != 'admin_role':
        return "you need to be admin", 401
    return wrapped(*args, **kwargs)
        
@wrapt.decorator
def customer_login_required(wrapped, instance, args, kwargs):
    if app.config['TESTING']:
        return wrapped(*args, **kwargs)

    if current_user.get_main_role() != 'customer_role':
        return "you need to be customer", 401
    return wrapped(*args, **kwargs)

@wrapt.decorator
def seller_login_required(wrapped, instance, args, kwargs):
    if app.config['TESTING']:
        return wrapped(*args, **kwargs)

    if current_user.get_main_role() != 'seller_role':
        return "you need to be seller", 401
    return wrapped(*args, **kwargs)

@wrapt.decorator
def global_login_required(wrapped, instance, args, kwargs):
    if app.config['TESTING']:
        return wrapped(*args, **kwargs)

    if current_user.get_main_role() != 'admin_role' and \
      current_user.get_main_role()  != 'customer_role' and \
      current_user.get_main_role()  != 'seller_role':
        return "you need to be admin", 401
    return wrapped(*args, **kwargs)
        