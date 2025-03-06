* Bypass execution policy
    * Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

* Run virtual environment
    * myvenv/Scripts/activate

* You can test through (if using django):
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
        * points/ (GET, POST)
            * <int:point_id> (GET, PUT, PATCH, DELETE)
        * script/ (GET, POST, PUT, PATCH, DELETE)
        * links/ (GET, POST)
            * <int:link_id> (GET, PUT, PATCH, DELETE)
        * characters/ (GET, POST)
            * <int:character_id> (GET, PUT, PATCH, DELETE)
        * media/ (GET, POST, PUT, PATCH, DELETE)

User stories:
* Users should be able to create stories
* Users should be able to retrieve stories
* Users should be able to update stories
* Users should be able to delete stories

* Users should be able to schedule time on a calendar and track how much time was spent each day working on a story
* Users should be able to filter and sort for stories

Skill gaps:
* Querying a DB
* Manipulating dictionaries
* Manipulating API requests
* Constructing API request methods
* Tuple assignment
* ORM retrieving and inserting data