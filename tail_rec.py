from ast import *
from inspect import getsource


class TrampolineTransform(NodeTransformer):

    def visit_Return(self, node):
        return_val = node.value
        if return_val.__class__ == Call:
            func = return_val.func
            func_args = return_val.args
            # TODO kwargs

            return copy_location(Return(
                value=Tuple(elts=[
                    Str(s='__trampoline__'),
                    func, 
                    List(elts=func_args, ctx=Load())
                ], ctx=Load()), ctx=Load()
            ), node)
        return node


def compile_tco(f):
    ast = parse(getsource(f))
    tco_ast = fix_missing_locations(TrampolineTransform().visit(ast))
    return compile(tco_ast, '', 'exec')


def trampoline(f):
    def g(*args, **kwargs):
        result = f(*args, **kwargs)
        while isinstance(result, tuple) and result[0] == '__trampoline__':
            _, func, args = result
            result = func(*args)
        return result
    return g


def tail_rec(f, global_context=globals(), local_context=locals()):
    def g(*args, **kwargs):
        exec(compile_tco(f), global_context, local_context)
        return trampoline(f)(*args, **kwargs)
    return g

