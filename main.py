import os
import datetime


def logger_no_parameters(old_function):
    def __logger(*args, **kwargs):
        call_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        func_name = old_function.__name__
        result = old_function(*args, **kwargs)
        with open ('main.log', 'a') as log_file:
            log_file.write(call_time + '\n')
            log_file.write(func_name + '\n')
            log_file.write(str(args) + '\n')
            log_file.write(str(kwargs) + '\n')
            log_file.write(str(result) + '\n')
        return result
    return __logger

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            call_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result = old_function(*args, **kwargs)
            func_name = old_function.__name__
            with open(path, 'a') as log_file:
                log_file.write(call_time + '\n')
                log_file.write(func_name + '\n')
                log_file.write(str(args) + '\n')
                log_file.write(str(kwargs) + '\n')
                log_file.write(str(result) + '\n')
            return result

        return new_function

    return __logger

def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger_no_parameters
    def hello_world():
        return 'Hello World'

    @logger_no_parameters
    def summator(a, b=0):
        return a + b

    @logger_no_parameters
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'

def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'

def create_flat_list(source_list, result_list):
    for item in source_list:
        if isinstance(item, list):
            create_flat_list(item, result_list)
        else:
            result_list.append(item)
    return result_list

@logger('my_func.log')
def flat_generator(list_of_lists):
    flat_list = []
    result = create_flat_list(list_of_lists, flat_list)
    result_len = len(result)
    for cursor in range(result_len):
        yield result[cursor]

if __name__ == '__main__':
    test_2()
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]
    print(list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None])
