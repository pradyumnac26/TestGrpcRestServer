from __future__ import print_function
import grpc
import lab6_pb2
import lab6_pb2_grpc
import time
import base64
import random

def test_add(stub, reps):
    start = time.perf_counter()
    for _ in range(reps):
        response = stub.Add(lab6_pb2.addMsg(a=10, b=20))
    delta = ((time.perf_counter() - start) / reps) * 1000
    print(f"Add took {delta:.2f} ms per operation")

def test_dotproduct(stub, reps):
    start = time.perf_counter()
    for _ in range(reps):
        a = [random.random() for _ in range(100)]
        b = [random.random() for _ in range(100)]
        response = stub.DotProduct(lab6_pb2.dotProductMsg(a=a, b=b))
    delta = ((time.perf_counter() - start) / reps) * 1000
    print(f"DotProduct took {delta:.2f} ms per operation")

def test_rawimage(stub, reps):
    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
        img_data = f.read()
    start = time.perf_counter()
    for _ in range(reps):
        response = stub.RawImage(lab6_pb2.rawImageMsg(img=img_data))
    delta = ((time.perf_counter() - start) / reps) * 1000
    print(f"RawImage took {delta:.2f} ms per operation")

def test_jsonimage(stub, reps):
    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
        img_data = base64.b64encode(f.read()).decode('utf-8')
    start = time.perf_counter()
    for _ in range(reps):
        response = stub.JsonImage(lab6_pb2.jsonImageMsg(img=img_data))
    delta = ((time.perf_counter() - start) / reps) * 1000
    print(f"JsonImage took {delta:.2f} ms per operation")

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = lab6_pb2_grpc.Lab6ServiceStub(channel)
        print("Testing Add method:")
        test_add(stub, 1000)

        print("Testing DotProduct method:")
        test_dotproduct(stub, 1000)

        print("Testing RawImage method:")
        test_rawimage(stub, 1000)

        print("Testing JsonImage method:")
        test_jsonimage(stub, 1000)

if __name__ == '__main__':
    run()
