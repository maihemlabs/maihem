import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from maihem.api import MaihemHTTPClientSync
from maihem.clients import MaihemSync


m = MaihemHTTPClientSync(
    "http://localhost:8000",
    "10c972323b5a56914452fe58980b1502a64014af0bee0978f3202d7ce81a0b4cf4a3601d97d1344fac00e65a1d9371ab",
)

maihem_client = MaihemSync(
    "10c972323b5a56914452fe58980b1502a64014af0bee0978f3202d7ce81a0b4cf4a3601d97d1344fac00e65a1d9371ab"
)

print(m.whoami())

# target_agent = maihem_client.create_target_agent(
#    agent_identifier="agent-v-5",
#    name="Agent V5",
#    industry="Technology",
#    description="A helpful customer support agent",
#    role="customer_support",
# )

target_agent = maihem_client.get_target_agent("agent-v-5")

print(target_agent)
