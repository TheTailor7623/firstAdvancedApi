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

Knowledge gaps:
* Tuples
* Lists
* Dictionaries
* Iterating through tuples, lists and dictionaries
* for loops
* while loops
* Testing validation of data being stored in a model
* Different assertions that can be made
* List comprehensions and filtering data
* Data manipulation (string, integer etc... but mainly string)

REST FRAMEWORK NOTES:
* Creating a user model
    * AbstractBaseUser and PermissionsMixin are what the user model is based on
    * Create model field
    * set is_active, is_staff and is_superuser
    * Link to appropriate manager
* Create manager for user model
    * create_user function
    * create_superuser function