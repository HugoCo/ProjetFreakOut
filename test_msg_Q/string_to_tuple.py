def my_method(parameter_A, parameter_B=None):
    if isinstance(parameter_B, int):
        print(parameter_A * parameter_B)
    else:
        print(parameter_A)


my_method(4)
