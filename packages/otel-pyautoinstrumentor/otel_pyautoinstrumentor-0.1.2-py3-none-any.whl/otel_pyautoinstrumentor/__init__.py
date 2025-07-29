import logging
import sys

from .sysmon_autoinstumentor import SysmonAutoInstrumentor

__all__ = ["SysmonAutoInstrumentor"]

# Import the sys.monitoring-based tracer if Python 3.12+ is available
if not hasattr(sys, "monitoring"):
    logging.warning("Python 3.12+ is required to use the sys.monitoring-based tracer.")


