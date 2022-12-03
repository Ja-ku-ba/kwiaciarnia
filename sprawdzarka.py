
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



<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
    <a class="navbar-brand" href="#">Hidden brand</a>
    <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
      <li class="nav-item active">
        <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Link</a>
      </li>
      <li class="nav-item">
        <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
      </li>
    </ul>
    <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
  </div>
</nav>
