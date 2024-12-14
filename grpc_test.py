import grpc
from hero_pb2_grpc import HeroesServiceStub
from hero_pb2 import HeroById  # Replace with your actual request message

def run():
    # Create a gRPC channel to the NestJS gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a client (stub) for the service
        stub = HeroesServiceStub(channel)

        # Create a request message (populate with necessary data)
        request = HeroById(id=1)  # Replace field_name and value

        # Call the service method and get the response
        response = stub.FindOne(request)  # Replace with the actual method name

        # Print or process the response
        print("Response received:", response)

if __name__ == "__main__":
    run()