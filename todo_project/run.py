import coverage
from todo_project import app

cov = coverage.Coverage()
cov.start()

cov.stop()
cov.save()

if __name__ == '__main__':
    app.run(debug=True)
