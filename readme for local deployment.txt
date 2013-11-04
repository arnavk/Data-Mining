1. Download the project directory off Github, available at https://github.com/radzinzki/Data-Mining
2. Install Python v2.7.x from http://www.python.org/download/
3. Install Django v1.5.x from https://www.djangoproject.com/download/
4. Open the shell interface and go to the relevant project directory. Once there, first enter the 'Visualizer' directory. This is where the project's source files can be found.
5. The database has to be initialized from the stored json file. To do so:
	5.1. Run the command "python manage.py shell"
	5.2. Once the shell is open run "from mapper.views import *" followed by "init()".
	5.3. Once the initialization is finished, exit the shell using the "exit()" command.
6. Locally deploy the application using the "python manage.py runserver" command
7. To access the application, go to a web browser (Firefox, Google Chrome and Safari are recommended) and go to "127.0.0.1:8000"