Training Application
====================

* Store training data in a SQLite database in the server.

* Leverage sqlite for indexing, otherwise rely on pickling
  and storing the objects in BLOBs.

* Use blobopen() for efficiently interacting with the data.

* Schedule apps script to regularly fetch data from the
  server and put it into a google sheet for visualization
  and analytics.



ELM Inspiration
---------------

* https://github.com/elm/package.elm-lang.org
* https://github.com/rtfeldman/elm-spa-example



API
---

`/` - Index page
`/js/<path>` - Javascript resources

`GET  /api/exercises` - List of exercise objects
`POST /api/exercises` - Create a new exercise
`GET  /api/exercises/<name>` - Get an exercise object
`POST /api/exercises/<name>` - Add an exercise entry

`GET  /api/warmups` - List of warmup objects
`POST /api/warmups` - Create a new warmup
`GET  /api/warmups/<name>` - Get a warmup object
`POST /api/warmups/<name>` - Add a warmup entry

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
      "reps": [int]
      "weight": int?
      "onerepmax": int?
    }
  ]
}
```


### Warmup object

```
{
  "name": string
  "entries": [
    {
      "date": date/string
      "intervals": [int]
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
