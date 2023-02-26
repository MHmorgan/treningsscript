Training Application
====================

* Store training data in a SQLite database in the server.

* Leverage sqlite for indexing, otherwise rely on pickling
  and storing the objects in BLOBs.

* Use blobopen() for efficiently interacting with the data?

* Schedule apps script to regularly fetch data from the
  server and put it into a google sheet for visualization
  and analytics.


    Endpoint                Methods  Rule
    ----------------------  -------  ------------------------------
    api.add_exercise        POST     /api/exercises
    api.add_exercise_entry  POST     /api/exercises/<exercise_name>
    api.add_session         POST     /api/sessions
    api.all_exercises       GET      /api/exercises
    api.all_sessions        GET      /api/sessions
    api.get_exercise        GET      /api/exercises/<exercise_name>
    static                  GET      /static/<path:filename>
    website.entry_page      GET      /exercise/<name>
    website.exercise_page   GET      /exercise
    website.index           GET      /
    website.session_page    GET      /session



Cheatsheet
----------

* `flask routes` - List all routes



Main Page
---------

Path: `/`

The main page of the application.

Functionality:

- Start new session
- Create a new exercise



Session Page
------------

Path: `/session`

The page for a training session. Need a `daytype` url
parameter when starting a new session.

Functionality:

- Add an exercise entry
- Create a new exercise



Entry Page
----------

Path: `/exercise/<name>`

The page for adding an exercise entry.



Exercise Page
-------------

Path: `/exercise`

The page for creating a new exercise.



API
---

`GET  /api/exercises` - List of exercise objects  
`POST /api/exercises` - Create a new exercise  
`GET  /api/exercises/<name>` - Get an exercise object  
`POST /api/exercises/<name>` - Add an exercise entry  

`GET  /api/sessions` - List of session objects
`POST /api/sessions` - Record a new session


### Exercise object

```
{
  "name": string
  "daytype": string
  "weighttype": string
  "entries": [
    {
      "date": date/string
      "reps": int
      "sets": int
      "weight": int?
      "onerepmax": int?
    }
  ]
}
```


### Session object

```
{
  "date": date/string
  "length": float
  "daytype": string
}
```
