from src.maihem.api import MaihemHTTPClientSync

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src/maihem"))

m = MaihemHTTPClientSync(
    "http://localhost:8000",
    "10c972323b5a56914452fe58980b1502a64014af0bee0978f3202d7ce81a0b4cf4a3601d97d1344fac00e65a1d9371ac",
)

print(m.whoami())
