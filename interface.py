from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# In-memory policy storage for demonstration
policies = []

@app.route('/')
def home():
    return "Unified Security Policy Framework"

@app.route('/policies', methods=['GET'])
def get_policies():
    return jsonify(policies)

@app.route('/policies', methods=['POST'])
def add_policy():
    policy = request.json
    policies.append(policy)
    return jsonify({"message": "Policy added", "policy": policy}), 201

@app.route('/deploy/<provider>', methods=['POST'])
def deploy_policy(provider):
    policy_id = request.json['policyId']
    policy = next((p for p in policies if p['policyId'] == policy_id), None)
    
    if not policy:
        return jsonify({"message": "Policy not found"}), 404

    if provider == "aws":
        aws_policy = translate_to_aws_policy(policy)
        response = deploy_aws_policy(policy['policyName'], aws_policy)
    elif provider == "azure":
        azure_policy = translate_to_azure_policy(policy)
        response = deploy_azure_policy(policy['policyName'], azure_policy)
    elif provider == "gcp":
        gcp_policy = translate_to_gcp_policy(policy)
        response = deploy_gcp_policy(policy['policyName'], gcp_policy, "<project_id>")
    else:
        return jsonify({"message": "Invalid provider"}), 400

    return jsonify({"message": "Policy deployed", "response": response})

if __name__ == '__main__':
    app.run(debug=True)
