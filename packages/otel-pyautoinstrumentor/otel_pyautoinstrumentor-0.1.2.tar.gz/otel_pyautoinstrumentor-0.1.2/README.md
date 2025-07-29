# OpenTelemetry Python Autoinstrumentation


## Problem we are trying to solve

When we want to instrument our python code, the opentelemetry python library provides a convenient way to do so.

In the repo [opentelemetry-python-contrib](https://github.com/open-telemetry/opentelemetry-python-contrib), there are numerous autoinstrumentation libraries for different frameworks and libraries.

Examples are:
- [opentelemetry-instrumentation-aiohttp-client](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-aiohttp-client)
- [opentelemetry-instrumentation-openai](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-openai)
- [opentelemetry-instrumentation-requests](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-requests)
- [opentelemetry-instrumentation-sqlalchemy](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-sqlalchemy)
- [opentelemetry-instrumentation-fastapi](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-fastapi)
- a lot of other libraries ...

But it would be a good thing to be able to instrument any python code without having to use a specific library.
For example it would be convenient to create a span for any function call in a python script. In this span, we could have the function name, the arguments and the return value.

## Solution

### The @tracer.start_as_current_span decorator

The `opentelemetry.tracer` module provides a `start_as_current_span` decorator that can be used to create a span for any function call.

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span
def my_function(arg1, arg2):
```

This is the standard way to create a span for a function call.

### Automatize the creation of the span

One way to automate the creation of the span would be to use the [sys.monitoring](https://docs.python.org/3/library/sys.monitoring.html) module.
Using this module, we can register a callback that will be called when a function call is made, and that would create a span for the function call.
We can also register a callback that will be called when a function is returned, and that would end the span.

When implementing these callbacks, we can also get the args and the return value of the function call and add them to the span.

See [examples/basic_example.py](examples/basic_example.py) for an example.
