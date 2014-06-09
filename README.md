##Chat with [Gevent WebSocket](https://bitbucket.org/Jeffrey/gevent-websocket) and [wheezy.web](https://bitbucket.org/akorn/wheezy.web)

This code serve as an example for using WebSockets with wheezy.web. 
What would be prefect than a chat application?

![](https://lh5.googleusercontent.com/-vYLqFjJtd2M/U5YABun7wAI/AAAAAAAAKNk/tviQLHd3qq0/w900-no/screenshot.png)

There are multiple ways of implementing websockets. 
But, it's something like chat is too complex.
So, I have added another small example `test.py` to understand in a better way.

##Installation:

1. Install the requirements in `requirements.pip` file with pip on [virtualenv/virtualwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
2. Run the application. That's all. :D

## Test

Test is a simple example on using `request.environ['wsgi.websocket']` for Websockets.

After installing the requirements. Use `python test.py` to run the server. Which runs on port `5000`

## Chat

Chat is a complex application. It's more WebSocket centric than wheezy.web, that is because `geventwebsocket` provide `WebSocketApplication` and `WebSocketServer` which makes your life easy when you are working with websockets.

After installing the requirements. Use `python chat.py` to run the server. Which runs on `http://localhost:8000/`

##Front-end

The front-end is written in jQuery and Basic HTML. So, it will be easy to understand for most audience.
If you want you can fork it, make versions with any MVC framework.


##Why did we do this and not create a Middleware instead?
> An application server will supply you an environ variable that will corresponds to a web socket so you use it from there (e.g. gevent web sockets). Thus anything built on top of this is considered over engineering. [**- Andriy Kornatskyy**](http://mindref.blogspot.in/)


##Warnings

Don't worry about this warning, they are not needed at development:

    UserWarning: Ticket: digestmod is not specified, fallback to sha1
    options['ticket'] = Ticket()
    UserWarning: Ticket: cypher not available
    options['ticket'] = Ticket()
