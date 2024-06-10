from google.cloud import iam

def translate_to_gcp_policy(unified_policy):
    gcp_policy = {
        "bindings": []
    }

    for resource in unified_policy['resources']:
        binding = {
            "role": f"roles/{unified_policy['actions'][0]}",  # Assuming a single action maps to a role
            "members": [resource['resourceId']]
        }
        if 'conditions' in unified_policy:
            binding["condition"] = unified_policy['conditions']
        gcp_policy["bindings"].append(binding)
    
    return gcp_policy

def deploy_gcp_policy(policy_name, gcp_policy, project_id):
    client = iam.Policy()
    
    policy_binding = {
        'policy': gcp_policy,
        'updateMask': {
            'paths': ['bindings']
        }
    }

    try:
        response = client.set_iam_policy(request={"resource": project_id, "policy": policy_binding})
        return response
    except Exception as e:
        print(f"Error deploying policy to GCP: {e}")
