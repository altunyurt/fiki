# Fiki
A very simple, super fast wiki on Flask

## How it works 

* Create an .md file and place it under ```src/pages/[lang]/example.md```
* View it rendered as html at ```http://localhost:8081/[lang]/example.md```

## Serving on production

A supervisord controlled docker image and granian as wsgi server would provide a rock solid 5 mins setup.

Have a look at the sample Dockerfile
