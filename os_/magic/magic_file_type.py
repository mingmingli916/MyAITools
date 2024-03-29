import sys
import os_
import glob

magic_path = '/home/hack/PycharmProjects/packages/chyson/os/magic/magic_file_type.py'
# this deals with the linux and windows platform
if sys.platform.startswith("win"):
    def get_files(names):
        for name in names:
            if os_.path.isfile(name):
                yield name
            else:
                for file in glob.iglob(name):
                    if not os_.path.isfile(file):
                        continue
                    yield file
else:
    def get_files(names):
        return (file for file in names if os_.path.isfile(file))


def load_modules():
    """
    Dynamically load modules in the specified directory python files and
    has magic keyword in the python file.
    :return:
    """
    modules = []
    # for name in os.listdir(os.path.dirname(__file__) or '.'):
    for name in os_.listdir(os_.path.dirname(magic_path)):
        if name.endswith('.py') and 'magic' in name.lower():
            filename = name
            name = os_.path.splitext(name)[0]  # remove extension
            if name.isidentifier() and name not in sys.modules:  # isidentifier: if a string is a valid identifier
                fh = None
                try:
                    fh = open(os_.path.join(os_.path.dirname(magic_path), filename), 'r', encoding='utf8')
                    code = fh.read()
                    # When we call type() it returns the type object
                    # of the object it is given. So if we called type(1) we would get int back. If we
                    # print the type object we just get something human readable like “int”, but if
                    # we call the type object as a function, we get an object of that type back. For
                    # example, we can get the integer 5 in variable x by writing x = 5 , or x = int(5) ,
                    # or x = type(0)(5) , or int_type = type(0); x = int_type(5) . In this case we’ve used
                    # type(sys) and sys is a module, so we get back the module type object (essentially
                    # the same as a class object), and can use it to create a new module with the giv-
                    # en name.
                    module = type(sys)(name)

                    # Once we have a new (empty) module, we add it to the global list of modules
                    # to prevent the module from being accidentally reimported.
                    # This is done before calling exec() to more closely mimic the behavior of the import statement.
                    sys.modules[name] = module
                    exec(code, module.__dict__)  # module.__dict__ is environment
                    modules.append(module)
                except (EnvironmentError, SyntaxError) as err:
                    sys.modules.pop(name, None)
                    print(err)
                finally:
                    if fh is not None:
                        fh.close()
    return modules


def load_module_v2():
    # One theoretical problem with this approach is that it is potentially insecure.
    # The name variable could begin with sys; and be followed by some destructive code.
    modules = []
    for name in os_.listdir(os_.path.dirname(__file__) or '.'):
        if name.endswith('.py') and 'magic' in name.lower():
            name = os_.path.splitext(name)[0]  # remove extension
            if name.isidentifier() and name not in sys.modules:
                try:
                    exec("import " + name)
                    modules.append(sys.modules[name])
                except SyntaxError as err:
                    print(err)
    return modules


def load_module_v3():
    # This is the easiest way to dynamically import modules and is slightly safer
    # than using exec()
    modules = []
    for name in os_.listdir(os_.path.dirname(__file__) or '.'):
        if name.endswith('.py') and 'magic' in name.lower():
            name = os_.path.splitext(name)[0]  # remove extension
            if name.isidentifier() and name not in sys.modules:
                try:
                    module = __import__(name)
                    modules.append(module)
                except SyntaxError as err:
                    print(err)
    return modules


# None of the techniques shown here handles packages or modules in different
# paths, but it is not difficult to extend the code to accommodate these.

def get_function(module, function_name):
    """
    Load the specified function in the model with function_name
    :param module:
    :param function_name:
    :return:
    """
    # If hundreds of files were being processed (e.g., due to using *.* in the C:\windows
    # directory), we don’t want to go through the lookup process for every module
    # for every file. So immediately after defining the get_function() function, we
    # add an attribute to the function, a dictionary called cache . (In general, Python
    # allows us to add arbitrary attributes to arbitrary objects.) The first time that
    # get_function() is called the cache dictionary is empty, so the dict.get() call will
    # return None . But each time a suitable function is found it is put in the dictionary
    # with a 2-tuple of the module and function name used as the key and the function
    # itself as the value. So the second and all subsequent times a particular
    # function is requested the function is immediately returned from the cache and
    # no attribute lookup takes place at all.

    # The technique used for caching the get_function() ’s return value for a given set
    # of arguments is called memorizing.
    function = get_function.cache.get((module, function_name), None)
    if function is None:
        try:
            function = getattr(module, function_name)
            if not hasattr(function, "__call__"):
                raise AttributeError()
            get_function.cache[module, function_name] = function
        except AttributeError:
            function = None
    return function


get_function.cache = {}


def get_file_types(file_list):
    modules = load_modules()
    get_file_type_functions = []
    for module in modules:
        get_file_type = get_function(module, "get_file_type")
        if get_file_type is not None:
            get_file_type_functions.append(get_file_type)

    # This loop iterates over every file listed on the command line and for each one reads its first 1 000 bytes.
    # for file in get_files(sys.argv[1:]):
    for file in get_files(file_list):
        fh = None
        try:
            fh = open(file, 'rb')
            magic = fh.read(1000)
            for get_file_type in get_file_type_functions:
                filetype = get_file_type(magic, os_.path.splitext(file)[1])
                if filetype is not None:
                    print('{0:.<20}{1}'.format(filetype, file))
                    break
            else:
                print('{0:.<20}{1}'.format('Unknown', file))
        except EnvironmentError as err:
            print(err)

        finally:
            if fh is not None:
                fh.close()
