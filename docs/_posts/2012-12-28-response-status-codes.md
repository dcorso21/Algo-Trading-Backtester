---
title: 'Getting Up and Running'

layout: null
---

### The Main File.

In order to use the backtester, You should first aquiant yourself with the __main.py__ file.

* `GET`, `PUT`, `DELETE` returns `200 OK` on success,
* `POST ` returns 201 on success,

When [retrieving stuff](#get-stuff) for example:

[batches](../../batches.html)

```Status: 200 OK```
```{
    {
        id: thing_1,
        name: 'My first thing'
    },
    {
        id: thing_2,
        name: 'My second thing'
    }
}```

### Error

Error responses are simply returning [standard HTTP error codes](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html) along with some additional information:

* The error code is sent back as a status header,
* The body includes an object describing both the code and message (for debugging and/or display purposes),

For a call with an invalid authentication token for example:

```Status: 401 Access denied```
```{
    code: 401,
    message: 'Access denied: invalid authentication token.'
}```