from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200))
    status = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)

@app.route('/')
def list_jobs():
    jobs = Job.query.all()
    return render_template('list_jobs.html', jobs=jobs)

@app.route('/create', methods=['GET', 'POST'])
def create_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        url = request.form['url']
        status = request.form['status']
        description = request.form['description']
        job = Job(title=title, company=company, url=url, status=status, description=description)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('list_jobs'))
    return render_template('create_job.html')

@app.route('/job/<int:id>')
def job_detail(id):
    job = Job.query.get_or_404(id)
    return render_template('job_detail.html', job=job)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_job(id):
    job = Job.query.get_or_404(id)  # Retrieve the job entry by ID

    if request.method == 'POST':
        job.title = request.form['title']
        job.company = request.form['company']
        job.url = request.form['url']
        job.status = request.form['status']
        job.description = request.form['description']
        db.session.commit()
        return redirect(url_for('job_detail', id=job.id))
    return render_template('edit_job.html', job=job)

@app.route('/job/<int:id>/delete', methods=['POST'])
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('list_jobs'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
