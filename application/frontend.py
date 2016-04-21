# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Blueprint, render_template, flash, redirect, url_for, \
    current_app
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from flask_security import login_required, roles_required, current_user
from markupsafe import escape

from .forms import SignupForm
from .nav import nav, ExtendedNavbar

frontend = Blueprint('frontend', __name__)


# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.
def frontend_top_nav():
        navbar = ExtendedNavbar(
            View(current_app.config['SITE_TITLE'], 'frontend.index'),
            root_class='navbar navbar-inverse navbar-fixed-top',
            items = (
                View('Home', 'frontend.index'),
                View('Members', 'frontend.members'),
            )
        )
        if current_user.is_active:
            navbar.right_items = (
                View('Logout {}'.format(current_user.email), 'security.logout'),
                View('Change password', 'security.change_password'),
            )
            if current_user.has_role('admin'):
                navbar.right_items = \
                    (View('User admin', 'useradmin.index'),)\
                        +navbar.right_items
            if current_user.has_role('editor'):
                navbar.right_items = \
                    (View('Site editor', 'frontend.site_editor'),)\
                        +navbar.right_items
                
        else:
            navbar.right_items = ( View('Login', 'security.login'), )
        return navbar

nav.register_element('frontend_top', frontend_top_nav)

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/members')
@login_required
def members():
    return render_template('members.html')

@frontend.route('/site-editor')
@login_required
@roles_required('editor')
def site_editor():
    return render_template('site_editor.html')

