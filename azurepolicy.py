from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient

def translate_to_azure_policy(unified_policy):
    azure_policy = {
        "if": {
            "field": "type",
            "equals": unified_policy['resources'][0]['resourceType']
        },
        "then": {
            "effect": unified_policy['effect']
        }
    }

    for action in unified_policy['actions']:
        azure_policy['if']['equals'] = action
    
    if 'conditions' in unified_policy:
        azure_policy['if']['conditions'] = unified_policy['conditions']
    
    return azure_policy

def deploy_azure_policy(policy_name, azure_policy):
    credentials = DefaultAzureCredential()
    client = AuthorizationManagementClient(credentials, "<subscription_id>")

    policy = {
        "properties": {
            "displayName": policy_name,
            "policyRule": azure_policy,
            "description": "A policy example for demonstration"
        }
    }

    try:
        response = client.policy_definitions.create_or_update(
            policy_name,
            policy
        )
        return response
    except Exception as e:
        print(f"Error deploying policy to Azure: {e}")
