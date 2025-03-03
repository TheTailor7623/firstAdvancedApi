* Create a virtual environment
    * python -m venv myvenv
* Bypass execution policy
    * Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
* Run virtual environment
    * myvenv/Scripts/activate
* Create requirements.txt file
* Install requirements
    * pip install -r requirements.txt
* Create .gitignore file
* Build the .gitignore file
* Create local git repository
    * git init
* Create respository on github and connect it to local repository
    * git remote add origin git@github.com:TheTailor7623/AdvancedAPI.git
    * git branch -M main
    * git push -u origin main

You can test through (if using unittest):
if test structure is single file...
* python -m unittest tests.py
if folder structure...
* "python -m unittest discover -s tests" or for specific test "python -m unittest tests.test_app"

You can test through (if using django):
* python manage.py test
or
* python manage.py test app_name.tests.test_name.class_name.test_function_name

API ENDPOINTS:
api/
* dashboard/ (GET)
* user/
    * registration/ (POST)
    * token/ (GET, POST)
        * refresh/ (GET, POST)
* stories/ (GET)
    * create-new-story/ (POST)
    * <int:story_id>/ (GET, PUT, PATCH, DELETE)
        * incident/ (GET, POST, PUT, PATCH, DELETE)
        * people/ (GET, POST)
            * <int:person_id> (GET, PUT, PATCH, DELETE)
        * VAKS/ (GET, POST, PUT, PATCH, DELETE)
        * points/ (GET, POST, PUT, PATCH, DELETE)
        * script/ (GET, POST, PUT, PATCH, DELETE)
        * links/ (GET, POST, PUT, PATCH, DELETE)
        * media/ (GET, POST, PUT, PATCH, DELETE)
        * characters/ (GET, POST, PUT, PATCH, DELETE)

User stories:
* Users should be able to create stories
* Users should be able to edit stories
* Users should be able to search for stories
* Users should be able to delete stories
* Users should be able to schedule time on a calendar and track how much time was spent each day working on a story
* Users should be able to filter and sort for stories

Skill gaps:
* Querying a DB
* Manipulating dictionaries
* Manipulating API requests
* Constructing API request methods
* Tuple assignment
* ORM retriving and inserting data