import requests
import json
import grpc
import mlserver.grpc.converters as converters
import mlserver.grpc.dataplane_pb2_grpc as dataplane
import mlserver.types as types
from mlserver.codecs import NumpyRequestCodec
import numpy as np

model_name = "linear-regression"
input = np.array([1.23])
input = input.reshape(1,-1)
#input_bytes = json.dumps(input).encode("UTF-8")

inference_request = NumpyRequestCodec.encode_request(input)

inference_request_g = converters.ModelInferRequestConverter.from_types(
    inference_request,
    model_name=model_name,
    model_version=None
)

grpc_channel = grpc.insecure_channel("localhost:8033")
grpc_stub = dataplane.GRPCInferenceServiceStub(grpc_channel)

response = grpc_stub.ModelInfer(inference_request_g)
print(response)