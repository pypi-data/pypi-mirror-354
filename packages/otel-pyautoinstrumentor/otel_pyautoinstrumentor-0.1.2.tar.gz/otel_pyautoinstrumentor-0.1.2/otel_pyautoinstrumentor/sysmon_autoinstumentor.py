import inspect
import logging
import sys

from opentelemetry.trace import Tracer

class SysmonAutoInstrumentor:
    def __init__(self, tracer: Tracer):
        self.tool_id = sys.monitoring.PROFILER_ID
        self.tracer = tracer
        
        # We store the spans created in this dictionnary so we can end them when the function returns
        self.spans = {}
        
    def _handle_call(self, code, instruction_offset):
        """This function is a callback called when a function call is made.
        
        [Python official documentation](https://docs.python.org/3/library/sys.monitoring.html#callback-function-arguments)        
        """
        file_name = code.co_filename
        if not self._is_user_code(file_name):
            # The code is not user code, we don't want to instrument it
            return
        
        frame = sys._getframe(1)
        function_name = frame.f_code.co_name
        
        ctx_mgr = self.tracer.start_as_current_span(
            name=function_name,
            attributes={
                "file_name": file_name,
                "line_number": frame.f_lineno,
                "function_name": function_name,
            }
        )
        
        span = ctx_mgr.__enter__()
        
        # add input as attributes
        try:
            args = inspect.getargvalues(frame)
            for arg_name, arg_value in args.locals.items():
                span.set_attribute(arg_name, arg_value)
        except Exception as e:
            logging.error(f"Error getting arguments for {function_name}: {e}")
        
        self.spans[id(frame)] = (ctx_mgr, span)
        
    def _handle_return(self, code, instruction_offset, retval):
        """This function is a callback called when a function returns.
        
        [Python official documentation](https://docs.python.org/3/library/sys.monitoring.html#callback-function-arguments)
        """
        frame = sys._getframe(1)
        key = id(frame)
        if key in self.spans:
            ctx_mgr, span = self.spans.pop(key)
            try: 
                span.set_attribute("return_value", str(retval))
                ctx_mgr.__exit__(None, None, None)
            except Exception as e:
                logging.error(f"Error setting return value for {frame.f_code.co_name}: {e}")
                
    def instrument(self):
        """Instrument the python interpreter to trace all function calls."""
        if not sys.monitoring.get_tool(self.tool_id):
            sys.monitoring.use_tool_id(self.tool_id, "python-autoinstrumentor")
        else:
            # if the tool already assigned is not ours, we need to raise an error
            if sys.monitoring.get_tool(self.tool_id) != "python-autoinstrumentor":
                raise RuntimeError(
                    "A tool with the id python-autoinstrumentor is already assigned, please stop it before starting a new tracing"
                )
        sys.monitoring.register_callback(self.tool_id, sys.monitoring.events.PY_START, self._handle_call)
        sys.monitoring.register_callback(self.tool_id, sys.monitoring.events.PY_RETURN, self._handle_return)
        sys.monitoring.set_events(self.tool_id, sys.monitoring.events.PY_START | sys.monitoring.events.PY_RETURN)
        
    def _is_user_code(self, filename: str) -> bool:
        """Check if a file belongs to an installed module rather than user code.
        This is used to determine if we want to trace a line or not"""

        if (
            ".local" in filename
            or "/usr/lib" in filename
            or "/usr/local/lib" in filename
            or "site-packages" in filename
            or "dist-packages" in filename
            or "/lib/python3.12/" in filename
            or "frozen" in filename
            or filename.startswith("<")
        ):
            return False
        return True