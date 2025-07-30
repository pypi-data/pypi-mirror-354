from relationalai.early_access.dsl.core.exprs import contextStack
from relationalai.early_access.dsl.core.exprs.scalar import ScalarExpr
from relationalai.early_access.dsl.core.logic import LogicFragment


class Aggregation(LogicFragment, ScalarExpr):

    # Each Schema object is a ContextManager
    def __enter__(self):
        contextStack.push(self)  # open a new context for this Schema
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        contextStack.pop()

    def __init__(self, method):
        LogicFragment.__init__(self)
        self._method = method
        self._aggregates = None
        self._schema = self

    def aggregates(self, var):
        self._aggregates = var

    def display(self):
        vars = [v.display() for v in self._scalars.values()]

        args = ", ".join(vars)
        body = self.rel_formula()
        return f"{self._method}[" + args + ":" + body + "]"

    def grounded(self): return False

    def rename(self, renaming) -> 'Aggregation':
        new_vars = {}
        for d in self._scalars:
            dv = self._scalars[d]
            if d in renaming:
                new_vars[d] = dv.rename(renaming[d])
            else:
                new_vars[d] = dv

        renamed_agg = Aggregation(self._method)
        renamed_agg._aggregates = self._aggregates
        renamed_agg._scalars = new_vars

        renamed_agg._existentials = self._existentials
        renamed_agg._atoms = self._atoms
        renamed_agg._sconstraints = self._sconstraints

        return renamed_agg

    def pprint(self): return self.display()

    @staticmethod
    def max(var):
        return Aggregation._agg(var, "max")

    @staticmethod
    def min(var):
        return Aggregation._agg(var, "min")

    @staticmethod
    def argmax(var):
        return Aggregation._agg(var, "argmax")

    @staticmethod
    def argmin(var):
        return Aggregation._agg(var, "argmin")

    @staticmethod
    def sum(var):
        return Aggregation._agg(var, "sum")

    @staticmethod
    def count(var):
        return Aggregation._agg(var, "count")

    @staticmethod
    def _agg(var, method):
        agg = Aggregation(method)
        var == agg
        return agg