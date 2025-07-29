
from universal_mcp.servers import SingleMCPServer
from universal_mcp.integrations import AgentRIntegration
from universal_mcp.stores import EnvironmentStore

from universal_mcp_aws_s3.app import AwsS3App

env_store = EnvironmentStore()
integration_instance = AgentRIntegration(name="aws-s3", store=env_store)
app_instance = AwsS3App(integration=integration_instance)

mcp = SingleMCPServer(
    app_instance=app_instance,
)

if __name__ == "__main__":
    mcp.run()


