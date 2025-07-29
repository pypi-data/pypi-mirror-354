
from universal_mcp.servers import SingleMCPServer
from universal_mcp.integrations import AgentRIntegration
from universal_mcp.stores import EnvironmentStore

from universal_mcp_sharepoint.app import SharepointApp

env_store = EnvironmentStore()
integration_instance = AgentRIntegration(name="sharepoint", store=env_store)
app_instance = SharepointApp(integration=integration_instance)

mcp = SingleMCPServer(
    app_instance=app_instance,
)

if __name__ == "__main__":
    mcp.run()


