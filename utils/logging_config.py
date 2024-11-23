import logging
import sys
import structlog
from pythonjsonlogger import jsonlogger

# Configuração do logger padrão do Python
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    stream=sys.stdout,
)

# Configuração do handler de log para JSON
class JsonFormatter(jsonlogger.JsonFormatter):
    def parse(self):
        return [
            "asctime",
            "levelname",
            "message",
            "name",
            "filename",
            "lineno",
            "funcName",
        ]

# Configuração do logger estruturado
logging.getLogger().handlers = []
handler = logging.StreamHandler()
formatter = JsonFormatter()
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)

# Configuração do structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),  # Adiciona timestamp
        structlog.processors.JSONRenderer()           # Renderiza logs em JSON
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Criação de um logger estruturado
logger = structlog.get_logger("estimate-svc")
