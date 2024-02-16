from flask import Flask, request, render_template, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash
from flask_bootstrap import Bootstrap
import os
from sqlalchemy import func

# Assuming models.py and auth_blueprint.py are properly set up
from models import db, Evaluation, Criteria, User
from auth_blueprint import auth_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaluations.db'
app.config['SECRET_KEY'] = "sdfawfeaw2b9a5d0208a72aasdqw1231234feba25506"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(auth_blueprint, url_prefix='/')

db.init_app(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/consent')
def consent():
    return render_template('consent.html')  

@app.route('/criteria')
def criteria():
    return render_template('criteria.html')  


@app.route('/')
@login_required
def index():
    stories_dir = os.path.join('static', 'stories')
    projects = [project.replace(".txt","") for project in os.listdir(stories_dir)]

    # Determine evaluation progress for each project
    project_evaluations = {}
    depiction = {}
    for project in projects:
        evaluations_count = Evaluation.query.filter_by(evaluator_id=current_user.id, project_name=project).count()
        project_evaluations[project] = evaluations_count > 0
        depiction[project] = url_for('static', filename=f'depiction/{project}.jpg')
    
    return render_template('index.html', projects=projects, project_evaluations=project_evaluations, depiction=depiction)

@app.route('/compare', methods=['GET'])
@login_required
def compare():
    project = request.args.get('project', 'default_project')
    stories_dir = os.path.join(app.static_folder, 'stories', f'{project}.txt')
    depiction_img = url_for('static', filename=f'depiction_small/{project}.jpg')
    description_dir = os.path.join(app.static_folder, 'description', f'{project}.txt')
    methods = ['gpt-3.5', 'gpt-4', 'llama2', 'mixtral']
    
    # Mapping real method names to user-friendly labels
    method_labels = {method: label for method, label in zip(methods, ['A', 'B', 'C', 'D'])}
    
    user_stories = []
    description = ""
    if os.path.exists(stories_dir):
        with open(stories_dir, 'r') as file:
            user_stories = file.read().strip().split('\n')
            
    if os.path.exists(description_dir):
        with open(description_dir, 'r') as file:
            description = file.read().strip()
    
    images = {}
    for method in methods:
        image_path = os.path.join(app.static_folder, 'images', method, f'{project}.drawio.png')
        if os.path.isfile(image_path):
            images[method_labels[method]] = url_for('static', filename=f'images/{method}/{project}.drawio.png')
        else:
            images[method_labels[method]] = None
    
    criteria_list = Criteria.query.all()
    criteria = {criterion.name: criterion.id for criterion in criteria_list}
    
    evaluations = {}
    # Fetch evaluations if any exist for the current user and project
    for criterion in criteria_list:
        evaluations[criterion.name] = {}
        for method in methods:
            eval = Evaluation.query.filter_by(project_name=project, criteria_id=criterion.id, method=method, evaluator_id=current_user.id).first()
            evaluations[criterion.name][method_labels[method]] = eval.score if eval else None

    return render_template('compare.html', project=project, user_stories=user_stories, images=images, criteria=criteria, evaluations=evaluations, depiction_img=depiction_img, description=description)


@app.route('/submit_evaluation', methods=['POST'])
@login_required
def submit_evaluation():
    project = request.form.get('project')

    # Invert the method_labels mapping
    method_labels = {label: method for method, label in zip(['gpt-3.5', 'gpt-4', 'llama2', 'mixtral'], ['A', 'B', 'C', 'D'])}
    
    # Extract and process scores from form data
    for key, value in request.form.items():
        if key.startswith('scores_'):
            _, label, criteria_id = key.split('_')
            score = value
            method = method_labels[label]  # Translate label back to method name
            # Save the evaluation to the database
            new_evaluation = Evaluation(evaluator_id=current_user.id, project_name=project, method=method, criteria_id=int(criteria_id), score=int(score))
            db.session.add(new_evaluation)
    db.session.commit()
    return redirect(url_for('compare', project=project))


@app.route('/results')
@login_required
def results():
    criteria_scores = db.session.query(
        Criteria.name,
        Evaluation.method,
        func.avg(Evaluation.score).label('average_score')
    ).join(Evaluation, Criteria.id == Evaluation.criteria_id) \
     .group_by(Criteria.name, Evaluation.method) \
     .all()

    # Convert query results to a nested dictionary for easier use in the template
    scores_dict = {}
    for criteria_name, method, average_score in criteria_scores:
        if criteria_name not in scores_dict:
            scores_dict[criteria_name] = {}
        scores_dict[criteria_name][method] = round(average_score, 2)

    return render_template('results.html', scores=scores_dict)



def add_criteria():
    criteria_list = [
        {'name': 'Completeness', 'description': 'Assess whether the DFD includes all necessary components (processes, data stores, external entities, and data flows) to describe the system accurately.'},
        {'name': 'Correctness', 'description': 'Evaluate if the processes described correctly reflect the actual data processing steps, data flows correctly represent the data movement, and external entities and data stores are correctly identified.'},
    ]
    for criteria in criteria_list:
        if not Criteria.query.filter_by(name=criteria['name']).first():
            new_criteria = Criteria(name=criteria['name'], description=criteria['description'])
            db.session.add(new_criteria)
    db.session.commit()


if __name__ == '__main__':
    # Execute only once
    # with app.app_context():
    #     db.create_all()
    #     initial_user = User(username="put_your_username", 
    #                         email="put_your_email",
    #                         password=generate_password_hash("put_your_password"),
    #                         is_active=True,
    #                         has_consented=True)

    #     db.session.add(initial_user)
    #     db.session.commit()
        
    #     add_criteria()
       
    app.run(port=6970, debug=True)
