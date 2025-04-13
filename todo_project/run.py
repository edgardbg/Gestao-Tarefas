import coverage
from todo_project import app

cov = coverage.Coverage()
cov.start()

if __name__ == '__main__':
    app.run(debug=True)

cov.stop()
cov.save()
