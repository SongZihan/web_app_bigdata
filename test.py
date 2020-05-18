def decorator(func):
    def wrapper(*args,**kw):
        # *args可以保证使用装饰器的函数需要的参数（一个或多个）被正确传递
        # **kw表示接收任意数量的关键字参数，它将以字典的形式被传入
        print("这是装饰器附加的语句~~")
        func(*args,**kw)
        print("这是目标函数结束后被执行的语句~~~")

    return wrapper


@decorator
def cat(name,**kw):
    print("这是使用了装饰器函数打印的语句~~",name)
    print(kw)


cat("666",a=2,b=3)
