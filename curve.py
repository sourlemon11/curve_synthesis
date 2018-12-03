import logging
from sympy import lambdify
from numpy import array as np_array

from variable import Variable, Variables

""" Plotting Setup """
class Curve(Variables):
    def __init__(self, Vars:object):
        super().__init__(Vars)
        self.func = None
        self.const = None
        self.indep_pts = None
        self.x = None
        self._x_lim = None
        self.y = None
        self._y_lim = None

        # key_names = [v.name for v in Vars]
        # self._Vars = dict(zip(key_names, Vars))

    def lambdify(self, sympy_func, mod="numpy"):
        syms = tuple(v.symbol for v in self.Vars.values())
        self.func = lambdify(syms,
                             sympy_func,
                             modules=[mod])
        logging.debug(f"function {self.func} using syms: {syms}")
        try:
            return self.func
        except:
            print("oh well")

    def lambdify_single(self, sympy_func, sym_val:dict):
        # 1 match symval str to var string
        self.func = lambdify()

    def coord_gen(self, sym_val={}):
        logging.debug(f"Running coord_gen")
        # args = [v.linspace for v in self.Vars]
        self.x = []
        self.y = []

        def generate_points(_vars, const=None):
            logging.debug(f"Running generate_points")
            def lamb_const_linspace(var, const):
                logging.debug(f"Running lamb_const_linspace")
                if var.is_constant: return const
                else: return var.linspace

            if const is not None:
                logging.debug(f"const is not None")
                args = tuple(lamb_const_linspace(v,const) for v in self.Vars.values())
            else:
                logging.debug(f"const is not not None")
                args = tuple(v.linspace for v in self.Vars.values())

            logging.debug(f"using args {args}")
            gpts = self.func(*args)
            # use [x][x] to exclude datatype element
            logging.debug(f"ASSIGNING POINTS with function {self.func}")
            # logging.debug(f"{ gpts[0][0] }")
            self.x.append(np_array(gpts[0][0]))
            self.y.append(np_array(gpts[1][0]))

        #print("--------CURVE------------")
        #print("length is vars is {}".format(len(list(v for v in self.Vars.values()))))
        #print("any constant is {}".format(self.Vars.any_constant))
        #print("constant var is {}".format(self.Vars.constant_var))
        #print("------------------------")
        if self.any_constant is True:
            if self.constant_var.ran is not None:
                logging.debug(f"running if self.Vars.constant_var.ran is not None:")
                for ct in self.constant_var.linspace:
                    generate_points(self.Vars, const=ct)

            elif self.constant_var.val is not None:
                logging.debug(f"running if self.Vars.constant_var.val is not None:")
                logging.debug(f"{ list(v.name for v in self.Vars.values()) }")
                generate_points(self.Vars)

        elif len(list(v for v in self.Vars.values())) == 1 and self.check_any_constant is False:
            logging.debug(f"running elif len(list(v for v in self.Vars.values())) == 1 and self.Vars.check_any_constant is False:")
            generate_points(self.Vars)

        else:
            raise ValueError("No constant var included in class 'Vars', in\
            'vars'")

        logging.debug(f"ASSIGNED X {self.x}")
        logging.debug(f"LENGTH X {len(self.x)}")

    @property
    def x_lim(self):
        x_min = min(x for i in self.x for x in i)
        x_max = max(x for i in self.x for x in i)
        self._x_lim = [x_min - 0.1 * abs(x_min), x_max + 0.1 * abs(x_max)]
        return self._x_lim

    @property
    def y_lim(self):
        y_min = min(y for i in self.y for y in i)
        y_max = max(y for i in self.y for y in i)
        self._y_lim = [y_min - 0.1 * abs(y_min), y_max + 0.1 * abs(y_max)]
        return self._y_lim

    def plot(self):
        pass
