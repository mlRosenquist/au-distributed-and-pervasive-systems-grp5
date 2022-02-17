# Getting Started

## Prequisites
- Docker
- Minikube
- Kubectl
- Python3

## Steps to run
- Navigate to src folder with Dockerfile
- Build docker image: docker build -t node .
- Provision ressources in minikube: kubectl apply -f node-deployments-services.yml
- See dashboard: minikube dashboard
- Give services external endpoints: minikube tunnel
- Under services in the dashboard you can now see the endpoints. 