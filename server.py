import grpc
from concurrent import futures
import  psycopg2

import hello_pb2_grpc
import hello_pb2

class Greeter(hello_pb2_grpc.GreetingServicer):

    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="6010",
                database="grpc"
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

        except Exception as e:
            print(e)

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def add_user(self, login, password):
        self.cursor.execute(f"INSERT INTO public.user (login, psswrd) VALUES ('{login}', '{password}')")

    def get_user(self, login):
        self.cursor.execute(f"SELECT * FROM public.user WHERE login = '{login}'")
        return self.cursor.fetchone()

    def HelloEcho(self, request, context):
        user = self.get_user(request.login)
        if user != None:
            if request.password == user[2]:
                return hello_pb2.HelloResponse(message='Hello, %s!' % request.login)
            else:
                return hello_pb2.HelloResponse(message='Invalid!')
        else:
            return hello_pb2.HelloResponse(message='Registrate!')

    def RegistrateUser(self, request, context):
        self.add_user(request.login, request.password)
        return hello_pb2.HelloResponse(message="Registrate!")


port = '50051'
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
hello_pb2_grpc.add_GreetingServicer_to_server(Greeter(), server)
server.add_insecure_port('[::]:' + port)
server.start()
print("Server started, listening on " + port)
server.wait_for_termination()