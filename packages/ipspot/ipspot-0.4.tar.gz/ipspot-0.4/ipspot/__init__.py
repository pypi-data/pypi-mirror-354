# -*- coding: utf-8 -*-
"""ipspot modules."""
from .params import IPSPOT_VERSION, IPv4API
from .ipv4 import get_private_ipv4, get_public_ipv4, is_ipv4
from .utils import is_loopback
__version__ = IPSPOT_VERSION
