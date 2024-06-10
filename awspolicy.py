import boto3
import json

def translate_to_aws_policy(unified_policy):
    aws_policy = {
        "Version": "2012-10-17",
        "Statement": []
    }

    for resource in unified_policy['resources']:
        statement = {
            "Effect": unified_policy['effect'].upper(),
            "Action": unified_policy['actions'],
            "Resource": resource['resourceId']
        }
        if 'conditions' in unified_policy:
            statement["Condition"] = unified_policy['conditions']
        aws_policy["Statement"].append(statement)
    
    return aws_policy

def deploy_aws_policy(policy_name, aws_policy):
    client = boto3.client('iam')

    try:
        response = client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(aws_policy)
        )
        return response
    except client.exceptions.EntityAlreadyExistsException:
        response = client.get_policy(PolicyArn=f"arn:aws:iam::aws:policy/{policy_name}")
        version = client.create_policy_version(
            PolicyArn=response['Policy']['Arn'],
            PolicyDocument=json.dumps(aws_policy),
            SetAsDefault=True
        )
        return version
    except Exception as e:
        print(f"Error deploying policy to AWS: {e}")
