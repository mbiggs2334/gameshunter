from flask import render_template, redirect, session, flash, g, request
from .forms import SignUpForm, LoginForm, ReverifyEmailForm, EditPasswordForm, EditProfileForm, DeleteAccountForm, ReportUserForm
from .models import FavoriteGames, User, Block, Conversation, Follow, PastUsernames
from gamehunter.db import db
from sqlalchemy.exc import IntegrityError
from .functions import login, logout
from .functions import verify_password_match
from blueprints.blueprints import users_bp


##########################################################################################################################################

@users_bp.route('/signup', methods=['GET', 'POST'])
def user_signup():
    """Endpoint for the User signup page. 
    
    Accepts both a GET and POST requst.
    
    GET requests will render the signup page.
    
    POST requests will take the form data and create a new User."""

    if g.user:
        flash('You already have an account.', 'danger')
        return redirect('/')
    
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            
        except IntegrityError as e:
            einfo = e.orig.args
            if einfo[0].find('users_email_') != -1:
                flash('Email is already in use. Please make another selection.',  'danger')
                
            elif einfo[0].find('users_username_') != -1:
                flash("That username is already in use. Please make another selection.",  'danger')
                
            return render_template('users/sign_up.html', form=form)
        
        session['email'] = form.email.data
        return redirect('/emails/confirm/send')

    return render_template('users/sign_up.html', form=form)
    

##########################################################################################################################################
    
@users_bp.route('/login', methods=['GET', 'POST'])
def login_user():
    """Endpoint for the User login page.
    
    Accepts both a GET and POST request.
    
    GET requests will render the login page with a form.
    
    POST requests will take form info and login the User if valid credentials are given."""
    
    if g.user:
        flash("You're already logged in.", 'danger')
        return redirect('/')
    
    form = LoginForm()
    if form.validate_on_submit():
        
        email = form.email.data
        password = form.password.data
        user = User.authenticate_user(email, password)
        
        if user:
            if user.email_confirmed:
                login(user)
                flash(f'Welcome back, {user.username}!', 'success')
                return redirect('/')
            else:
                flash("Account is unverified. If you need another verification email, please select 'Having trouble logging in?'", 'danger')
                return render_template('users/login.html', form=form)
            
        else:
            flash('Invalid Credentials. Please make sure you have entered your information correctly', 'danger')
            return render_template('users/login.html', form=form)
        
    return render_template('users/login.html', form=form)


##########################################################################################################################################

@users_bp.route('/logout')
def logout_user():
    """Endpoint to logout the User."""
    
    if not g.user:
        flash('Access unauthorized. You need to be logged in to do that.', 'danger')
        return redirect('/')
    
    logout()
    
    if 'curr_user' not in session:
        flash("Successly logged out.", 'success')
        return redirect('/')
    
    else:
        flash('There was a problem. Please try again later.', 'danger')
        return redirect('/')


##########################################################################################################################################

@users_bp.route('/<int:id>/profile')
def user_profile(id):
    """Endpoint to render the selected User's profile."""
    
    if not g.user:
        flash("You need to be logged in to do that.", 'danger')
        return redirect('/')
    
    user = User.query.get_or_404(id)
    is_blocked = User.check_if_g_user_blocked(user.id)
    
    if is_blocked:
        flash('Access unauthorized. This user has blocked you.', 'danger')
        return redirect('/')
    
    if g.user.id != id:
        has_conversation = Conversation.check_for_existing_conversation(other_user=user)
        return render_template('users/user_profile.html', user=user, convo_id=has_conversation)
    
    return render_template('users/user_profile.html', user=user)


##########################################################################################################################################


@users_bp.route('/<int:id>/profile/edit', methods=['GET', 'POST'])
def edit_user_profile(id):
    """Endpoint to render the User's Account/Profile edit page.
    
    Accepts both a GET and POST request.
    
    GET requests will render the appropriate HTML while passing in a form.
    
    POST requests will take profile changes and submit them in the DB."""
    
    if not g.user:
        flash('You need to be logged in to do that.', 'danger')
        return redirect('/')
    
    if id != g.user.id:
        flash('Access unauthorized.', 'danger')
        return redirect('/')
    
    form = EditProfileForm(obj=g.user) 
    if form.validate_on_submit():
        stored = PastUsernames.store_old_username(g.user.username)
        if not stored:
            flash('Something went wrong. Please try again later.', 'danger')
            return redirect(f'/users/{id}/profile/edit')
     
        if request.files['profile_image']:
            User.change_user_image(file=request.files['profile_image'] )
        
        info_updated = User.update_user_info(form=form)
        if info_updated:
            flash('Changes saved successfully.', 'success')
            return render_template('users/edit_profile.html', form=form)
        flash('Something went wrong. Please try again later.', 'danger')
        return redirect(f'/users/{id}/profile/edit')
    
    return render_template('users/edit_profile.html', form=form)


##########################################################################################################################################

@users_bp.route('/login/verify', methods=['GET', 'POST'])
def resend_verify_email():
    """Enpoint to render the page to resend the verifcation email.
    
    Will only send the email if the account both exists and is unverified."""

    if g.user:
        flash('Your account has already been verified.', 'danger')
        return redirect('/')
    
    form = ReverifyEmailForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        
        if user:
            if user.email_confirmed:
                flash('If there is an account associated with this email address, you will receive a verification link shortly.', 'central-blue')
                return redirect('/')
            elif not user.email_confirmed:
                session['email'] = user.email
                return redirect('/emails/confirm/resend')
            
        else:
            flash('If there is an account associated with this email address, you will receive a verification link shortly.', 'central-blue')
            return redirect('/')
        
    return render_template('users/resend_email_verify.html', form=form)


##########################################################################################################################################


@users_bp.route('/account/password/edit', methods=['GET', 'POST'])
def edit_password():
    """Endpoint to render the edit password page """
    
    if not g.user:
        flash('You need to be logged in to do that.', 'danger')
        return redirect('/')
    
    form = EditPasswordForm()
    if form.validate_on_submit():
        user = User.authenticate_user(email=g.user.email, password=form.password.data)
        
        good_pass = verify_password_match(original_pass=form.password.data, new_password=form.new_password.data, new_password_confirm=form.new_password_confirm.data)
        
        if not good_pass:
            return redirect('/')
        
        if user:
            g.user.change_password(form.new_password.data)
            flash('Password successfully changed!', 'success')
            return redirect('/')
        
        elif not user:
            flash("Invalid credentials. Please assure you've entered the information correctly.", 'danger')
            return render_template('users/change_password.html', form=form)
    
    return render_template('users/change_password.html', form=form)
    

##########################################################################################################################################  


@users_bp.route('/forgotpassword', methods=['GET', 'POST'])
def email_password_reset():
    """Endpoint for the forgot password page.
    
    Accepts both a GET and POST request.
    
    GET requests will render forgot password page with form.
    
    POST request will redirect to the EmailHandler."""
    
    form = ReverifyEmailForm()
    if form.validate_on_submit():
        email = form.email.data
        session['email'] = email
        return redirect('/emails/resetpassword')
    
    return render_template('users/email_password_change.html', form=form)


##########################################################################################################################################


@users_bp.route('/<int:id>/favorites', methods=['GET', 'POST'])
def user_favorites(id):
    """Endpoint to show the User's favorites. 
    
    Accepts both a GET and POST request.
    
    GET requests will render the User's favorites page.
    
    POST requests will update the user's favorites."""
    
    user = User.query.get_or_404(id)
        
    if request.method == 'POST':
        if not g.user:
            flash('Access Unauthorized.', 'danger')
            return redirect(f'/users/{id}/favorites')
        
        favs_edited = FavoriteGames.edit_user_favorites(form=request.form)
        
        if favs_edited:
            flash('Favorites sucessfully updated.', 'success')
            return redirect(f'/users/{id}/favorites')
        else:
            flash('Something went wrong. Please try again later.', 'danger')
            return redirect(f'/users/{id}/favorites')
    
    return render_template(f'users/favorites.html', user=user)


##########################################################################################################################################

@users_bp.route('/<int:id>/block')
def block_user(id):
    """Endpoint for one user to block another. """

    if not g.user:
        flash('You need to be logged in to do that.', 'danger')
        return redirect('/users/login')
    
    if id == g.user.id:
        flash("You shouldn't block yourself you goober.", 'central-blue')
        return redirect(f'/users/{id}/profile')
    
    is_blocked = User.check_if_g_user_blocked(id)
    if is_blocked:
        flash('This user is already blocking you.', 'central-blue')
        return redirect('/')
    
    else:
        user = User.check_if_g_user_blocking(id)
        if not user:
            user = User.query.get_or_404(id)
            new_block = Block.create_new_block(user=user)
            if new_block:
                flash('You are now blocking this user.', 'success')
                return redirect(f'/users/{id}/profile')
            else:
                flash('Something went wrong. Please try again later.', 'danger')
                return redirect(f'/users/{id}/profile')
            
        else:
            flash("You're already blocking this user.", 'central-blue')
            return redirect(f'/users/{id}/profile')
    
    
##########################################################################################################################################
    
@users_bp.route('/<int:id>/unblock')
def unblock_user(id):
    """Endpoint for one User to Unblock another User."""
    
    if not g.user:
        flash("You need to be logged in to do that.", 'danger')
        return redirect('/users/login')
    
    if id == g.user.id:
        flash("You aren't blocking yourself.", 'central-blue')
        return redirect(f'/users/{id}/profile')
    
    is_blocking = User.check_if_g_user_blocking(id)
    if is_blocking:
        block_removed = Block.remove_block(id=id)
        if not block_removed:
            flash('Something went wrong. Please try again later.', 'danger')
            return redirect(f'/users/{id}/profile')
        flash('User unblocked.', 'success')
        return redirect(f'/users/{id}/profile')
    else:
        is_blocked = User.check_if_g_user_blocked(id)
        if is_blocked:
            flash('Access unauthorized. This user has blocked you.', 'danger')
            return redirect('/')
        flash("You haven't blocked this user.", 'central-blue')
        return redirect(f'/users/{id}/profile')
    
    
##########################################################################################################################################

@users_bp.route('/<int:user_id>/follow')
def follow_user(user_id):
    """Endpoint to create a new Follow. """

    if not g.user:
        flash('You need to be logged in to do that', 'danger')
        return redirect(f'/users/{user_id}/profile')
    
    is_following = Follow.check_if_following(id=user_id)
    if is_following:
        flash(f"You are already following this user.", 'central-blue')
        return redirect(f'/users/{user_id}/profile')
    
    else:
        follow_created = Follow.create_new_follow(id=user_id)
        if follow_created:
            flash(f'You are now following this user.', 'success')
            return redirect(f'/users/{user_id}/profile')
        else:
            flash("Something went wrong. Please try again later", 'danger')
            return redirect(f'/users/{user_id}/profile')
        
    

##########################################################################################################################################


@users_bp.route('/<int:user_id>/unfollow')
def unfollow_user(user_id):
    """Endpoint for one user to Unfollow another."""
    
    if not g.user:
        flash('You need to be logged in to do that', 'danger')
        return redirect(f'/users/{user_id}/profile')
    
    is_following = Follow.check_if_following(id=user_id)
    if is_following:
        follow_removed = Follow.remove_follow(is_following)
        if follow_removed:
            flash('You are no longer following this user.', 'success')
            return redirect(f'/users/{user_id}/profile')
        else:
            flash('Something went wrong. Please try again later.', 'danger')
            return redirect(f'/users/{user_id}/profile')
        
    else:
        flash("You aren't following this user.", 'dangerret')
        return redirect(f'/users/{user_id}/profile')
    
    
##########################################################################################################################################

    
@users_bp.route('/account/delete', methods=['GET', 'POST'])
def delete_user_account():
    """Endpoint to for account deletion.
    
    Accepts a GET and POST request.
    
    GET requests will render the HTML doc and pass in a Form.
    
    POST requests will delete the User account."""
    
    if not g.user:
        flash("You need to be logged in to do that.", 'danger')
        return redirect('/users/login')
    
    form = DeleteAccountForm()
    if form.validate_on_submit():
        was_deleted = User.delete_account()
        if was_deleted:
            return redirect('/')
        return redirect(f'/users/{g.user.id}/profile/edit')
    
    return render_template('users/delete_account.html', form=form)


##########################################################################################################################################


@users_bp.route('/<int:user_id>/report', methods=['GET', 'POST'])
def report_user(user_id):
    """Endpoint for one User to report another.
    
    Accepts a GET and POST request.
    
    GET requests will render the form to report a specific User.
    
    POST requests will take the User submitted report and pass it to the support email."""
    
    if not g.user:
        flash('You need to be logged in to do that.', 'danger')
        return redirect('/')
    
    form = ReportUserForm()
    if form.validate_on_submit():
        session['reportMessage'] = form.report_message.data
        return redirect(f'/emails/report/{user_id}')
    
    return render_template('users/report.html', form=form)