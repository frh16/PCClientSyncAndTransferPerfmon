import time

def get_time(format='%Y%m%d%H%M%S'):
    return time.strftime(format)








if __name__ == '__main__':
    print(get_time())