from flask import render_template, redirect, request, flash, g, Markup, jsonify
from ...gamehunter.db import db
from .forms import NewPostForm, NewCommentForm
from ...blueprints.games.models import Games
from ...blueprints.api.models import RAWGioAPI
from .models import Post, Comment, UpvoteComment, UpvotePost
from ...blueprints.blueprints import forum_bp

##########################################################################################################################################

@forum_bp.route('/<int:page>')
def home_page(page):
    """Endpoint for Forum index page. Grabs posts ordered by most recently active. """
    
    fresh_posts = Post.query.order_by(Post.last_active.desc()).paginate(page=page,per_page=10,error_out=False)
    
    return render_template('forum/index.html', posts=fresh_posts)


##########################################################################################################################################

@forum_bp.route('/post/new/<int:game_id>', methods=['GET', 'POST'])
def new_post(game_id):
    """End point for creating a new Post.
    
    Accepts GET and POST requests.
    
    GET requests will check for the Game in our DB. It will create one if it is not found. It will then render the Post
    creation page with a Form.
    
    POST requests will create the Post and add it to the DB and redirect to the newly created Post's page."""
    
    if not g.user:
        flash('You must be logged in to do that.', 'danger')
        return redirect('/')
    
    if request.method == 'GET':
        if 'name' not in request.form:
            flash(Markup("Please create a post through the appropriate channels. If you need help, check out our FAQ <a class='link-light' href='/faq'>here</a>."), 'danger')
            return redirect('/')
        
    game_check = Games.check_for_game_in_db(game_id)
    
    if game_check:
        game_check.activity = game_check.activity + 1
        db.session.commit()
        pass
    else:
        game = RAWGioAPI.get_specific_game(game_id)
        if not game:
            flash(Markup("That game doesn't exist. Please make sure you're creating a post properly. If you need help you can view the FAQ <a class='link-light' href='/faq'>here</a>."),'danger')
            return redirect('/')
        else:
            new_game = Games.create_new_game(rawg_id=game_id, title=request.form.get('name'), 
                                             background_img=request.form.get('background_image'),
                                             release_date=request.form.get('release_date'))
            
    form = NewPostForm()
    if form.validate_on_submit():
        new_post = Post.create_new_post(game_id=game_id, title=form.title.data, content=form.content.data.strip())
        
        if new_post:
            flash("Post successfully created", 'success')
            return redirect(f'/forum/post/{new_post.id}')
        else:
            flash('Something went wrong. Please try again later.', 'danger')
            return redirect(f'/games/{game_id}')
    
    return render_template('forum/new_post.html', form=form, game=game_check or new_game)


##########################################################################################################################################

@forum_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_details(post_id):
    """End point to the Post details page.
    
    Accepts both GET and POST requests.
    
    GET requests will simply render the Post details page along with a Form to submit User Comments.
    
    POST requests will create a new Comment and redirect to the Post details page."""

    post = Post.query.get_or_404(post_id)
    form = NewCommentForm()
    
    if form.validate_on_submit():
        if not g.user:
            flash('You need to be logged in to do that.', 'danger')
            return redirect(f'/forum/post/{post_id}')
        
        new_comment = Comment.create_new_comment(post=post, content=form.content.data)
        
        if new_comment:
            flash('Comment successfully added.', 'success')
            return redirect(f'/forum/post/{post_id}')
        else:
            flash('Something went wrong. Please try again later.')
            return redirect(f'/forum/post/{post_id}')
        
    return render_template('forum/post_details.html', post=post, form=form)


##########################################################################################################################################

@forum_bp.route('/comment/<int:comment_id>/like')
def add_comment_like(comment_id):
    """Endpoint to create a new UpvoteComment. 
    
    Accepts a Comment ID and will create a new UpvoteComment instance and commit it to the DB.
    
    Returns JSON."""
    
    if not g.user:
        return jsonify(dict(message='You need to be logged in to do that.', category='danger'))
    
    new_like = UpvoteComment.create_new_comment_upvote(comment_id=comment_id)
    
    if new_like:
        return jsonify(dict(message='Add Successful.'))
    else:
        return jsonify(dict(message='Something went wrong.'))


##########################################################################################################################################
    
@forum_bp.route('/comment/<int:comment_id>/unlike')
def remove_comment_like(comment_id):
    """Endpoint to 'Unlike' a comment.
    
    Will accept a Comment ID and remove the UpvoteComment from the DB.
    
    Returns JSON."""
    
    if not g.user:
        return jsonify(dict(message='You need to be logged in to do that.', category='danger'))
    
    upvote = UpvoteComment.query.filter(UpvoteComment.user_id==g.user.id, UpvoteComment.comment_id==comment_id).first()
    
    db.session.delete(upvote)
    
    try:
        db.session.commit()
    except:
        return jsonify(dict(message='Something went wrong.'))
    
    return jsonify(dict(message='Remove Successful.'))


##########################################################################################################################################
    
@forum_bp.route('/post/<int:post_id>/like')
def add_post_like(post_id):
    """Endpoint to create a new UpvotePost. 
    
    Accepts a Post ID and will create a new UpvotePost instance and commit it to the DB.
    
    Returns JSON."""
    
    if not g.user:
        return jsonify(dict(message='You need to be logged in to do that.', category='danger'))
    
    new_like = UpvotePost.create_new_post_upvote(post_id = post_id)
    
    if new_like:
        return jsonify(dict(message='Add Successful.'))
    else:
        return jsonify(dict(message='Something went wrong.'))


##########################################################################################################################################
    
@forum_bp.route('/post/<int:post_id>/unlike')
def remove_post_like(post_id):
    """Endpoint to 'Unlike' a Post.
    
    Will accept a Post ID and remove the UpvotePost from the DB.
    
    Returns JSON."""
    
    if not g.user:
        return jsonify(dict(message='You need to be logged in to do that.', category='danger'))
    
    upvote = UpvotePost.query.filter(UpvotePost.user_id==g.user.id, UpvotePost.post_id==post_id).first()
    
    db.session.delete(upvote)
    
    try:
        db.session.commit()
    except:
        return jsonify(dict(message='Something went wrong.'))
    
    return jsonify(dict(message='Remove Successful.'))


##########################################################################################################################################

@forum_bp.route('/post/remove/<int:post_id>')
def remove_post(post_id):
    """Endpoint to remove a Post from the DB. 
    
    Accepts a Post ID. Will redirect to Forum Index page on successful removal.
    Else will redirect to Post details page."""
    
    if not g.user:
        flash('You need to be logged in to do that.', 'danger')
        return redirect(f'/forum/post/{post_id}')
    
    was_deleted = Post.remove_post(id=post_id)
    
    if was_deleted:
        flash('Post successfully removed', 'success')
        return redirect('/forum')
    
    flash('Something went wrong. Please try again later.', 'danger')
    return redirect(f'/forum/post/{post_id}')


##########################################################################################################################################

@forum_bp.route('/post/<int:post_id>/comment/remove/<int:comment_id>')
def remove_comment(post_id, comment_id):
    """Endpoint to remove a Comment from the DB.
    
    Accepts a Post AND Comment ID. Will redirect to Post details page."""
    
    if not g.user:
        flash('You need to be logged in to do that.', 'danger')
        return redirect(f'/forum/post/{post_id}')
    
    was_deleted = Comment.remove_comment(id=comment_id)
    
    if was_deleted:
        flash('Comment removed.', 'success')
        return redirect(f'/forum/post/{post_id}')
    
    flash("Something went wrong. Please try again later.", 'danger')
    return redirect(f'/forum/post/{post_id}')


##########################################################################################################################################

@forum_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    """Endpoint to edit a Post. 
    
    Accepts both a GET and POST request.
    
    GET requests will render the Post edit page with a form.
    
    POST requests will take the form data and alter the Post's details and commit
    it to the DB. Redirects to Post details page on successfuly commit."""

    if not g.user:
        flash('You need to be logged in to do that.', 'danger')
        return redirect('/users/login')
    
    post = Post.query.get_or_404(post_id)
    
    if post.user.id != g.user.id:
        flash('You can only edit your own posts.', 'danger')
        return redirect(f'/forum/post/{post_id}')
    
    form = NewPostForm(obj=post)
    
    if form.validate_on_submit():
        post_edited = Post.edit_post(post=post, title=form.title.data, content=form.content.data)
        
        if post_edited:
            flash('Post successfully updated.', 'success')
            return redirect(f'/forum/post/{post_id}')
        else:
            flash('Something went wrong. Please try again later.', 'danger')
            return redirect(f'/forum/post/{post_id}')
        
    return render_template('forum/edit_post.html', form=form)


##########################################################################################################################################

@forum_bp.route('/comment/<int:comment_id>/edit', methods=['POST'])
def edit_comment(comment_id):
    """Endpoint to edit a Comment. 
    
    Accepts only a POST request. Returns JSON."""
    
    if not g.user:
        flash('You need to be logged in to do that.', 'danger')
        return redirect('/users/login')
    
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.user_id != g.user.id:
        flash('You can only edit your own comments.', 'danger')
        return redirect(f'/forum/post/{comment_id}')
    
    comment_edited = Comment.edit_comment(comment=comment, content=request.args['content'])
    if comment_edited:
        return jsonify(dict(message='Success', content=request.args['content']))
    else:
        return jsonify(dict(message='Something went wrong. Please try again later.', category='danger' ))


##########################################################################################################################################