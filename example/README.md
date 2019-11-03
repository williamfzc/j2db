# example

## usage

- start server.py (maybe you need to change some settings)
- start client.py or client.js
    - `python client.py`
    - `node client.js` (need `npm install -g request`)

> you can try it in different languages.

## customization

in production environment, customization is necessary and important for extending functions. And it should be simple enough:

```python
from j2db.handler import EventHandler
from j2db.models import EventModel

class NewEventHandler(EventHandler):
    def before_auth(self, e: EventModel) -> EventModel:
        # finish your customization
        e.content += "abcde"
        # and return it
        return e
    
    # there are many kinds of hooks for different usages, which start with `before` or `after`.
    # you can find them in EventHandlerHookMixin
```

and bind (overwrite) this handler to server:

```python
manager.connect()
manager.add_model(SomeModel)
new_handler = NewEventHandler(manager)

s = Server()
s.init_db(manager, create_tables=True)
s.init_handler(new_handler)
s.start()
```

they should work as expect.
