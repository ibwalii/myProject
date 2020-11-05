from flask import Flask, render_template

from forms import RegistrationForm

app = Flask(__name__)

app.config ['SECRET_KEY'] = 'f1b4c8ba43d3e1c31004b7055e368fbc'

posts = [
    {
        'author': 'ibrahim bakari',
        'title': 'test 1',
        'content': 'testing content 1',
        'date_posted': 'Nov 5, 2020'
    },
    {
        'author': 'ibrahim bakari',
        'title': 'test 1',
        'content': 'testing content 1',
        'date_posted': 'Nov 5, 2020'
    }

]

@app.route('/')
def home():
    return render_template('home.html', posts= posts)

@app.route('/about')
def about():
    return render_template('about.html', title='about us')

@app.route('/login')
def login():
    return render_template('about.html', title='about us') 

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Registration', form = form)


if __name__ == "__main__":
    app.run(debug=True)