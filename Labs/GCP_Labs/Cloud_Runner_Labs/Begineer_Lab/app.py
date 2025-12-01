from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Change this to a fixed secret key in production

# Form class for the contact form
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=100)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # In a real app, you would process the form data here
        # For example, send an email or save to a database
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    # If there are form validation errors, they'll be displayed automatically
    # by the template due to the form validation in the template
    return render_template('contact.html', form=form)

# API endpoint example
@app.route('/api/data')
def get_data():
    return jsonify({
        'status': 'success',
        'data': {
            'message': 'This is a sample API endpoint',
            'version': '1.0',
            'endpoints': [
                {'url': '/api/data', 'method': 'GET', 'description': 'Get sample data'},
                {'url': '/api/contact', 'method': 'POST', 'description': 'Submit contact form'}
            ]
        }
    })

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Run the app
    app.run(host="0.0.0.0", port=8080, debug=True)