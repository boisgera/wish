
The Classic API
--------------------------------------------------------------------------------

Consider the following use case: the computation of the
(approximate) derivative of a function with Newton's difference quotient:

    def d(f, x, h=1e-13):
        dq = (f(x + h) - f(x)) / h
        return dq

This function `d` would typically be used like this:

    >>> from math import sin
    >>> d(sin, x=0.0)
    0.9999999999999983

Now, an improved version of `d` would compute an error estimate `error`

    def d(f, x, h=1e-7):
        dq = (f(x + h) - f(x)) / h
        dq2 = (f(x + 0.5*h) - f(x)) / (0.5*h)
        error = 2 * (dq - dq2)
        return dq, error

whose usage would be

    >>> d(sin, x=0.0)
    (0.9999999999999983, -2.4424906541753444e-15)


While this is a sound idea to provide an error estimate, 
we have broken the original API. 
Now, in the simplest and more common use case,
when we do not care about the error, 
the code is more complex than it should be[^1]:

    >>> import math
    >>> dq, _ = d(sin, x=0.0)
    >>> dq 
    0.9999999999999983

[^1]: Conventionally, a variable is named `_` if its value is ignored.


With Wish
--------------------------------------------------------------------------------

To get a decent API in both cases, we may use wish and
specify in the function signature an extra argument that lists the value(s) 
returned by default

    def d(f, x, h=1e-7, returns="dq"):
        dq = (f(x + h) - f(x)) / h
        dq2 = (f(x + 0.5*h) - f(x)) / (0.5*h)
        error = 2 * (dq - dq2)
        return wish.grant(returns)

With this pattern, the common case is still simple

    >>> d(sin, x=0.0)
    0.9999999999999983

but the more complex case is possible and the intent is explicit:

    >>> d(sin, x=0.0, returns="dq, error")
    (0.9999999999999983, -2.4424906541753444e-15)


