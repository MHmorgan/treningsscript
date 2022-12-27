apps script project
===================


[Apps Script](https://developers.google.com/apps-script)
-----------

[Reference](https://developers.google.com/apps-script/reference)



[Clasp](https://developers.google.com/apps-script/guides/clasp)
-----

[GitHub repo](https://github.com/google/clasp)

**Setup**

```shell
$ npm install @google/clasp -g
$ clasp login
```

Create .clasp.json config file with the content:

```json
{"scriptId":"<script-id>","rootDir":"<repo-dir-abspath>"}
```

**Continuously pushing**

```shell
clasp push -w
```
