"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify
from app.forms import UserForm
from app.models import User, Food
# import sqlite3

###
# Routing for your application.
###

@app.route('/', methods=['POST', 'GET'])
def home():
    """Render website's home page."""
    users = db.session.query(User).all()

    if request.method == 'POST':
        user_id = request.form['user_id']
        food = request.form['food']

        existing_food = Food.query.filter_by(name=food).first()
        if existing_food:
            flash('Food already exists')

        else:
            new_food = Food(food)
            db.session.add(new_food)
            db.session.commit()
            flash('Food {} successfully added'.format(food))


    return render_template('home.html', users=users)

@app.route('/suggest-food', methods=['GET', 'POST'])
def suggest_food():
    term = request.args.get('term')
    matching_foods = Food.query.filter(Food.name.like(f'%{term}%')).all()
    suggestions = [food.name for food in matching_foods]
    return jsonify(suggestions)


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/users')
def show_users():
    users = db.session.query(User).all() # or you could have used User.query.all()

    return render_template('show_users.html', users=users)

@app.route('/add-user', methods=['POST', 'GET'])
def add_user():
    user_form = UserForm()

    if request.method == 'POST':
        if user_form.validate_on_submit():
            # Get validated data from form
            name = user_form.name.data # You could also have used request.form['name']

            # save user to database
            user = User(name)
            db.session.add(user)
            db.session.commit()

            flash('User successfully added')
            return redirect(url_for('show_users'))

    flash_errors(user_form)
    return render_template('add_user.html', form=user_form)

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
