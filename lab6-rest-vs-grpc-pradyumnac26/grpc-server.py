import grpc
from concurrent import futures
import time
import lab6_pb2
import lab6_pb2_grpc
from PIL import Image
import io
import base64
import numpy as np

class Lab6ServiceServicer(lab6_pb2_grpc.Lab6ServiceServicer):
    def Add(self, request, context):
        sum_result = request.a + request.b
        return lab6_pb2.addReply(sum=sum_result)

    def RawImage(self, request, context):
        img = Image.open(io.BytesIO(request.img))
        width, height = img.size
        return lab6_pb2.imageReply(width=width, height=height)

    def DotProduct(self, request, context):
        a = np.array(request.a)
        b = np.array(request.b)
        dot_product = float(np.dot(a, b))
        return lab6_pb2.dotProductReply(dotproduct=dot_product)

    def JsonImage(self, request, context):
        image_data = base64.b64decode(request.img)
        img = Image.open(io.BytesIO(image_data))
        width, height = img.size
        return lab6_pb2.imageReply(width=width, height=height)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(Lab6ServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on port 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
