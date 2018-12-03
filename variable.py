import logging
# import ipdb
from numpy import linspace as np_linspace, round as np_round, array as np_array
from sympy import symbols as sp_symbols
# from collections import ChainMap

# Variable
# --> Contains
# --> ... Range, n_points, linspace
# goes into curve as an class

class Variable():
    def __init__(self, symbol, ran=None, val=None, is_const=False, n=None):
        logging.debug(f"Running class Variable for {symbol}, range:{ran},\
    val:{val}, constant:{is_const}")
        self._name = str(symbol)
        self._symbol = symbol
        self._ran = None if ran is None else tuple(float(x) for x in ran)
        logging.debug(f"init range: {self._ran}")
        #self._val = ran_or_val if type(ran_or_val) is int or float else None
        self._val = None if val is None else float(val)
        self._n = n
        self._linspace = None
        self._is_constant = is_const

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, s):
        self._symbol = s

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def ran(self):
        return self._ran

    @ran.setter
    def ran(self, r: tuple):
        if len(r) == 2:
            self._ran = (float(x) for x in r)
        else:
            self._ran = None

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, v):
        self._val = v

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, n):
        if (type(n) is int):
            self._n = n
        else:
            raise TypeError("Use an int")

    @property
    def is_constant(self):
        return self._is_constant

    @is_constant.setter
    def is_constant(self, is_const):
        self._is_constant = is_const

    @property
    def linspace(self):
        if type(self.ran) is tuple:
            try:
                logging.debug(f"using ran: {self.ran}, type {type(self.ran[0])} for linspace")
                self._linspace = np_round(
                    np_linspace(self.ran[0],
                                self.ran[-1],
                                self.n), decimals=3)
                logging.debug(f"running linspace for {self.name}, if linspace: {type(self._linspace)}")
            except:
                raise(ValueError("Could not assign linspace"))
            return self._linspace
        else:
            self._linspace = np_array(self.val)

        return self._linspace


    @linspace.setter
    def linspace(self, ls:list):
        self._linspace = ls

class Variables():
    """

    Args:
    """

    def __init__(self, Vars):
        # Reimpliment Chainmap init
        #self.maps = list(maps) or [{}]  # always at least one map
        key_names = [v.name for v in Vars]
        self._Vars = dict(zip(key_names, Vars))
        self.index = 0
        self._constant_var = None
        self._any_constant = False

        self._check_any_constant()

    # def __getattr__(self, name):
    #     """Override to get a variable name based on attribute from the dict Vars"""
    #     attr = self.Vars[name]
    #     return attr

    @property
    def Vars(self):
        return self._Vars

    @property
    def constant_var(self):
        return self._constant_var

    @constant_var.setter
    def constant_var(self, v):
        self._constant_var = v

    @property
    def any_constant(self):
        return self._any_constant

    @any_constant.setter
    def any_constant(self, d):
        self._any_constant = d

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if(self.index == len(self.Vars)):
            raise StopIteration
        else:
            V = list(self.Vars.values())[self.index]
            self.index += 1
            return V

    def _check_any_constant(self):
        runs = 0
        def check_constant(m):
            nonlocal runs
            runs+=1
            if m.is_constant is True:
                if self.any_constant is True:
                    raise RuntimeError("Can only have one constant variable!")
                else:
                    logging.debug(f"check_any_constant: constant var is {m.name}")
                    self.constant_var = m
                    return True

        def check_all(maps):
            if(any([check_constant(m) for m in maps])):
                return True

        if(type(self.Vars) is dict):
            if check_all(list(self.Vars.values())):
                self.any_constant = True
                return True
            else: return False
