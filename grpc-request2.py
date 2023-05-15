import requests
import json
import grpc
import mlserver.grpc.converters as converters
import mlserver.grpc.dataplane_pb2_grpc as dataplane
import mlserver.types as types
from mlserver.codecs import NumpyRequestCodec
from mlserver.types import InferenceRequest
from mlserver.codecs import NumpyCodec
import numpy as np
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=1)

model_name = "testmodel"

input = np.array([[-0.07672111],
       [ 0.39475099],
       [ 0.46627568],
       [ 0.50694887],
       [ 0.52395762],
       [ 0.57207839],
       [ 0.57725378],
       [ 0.62670804],
       [ 0.67854757],
       [ 0.68305336],
       [ 0.6940444 ],
       [ 0.91215952],
       [ 0.9626345 ],
       [ 0.97963183],
       [ 0.98507583],
       [ 1.13533111],
       [ 1.25815571],
       [ 1.44147949],
       [ 1.58860785],
       [ 1.6400072 ],
       [ 1.65238516],
       [ 1.76523642],
       [ 1.89656553],
       [ 1.93420997],
       [ 1.93891226],
       [ 1.98109978],
       [ 2.04784774],
       [ 2.07619016],
       [ 2.10270157],
       [ 2.16312675],
       [ 2.19482653],
       [ 2.20921272],
       [ 2.23312708],
       [ 2.27040225],
       [ 2.36980233],
       [ 2.39157523],
       [ 2.43197649],
       [ 2.52413397],
       [ 2.77718162],
       [ 2.80035669],
       [ 2.86999865],
       [ 3.02353918],
       [ 3.04990916],
       [ 3.08512384],
       [ 3.13484271],
       [ 3.36589547],
       [ 3.38317128],
       [ 3.39237407],
       [ 3.44389562],
       [ 3.53105366],
       [ 3.66378642],
       [ 3.69475393],
       [ 3.773067  ],
       [ 3.9197644 ],
       [ 4.09042033],
       [ 4.09314036],
       [ 4.10827469],
       [ 4.2299105 ],
       [ 4.31690152],
       [ 4.46720112],
       [ 4.60355042],
       [ 4.65839746],
       [ 4.77271212],
       [ 4.78369527],
       [ 4.82063353],
       [ 4.84917435],
       [ 4.86432986],
       [ 4.9118197 ],
       [ 4.9446405 ],
       [ 5.0576086 ],
       [ 5.15655743],
       [ 5.17645451],
       [ 5.25579646],
       [ 5.29347125],
       [ 5.35531806],
       [ 5.36515089],
       [ 5.40445218],
       [ 5.45184316],
       [ 5.47057997],
       [ 5.49353902],
       [ 5.49882552],
       [ 5.6361293 ],
       [ 5.68069441],
       [ 5.95698266],
       [ 6.00617641],
       [ 6.02072026],
       [ 6.17960229],
       [ 6.20133823],
       [ 6.24555734],
       [ 6.28755616],
       [ 6.38644596],
       [ 6.40546154],
       [ 6.53519148],
       [ 6.59724452],
       [ 6.71868897],
       [ 6.89731644],
       [ 6.94737908],
       [ 6.96343178],
       [ 6.9896169 ],
       [ 6.99735752]])

# input_bytes = json.dumps(input).encode("UTF-8")

# inference_request = types.InferenceRequest(
#     inputs=[
#         types.RequestInput(
#             name="double_input",
#             shape=[len(input_bytes)],
#             datatype="BYTES",
#             data=[input_bytes],
#             parameters=types.Parameters(content_type="str"),
#         )
#     ]
# )

inference_request = InferenceRequest(
  inputs=[
    NumpyCodec.encode_input("double_input", input)
  ]
)

#inference_request = NumpyRequestCodec.encode_request(input)

inference_request_g = converters.ModelInferRequestConverter.from_types(
    inference_request,
    model_name=model_name,
    model_version=None,
)

#pp.pprint(inference_request_g)

grpc_channel = grpc.insecure_channel("localhost:8033")
grpc_stub = dataplane.GRPCInferenceServiceStub(grpc_channel)

response = grpc_stub.ModelInfer(inference_request_g)
pp.pprint(response)