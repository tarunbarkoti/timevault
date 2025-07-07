from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import MessageForm
from .models import Message, db

# Blueprint must be defined at the top
main = Blueprint('main', __name__)

# Home route
@main.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

# Compose route
@main.route('/compose', methods=['GET', 'POST'])
@login_required
def compose():
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(
            content=form.content.data,
            unlock_date=form.unlock_date.data,
            user_id=current_user.id
        )
        db.session.add(message)
        db.session.commit()
        flash("Your message has been locked in TimeVault! 🔒")
        return redirect(url_for('main.home'))  # redirect to home or dashboard
    return render_template('compose.html', form=form)
