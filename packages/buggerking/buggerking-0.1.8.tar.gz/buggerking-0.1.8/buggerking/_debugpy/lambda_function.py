import debugpy
import json
import random    

class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model
        self.__private_variable = "sexy guy"

    def start(self):
        print(f"{self.make} {self.model} is starting.")
        
class Engine:
    def __init__(self, cc, fuel):
        self.cc = cc
        self.fuel = fuel
        self.__private_variable = "sexy engine"
    

def calculate_sum(x, y):
    my_car2 = Car("test", "test2")

    def test_function():
        print("This is a test function.")

    if random.randint(0, 10) > 5:
        s = 1

    h = 4
    test_function()
    return x + y

def calculate_product(x, y):
    calculate_sum(x, y)
    return x * y

# global variables
car1 = Car(make="Hyundai", model="Sonata")
car2 = Car(make="Kia", model="K5")
car3 = Car(make="Tesla", model="Model S")
carlist = [car1, car2, car3]


def lambda_handler(event, context):
    print("🚀 Lambda 핸들러 시작!")

    # 재실행일 때
    if (event.get("queryStringParameters", {}) or {}).get("reinvoked") == "true":
        debugpy.connect(("165.194.27.213", 7789))
        # debugpy.wait_for_client(context=context, restart=((event.get("queryStringParameters", {}) or {}).get("reinvoked") == "true"))
        debugpy.wait_for_client(context=context, event=event)
        debugpy.breakpoint()
        print("Debugpy 재연결 완료!")

    # main Logic
    try:
        my_engine = Engine(1000, "diesel")
        my_car = Car("KIA", my_engine)
        
        testlist = [1, 2, 3, 4, 5]

        a = 11
        b = 22
        c = a - b
        ddd = 0
        cdk = calculate_product(11, 22)

        x = random.randint(0, 10)
        if x > 5:
            print("x is greater than 5")
            c = calculate_sum(a, b)

        d = [a, b]

        x = 1 / ddd   #  예외 발생!

        print("Lambda 핸들러 로직 완료!")
        print("Lambda 핸들러 로직 완료!")
        debugpy.breakpoint()
        print("Lambda 핸들러 로직 완료!")

    except Exception as e:
        debugpy.connect(("165.194.27.213", 7789))
        # debugpy.wait_for_client(exception=e, context=context, restart=((event.get("queryStringParameters", {}) or {}).get("reinvoked") == "true"))
        debugpy.wait_for_client(exception=e, context=context, event=event)
        debugpy.breakpoint()

        print("Exception occurred! Debug Mode starts...")
        # pass

    return {
        "statusCode": 200,
        "body": json.dumps("DAP JSON 전송 테스트 완료"),
    }