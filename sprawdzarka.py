
from kwiaciarnia.models import User


@property
def is_admin(self):
    user_check = User.query.filter_by(id=current_user.id)
    if user_check.is_stuff:
        return True



