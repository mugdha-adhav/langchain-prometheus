sudo chown vscode /home/vscode/.local
pip install --user -r requirements.txt
kind create cluster
mkdir -p ~/.kube
kind get kubeconfig > ~/.kube/config
helm repo add prometheus-community "https://prometheus-community.github.io/helm-charts"
helm repo update
helm upgrade --install prometheus "prometheus-community/kube-prometheus-stack"
