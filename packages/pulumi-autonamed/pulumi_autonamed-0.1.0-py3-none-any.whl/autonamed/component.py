import pulumi
import pulumi_azure_native as azure_native
from pulumi import ComponentResource, ResourceOptions, InvokeOptions


class AutoNamedArgs:
    def __init__(self, namespace: str, environment: str, region: str):
        self.namespace = namespace
        self.environment = environment
        self.region = region


class AutoNamed(ComponentResource):
    """
    Builds names that start with the subscription ID of *whatever*
    azure-native provider Pulumi wires into this component.
    """
    def __init__(self, name: str, args: AutoNamedArgs,
                 opts: ResourceOptions | None = None):
        super().__init__("autonamed:index:AutoNamed", name, {}, opts)

        az = self.get_provider("azure-native")
        inv = InvokeOptions(provider=az) if az else None
        sub_id = azure_native.authorization.get_client_config(
            opts=inv
        ).subscription_id                          # Output[str]

        rg_name = sub_id.apply(
            lambda sid: f"{args.namespace}-{sid[:8]}-{args.environment}-{args.region}"
        )

        self.resource_group = azure_native.resources.ResourceGroup(
            rg_name,
            resource_group_name=rg_name,
            opts=ResourceOptions(parent=self, provider=az),
        )

        self.register_outputs({"name": rg_name})
