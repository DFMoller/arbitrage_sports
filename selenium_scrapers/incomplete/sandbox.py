

my_dict = {}

try:
    try:
        print(my_dict['test'])
    except KeyError as in_err:
        print("inner catch")
except KeyError as out_err:
    print("outer catch")