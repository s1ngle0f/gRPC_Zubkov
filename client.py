import hello_pb2
import hello_pb2_grpc
import grpc

with grpc.insecure_channel('localhost:50051') as channel:
    stub = hello_pb2_grpc.GreetingStub(channel)
    # response = stub.HelloEcho(hello_pb2.HelloRequest(login='Mihail', password="123"))
    # response = stub.RegistrateUser(hello_pb2.Registrate(login='Pavel', password="321"))
    # response = stub.HelloEcho(hello_pb2.HelloRequest(login='Pavel', password="321"))
    print("Greeter client received: " + response.message)