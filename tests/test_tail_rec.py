from pytest import fixture

from tail_rec import tail_rec


def factorial(n, acc=1):
    if n == 1:
        return acc
    return factorial(n-1, n*acc)


def odd(n):
    if n == 1:
        return True
    return even(n-1)


def even(n):
    if n == 1:
        return False
    return odd(n-1)


global_context = globals()
local_context = locals()


def test_tail_rec():
    factorial2 = tail_rec(factorial, global_context, local_context)
    assert factorial2(10001) == factorial2(10000) * 10001

    even2 = tail_rec(even, global_context, local_context)
    assert even2(100000)
    assert not even2(99999)
