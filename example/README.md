# example

## usage

- start server.py (maybe you need to change some settings)
- start client.py or client.js
    - `python client.py`
    - `node client.js` (need `npm install -g request`)

> you can try it in different languages.

## use it in production

built-in auth function is quite simple (not safe enough). if you want to use it as production, you 'd better re-implement function `auth` in handler.

```python
class SafeHandler(EventHandler):
    def auth(self, event: EventModel) -> bool:
        # custom auth ...
        return event.secret == 'SOME SECRET'
```

and change the default auth function:

```python
s = Server(handler=SafeHandler(manager))
```
