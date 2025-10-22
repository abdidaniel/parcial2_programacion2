from flask import Flask, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import User, Task, db
from forms import SignupForm, LoginForm, TaskForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-super-segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:postgres123@localhost:5432/taskflow_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Inicializar extensiones
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


# Ruta de la página de inicio (mostrar tareas)
@app.route('/')
@login_required
def home():
    tasks = Task.query.filter_by(user_id=current_user.id).all()  # Mostrar tareas del usuario actual
    return render_template('index.html', tasks=tasks)


# Ruta de detalle de la tarea
@app.route('/task/<slug>/')
def task_view(slug):
    task = Task.get_by_slug(slug)
    if task is None:
        abort(404)
    return render_template('task_view.html', task=task)


# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Login failed. Please check your email and password.')
    return render_template('login_form.html', form=form)


# Ruta de registro (signup)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignupForm()
    
    # Debug logging
    app.logger.info(f"Form data received: {request.form}")
    
    if form.validate_on_submit():
        try:
            # Create user
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            
            # Explicit transaction handling
            db.session.add(user)
            try:
                db.session.commit()
                app.logger.info(f"Created user: {user.username}")
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"DB Error: {e}")
                return jsonify({"error": "Database error", "details": str(e)}), 500
            
            # Login the user
            login_user(user)
            
            # API response for Postman
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    "status": "success",
                    "message": "User created successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    }
                }), 201
            
            # Browser response
            flash('Account created successfully!')
            return redirect(url_for('home'))
            
        except Exception as e:
            app.logger.error(f"Error in signup: {e}")
            if request.headers.get('Accept') == 'application/json':
                return jsonify({"error": str(e)}), 500
            flash('Error creating account')
            
    # Validation failed
    if request.method == 'POST':
        app.logger.warning(f"Validation errors: {form.errors}")
        if request.headers.get('Accept') == 'application/json':
            return jsonify({"errors": form.errors}), 400
    
    return render_template('signup_form.html', form=form)


# Ruta de logout
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))


@app.route('/admin/task/', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            user_id=current_user.id
        )
        task.save()
        flash('Tarea creada exitosamente', 'success')
        return redirect(url_for('home'))
    return render_template('admin/task_form.html', form=form)

# Ruta para editar tarea
@app.route('/admin/task/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(slug):
    task = Task.query.filter_by(slug=slug).first_or_404()
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        # ❌ task.status = form.status.data  ← eliminar esta línea
        db.session.commit()
        flash('Tarea actualizada correctamente', 'success')
        return redirect(url_for('home'))
    return render_template('admin/task_form.html', form=form)



# Ruta para eliminar tarea
@app.route('/admin/task/<slug>/delete', methods=['POST'])
@login_required
def delete_task(slug):
    task = Task.get_by_slug(slug)
    if task is None or task.user_id != current_user.id:
        abort(403)

    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!')
    return redirect(url_for('home'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    task.is_done = not task.is_done
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database tables created")
    print("🚀 Starting server...")
    app.run(debug=True)
