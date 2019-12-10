import inspect
import jsonpickle
import functools
import random
import string
from collections import defaultdict

class formctrl(object):
    
    forms = defaultdict(list)
    
    def __init__(self, form):
        self._has_arg = True
        self._func = None
        self._sig = None
        self._doc = None
        if callable(form):
            # then the decorator is created without a parameter
            self._has_arg = False
            self._form = 'form_%s' % formctrl._generate_name()
            self._set_func_info(form)
        else:
            self._form = form
        self._n_calls = 0
        
    def __call__(self, *args, **kwargs):
        if self._has_arg:
            self._set_func_info(args[0])
            def wrapper(*args, **kwargs):
                self._n_calls += 1
                return self._func(*args, **kwargs)
            return wrapper
        else:
            self._n_calls += 1
            return self._func(*args)
    
    def _set_func_info(self, func):
        self._func = func
        self._sig = inspect.signature(self._func)
        self._doc = inspect.getdoc(self._func)
        functools.update_wrapper(self, func)
        if not self in formctrl.forms[self._form]:
            formctrl.forms[self._form].append(self)        
    
    def __str__(self):
        return '<formctrl name=%s func=%s>' % (self.form_name(), self.func_name())

    def __repr__(self):
        return self.__str__()
    
    def func_name(self):
        return self._func.__name__
    
    def form_name(self):
        return self._form
    
    def signature_json(self):
        return jsonpickle.encode(self._sig)
    
    def docstring(self):
        return self._doc
    
    def num_calls(self):
        return self._n_calls
    
    @staticmethod
    def _generate_name(length=5):
        """Generate a random string of fixed length """
        letters= string.ascii_lowercase
        return ''.join(random.sample(letters, length))
    
