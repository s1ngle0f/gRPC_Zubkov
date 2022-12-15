import psycopg2

# def test_AddUser(login, password):
#      return f"INSERT INTO user (login, psswrd) VALUES ({login}, {password})"
#
# print(test_AddUser("ku", "sdsd"))
#
# try:
#      connection = psycopg2.connect(
#           host="localhost",
#           user="postgres",
#           password="6010",
#           database="grpc",
#           port=5432
#      )
#      connection.autocommit = True
#
#      with connection.cursor() as cursor:
#           # cursor.execute(f"INSERT INTO public.user (login, psswrd) VALUES ('Mihail', '123');")
#           var = cursor.execute("SELECT * FROM public.user WHERE login = 'Mihail'")
#           print(cursor.fetchone() == None)
#
# except Exception as e:
#      print(e)
# finally:
#      if connection:
#           connection.close()


class TestDB():

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
        self.cursor.execute(f"INSERT INTO public.user (login, psswrd) VALUES ({login}, {password})")

    def get_user(self, login):
        self.cursor.execute(f"SELECT * FROM public.user WHERE login = '{login}'")
        return self.cursor.fetchone()

    def HelloEcho(self, request, context):
        user = self.get_user(request.login)
        if user != None:
            if request.password.equals(user[2]):
                return 'Hello, %s!' % request.login
            else:
                return 'Invalid!'
        else:
            return 'Registrate!'

    def RegistrateUser(self, request, context):
        self.add_user(request.login, request.password)
        return "Registrate!"

db = TestDB()
print(db.get_user("Mihail"))