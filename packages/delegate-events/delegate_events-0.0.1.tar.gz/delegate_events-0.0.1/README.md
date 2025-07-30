[![Test](https://github.com/apmadsen/delegate-events/actions/workflows/python-test.yml/badge.svg)](https://github.com/apmadsen/delegate-events/actions/workflows/python-test.yml)
[![Coverage](https://github.com/apmadsen/delegate-events/actions/workflows/python-test-coverage.yml/badge.svg)](https://github.com/apmadsen/delegate-events/actions/workflows/python-test-coverage.yml)
[![Stable Version](https://img.shields.io/pypi/v/delegate-events?label=stable&sort=semver&color=blue)](https://github.com/apmadsen/delegate-events/releases)
![Pre-release Version](https://img.shields.io/github/v/release/apmadsen/delegate-events?label=pre-release&include_prereleases&sort=semver&color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/delegate-events)
[![PyPI Downloads](https://static.pepy.tech/badge/delegate-events/week)](https://pepy.tech/projects/delegate-events)

# delegate-events: Python implementation of the Event Pattern.

delegate-events provides a basic implementation of the well-known Event or Pub/Sub Pattern, and is built on top of the `delegate-pattern` package which handles the delegation part.

## Example

```python
from delegate.pattern import delegate
from delegate.events import Channel, Event

class OnSomethingEvent(Event):
    def __init__(self, what: str, why: str):
        self.what = what
        self.why = why

    def __str__(self):
        return f"{self.what} happened because of {self.why}"

class Class1:
    on_something = delegate(Channel[OnSomethingEvent])

inst = Class1()
msg_queue: list[Event] = []

def fn(publisher, event: OnSomethingEvent):
    msg_queue.append(event)

inst.on_something.subscribe(fn)
inst.on_something.fire(OnSomethingEvent("Something", "some other thing"))

str(msg_queue[0]) # => "Something happened because of some other thing"
```

## Full documentation

[Go to documentation](https://github.com/apmadsen/delegate-pattern/blob/main/docs/documentation.md)
