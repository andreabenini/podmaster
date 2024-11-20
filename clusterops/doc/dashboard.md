# Dashboard installation

- `kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml`
```sh
namespace/kubernetes-dashboard created
serviceaccount/kubernetes-dashboard created
service/kubernetes-dashboard created
secret/kubernetes-dashboard-certs created
secret/kubernetes-dashboard-csrf created
secret/kubernetes-dashboard-key-holder created
configmap/kubernetes-dashboard-settings created
role.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrole.rbac.authorization.k8s.io/kubernetes-dashboard created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
deployment.apps/kubernetes-dashboard created
service/dashboard-metrics-scraper created
deployment.apps/dashboard-metrics-scraper created
```
- Proxy access
```sh
# Access URL
echo http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
# Start proxy
kubectl proxy
# Less picky on user-agent...
kubectl proxy --accept-hosts='^.*$'
# Broad open on LAN, all interfaces
# kubectl proxy --address='0.0.0.0' --port=8001 --accept-hosts='^.*$'
```
- Accessing dashboard from browsers outside local machine  
_Using NodePort (for access from outside your machine)_, edit the Dashboard service to use NodePort:
```sh
kubectl -n kubernetes-dashboard edit service kubernetes-dashboard
```
    - Change type: ClusterIP to type: NodePort.
    - Save the file. Kubernetes will assign a port number
    - Find the assigned port:
    ```sh
    kubectl -n kubernetes-dashboard get service kubernetes-dashboard
    ```
- Dashboard admin user:
Create `dashboard.yaml`
```yaml
#
# Dashboard configuration, apply recommended.yaml (github kubernetes/dashboard) BEFORE, this file later
#

# Creating a service account [admin-user]
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard

---
# Bind the service account to the cluster-admin ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: admin-user
    namespace: kubernetes-dashboard

---
# Assign secret token to [admin-user]
apiVersion: v1
kind: Secret
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
  annotations:
    kubernetes.io/service-account.name: "admin-user"
type: kubernetes.io/service-account-token
```
and apply changes:
```sh
kubectl apply -f dashboard.yaml
# serviceaccount/admin-user created
# clusterrolebinding.rbac.authorization.k8s.io/admin-user created
# secret/admin-user created
```
- Get secret token
```sh
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d
# kubectl -n kubernetes-dashboard get secret $(kubectl -n kubernetes-dashboard get sa/admin-user -o jsonpath="{.secrets[0].name}") -o go-template="{{.data.token | base64decode}}"
```
- If you are experiencing token issues there might be a problem with it, try to regenerate a
new one and use that instead to fix 401 Unauthorized Errors.
```sh
kubectl -n kubernetes-dashboard create token admin-user
```


# Dashboard uninstallation
```sh
kubectl delete -f dashboard.yaml
kubectl delete -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```
