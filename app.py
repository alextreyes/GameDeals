"""GameDeals application."""

from flask import Flask, request, render_template,  redirect, flash, session, g, url_for,jsonify, abort
import requests
from models import db,  connect_db, User, UserList, UserListGame, Like
from forms import UserForm, LoginForm, ListForm
from sqlalchemy.exc import IntegrityError    

app = Flask(__name__)

CURR_USER_KEY = "curr_user"


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gamedeals'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
app.config['SQLALCHEMY_ECHO'] =  True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True

connect_db(app)

# user login/ sign out

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/check-authentication', methods=['GET'])
def check_authentication():
    if CURR_USER_KEY in session:
        return jsonify({'isLoggedIn': True})
    else:
        return jsonify({'isLoggedIn': False})


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    form = UserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                profile_pic=form.profile_pic.data 
                
 
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form, g=g)
    
@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash(message="Successfully logged out")
    return redirect("/")

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

@app.route("/", methods=["GET"])
def render_home():
    """Renders homepage."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

    return render_template("home.html", user=g.user)



@app.route("/Bdeals")
def render_Bdeals():
    """Renders Best Deals"""
    url = "https://www.cheapshark.com/api/1.0/deals"
    params = {
        "storeID": "1",
        "sortBy":"DealRating",
        "pageSize":"6"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Pass the data to the template
        print(url)
        return render_template('Bdeals.html', deals=data, user=g.user)
    else:
        return "Failed to fetch data from API"
    
@app.route("/Bgames")
def render_Bgames():
    """Renders Best Games"""
    url = "https://www.cheapshark.com/api/1.0/deals"
    params = {
        "storeID": "1",
        "sortBy":"Metacritic",
        "pageSize":"12",
        "onSale": "1"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Pass the data and user to the template
        return render_template('Bgames.html', deals=data, url=url, user=g.user)
    else:
        return "Failed to fetch data from API"
    

    
@app.route('/lists', methods=["GET"])
def show_lists():
    """Show game lists"""
    
    if g.user:
        user = g.user
        
        all_lists = UserList.query.all()
        print(all_lists)
        if all_lists:
            liked_list = []
            for likes in user.likes:
                liked_list.append(likes.list_id)
            
            return render_template('lists.html', liked_list=liked_list, all_lists=all_lists, user=user)
        
        return render_template('lists.html', liked_list=liked_list, all_lists=all_lists)
    else:
        flash("Log in or Sign up to access best lists!")
        return render_template('home.html') 
    
@app.route("/lists/new", methods = ["GET", "POST"])
def show_create_list():
    """shows and creates a new list"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = ListForm()

    if form.validate_on_submit():
        list = UserList(list_name=form.list_name.data, user_id=g.user.id)
        g.user.lists.append(list)
        db.session.commit()

        return redirect("/lists")

    return render_template('list_new.html', form=form)

@app.route("/lists/<int:list_id>/delete", methods=["POST"])
def delete_list(list_id):
    """Deletes list."""
    # Retrieve the list from the database
    list_to_delete = UserList.query.get(list_id)
    
    # Check if the list exists
    if not list_to_delete:
        abort(404, "List not found")

    # Delete the list
    db.session.delete(list_to_delete)
    db.session.commit()

    flash("List deleted successfully")
    # Redirect the user back to the user page
    return redirect(url_for('render_user_page', user_id=list_to_delete.user_id))


@app.route("/lists/<int:list_id>", methods=["GET"])
def show_list(list_id):
    """shows specific list with games"""
    # Fetch the list object by its ID
    user_list = UserList.query.filter_by(id=list_id).first()

    # Check if the list exists
    if user_list:
        # Assuming you have a relationship between UserList and games, you can access the associated games like this:
        games = user_list.games
        return render_template("gameList.html", list=user_list, games=games)
    else:
        # Handle the case where the list with the given ID doesn't exist
        flash("List not found", "error")
        return redirect('/lists') 

@app.route('/lists/add_game', methods=['POST'])
def add_game_to_list():
    game_id = request.form.get('game_id')
    list_id = request.form.get('list_id')

    # Check if the game already exists in the user's list
    existing_game = UserListGame.query.filter_by(list_id=list_id, game_id=game_id).first()
    if existing_game:
        # Game already exists in the list, handle accordingly
        flash("Game already exists in the list")
        return redirect(f'/lists/{list_id}')

    # If the game doesn't exist, add it to the list
    name = request.form.get('title')
    thumbnail = request.form.get('thumbnail')
    webpage = request.form.get('deal_webpage')
    metacritic = request.form.get('metacritic')
    rating = request.form.get('rating')

    new_game = UserListGame(list_id=list_id, game_id=game_id, name=name, thumbnail=thumbnail, webpage=webpage, rating=rating, metacritic=metacritic )
    db.session.add(new_game)
    db.session.commit()

    flash("Game added to list successfully")
    return redirect(f'/lists/{list_id}')

@app.route('/lists/<int:list_id>/remove_game', methods =['POST'])
def remove_game_from_list(list_id):
    """Removes game from list"""
    user = g.user
    if not user:
        # will need to make this better, to redirect to an error page or another page with an error 
        return redirect('/')
    
    list_to_modify = UserList.query.get(list_id)

    if not list_to_modify:
        # Handle the case where the list doesn't exist
        return "List not found", 404  # Return a 404 status code    

    game_id = request.form.get('game_id')
    game_to_remove = UserListGame.query.filter_by(list_id=list_id, game_id=game_id).first()

    if not game_to_remove:
        # Handle the case where the game is not in the list
        return "Game not found in the list", 404  # Return a 404 status code

    # Remove the game from the list
    db.session.delete(game_to_remove)
    db.session.commit()    

    # liked_game_list = []
    # for liked_games in user.lists[list_id]:
    #     liked_game_list.append(liked_games.game_id)
    # print(liked_game_list)
    return redirect(f'/lists/{list_id}')
    



@app.route('/lists/add_like/<int:list_id>', methods=["POST"])
def add_like(list_id):
    """interact with likes"""
    #  user is logged in
    print(list_id)
    user = g.user
    print(user.id)
    if not user:
        return render_template("lists.html")

    # Check if the list is already liked by the user

    liked_list = []
    for likes in user.likes:
        liked_list.append(likes.list_id)
    print(liked_list)
    if list_id in liked_list:
        # Unlike the list
        Like.query.filter_by(user_id=user.id, list_id=list_id).delete()
        db.session.commit()
        return redirect('/lists')
    else:
        # Like the list
        user_liked = Like(user_id=user.id, list_id=list_id)
        db.session.add(user_liked)
        db.session.commit()
        return redirect('/lists')

@app.route("/users/<int:user_id>", methods=["GET"])
def render_user_page(user_id):
    """Renders user page"""
    user = User.query.get(user_id)  
    if user is None:
        # Handle the case where the user does not exist
        return "User not found", 404

    # Retrieve all lists associated with the user
    all_lists = UserList.query.filter_by(user_id=user_id).all()

    return render_template("/users/user_page.html", user=user, all_lists=all_lists)