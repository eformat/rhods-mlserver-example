# RHODS/ODH - Custom Serving Runtimes

Create a custom mlserver for sklearn model using MLFlow and RHODS.

1. Deploy RHODS Managed Operator

2. MLFLow is also deployed see for howto examples:
    - https://eformat.github.io/rainforest-docs/#/4-aiml-demos/2-mlflow
    - https://ai-on-openshift.io/tools-and-applications/mlflow/mlflow/

3. Open `mlflow.ipynb` - train a MLFLow model - pushes pkl model to Minio/S3

4. Create data science project in RHODS called `demo` - which creates a namespace called demo.

5. Create S3 secret for minio with creds under demo RHODS project

6. Create a new `ServingRuntime` in the `demo` namespace. See [here](https://github.com/red-hat-data-services/odh-model-controller/blob/main/config/manager/servingruntimes_config.yaml) for the source code.

    ```bash
    oc -n demo apply -f serving-runtime-mlserver.yaml
    ```

    Can see that created here:

    ```bash
    $ oc get servingruntimes.serving.kserve.io -A
    NAMESPACE   NAME           DISABLED   MODELTYPE   CONTAINERS   AGE
    demo        mlserver-0.x              sklearn     mlserver     20h
    ```

7. Create an `InferenceService` pointing to the runtime and S3 storage location and key for the pkl model:

    ```bash
    oc apply -n demo -f- <<EOF
    apiVersion: serving.kserve.io/v1beta1
    kind: InferenceService
    metadata:
    annotations:
        serving.kserve.io/deploymentMode: ModelMesh
    name: linear-regression
    spec:
    predictor:
        model:
        modelFormat:
            name: sklearn
        runtime: mlserver-0.x
        storage:
            key: aws-connection-minio
            path: 1/b0a1acea61304c3cbebf96a95d98e15b/artifacts/model/model.pkl
    EOF
    ```

8. Check isvc status:

    ```bash
    oc -n demo get isvc
    NAME                URL                                  READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION   AGE
    linear-regression   grpc://modelmesh-serving.demo:8033   True   
    ```

8. Demo GRPC call for the inference endpoint.

    Port forward GRPC:

    ```bash
    oc -n demo port-forward svc/modelmesh-serving 8033:8033
    ```

9. Call inference endpoint

    Install deps

    ```bash
    pip3.11 install grpcio mlserver --user
    ```

    Make request

    ```bash
    python3.11 grpc-request.py --modelname testmodel-v1

    model_name: "testmodel-v1__isvc-565bc5d323"
    outputs {
      name: "predict"
      datatype: "FP64"
      shape: 1
      shape: 1
      contents {
        fp64_contents: 4.9175517014573042
      }
    }
    ```

## Useful Links:

- [How to Create a Custom Serving Runtime in KServe ModelMesh to Serve Your Models](https://www.youtube.com/watch?v=VLXjIGRb3yU)
- [ODH ModelMesh Runtimes](https://github.com/opendatahub-io/odh-manifests/blob/master/model-mesh/runtimes/mlserver-0.x.yaml)
