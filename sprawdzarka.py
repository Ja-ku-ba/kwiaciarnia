
from kwiaciarnia.models import User


@property
def is_admin(self):
    user_check = User.query.filter_by(id=current_user.id)
    if user_check.is_stuff:
        return True



# if Post_likes.query.filter_by(post_like=pk, user_like=current_user.id).first():
#     new_unlike = Post_likes.query.filter_by(user_like=current_user.id).first()
#     db.session.delete(new_unlike)
#     unliked = Posts.query.filter_by(id=pk).first()
#     unliked.likes -= 1
#     db.session.commit()


# if Post_dislikes.query.filter_by(post_dislike=pk, user_dislike=current_user.id).first():
#     new_undislike = Post_dislikes.query.filter_by(user_dislike=current_user.id).first()
#     db.session.delete(new_undislike)
#     undisliked = Posts.query.filter_by(id=pk).first()
#     undisliked.dislikes -= 1
#     db.session.commit()