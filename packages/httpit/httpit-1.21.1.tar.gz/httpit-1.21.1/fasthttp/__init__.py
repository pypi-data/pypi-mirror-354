"""
httpit - Ultra-fast lightweight HTTP server

A Python wrapper around the high-performance webfsd C web server.
Developed and maintained by RODMENA LIMITED (https://rodmena.co.uk)
"""

from fasthttp.server import HTTPServer, WebfsdError

__version__ = '1.21.1'
__author__ = 'RODMENA LIMITED'
__email__ = 'info@rodmena.co.uk'
__url__ = 'https://github.com/rodmena-limited/fasthttp'
__all__ = ['HTTPServer', 'WebfsdError']