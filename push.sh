docker build --build-arg HTTP_PROXY=$http_proxy --build-arg HTTPS_PROXY=$http_proxy -t lallinger/extract-transform .
docker push lallinger/extract-transform
oc project extract-transform
oc delete -f service.yaml
oc create -f service.yaml