
Wish brings **selectable return values** to Python.

Overview
--------------------------------------------------------------------------------

It's already very easy to deal with functions
having several possible sets of arguments in Python.
Why? Because the language supports natively:

  - [default argument values](https://docs.python.org/2.7/tutorial/controlflow.html#default-argument-values)
  - [keyword arguments](https://docs.python.org/2.7/tutorial/controlflow.html#keyword-arguments)
  - [argument unpacking](https://docs.python.org/2.7/tutorial/controlflow.html#unpacking-argument-lists)

Now for return values, beyond tuples to deal with multiple values, 
Python provides actually little constructs. 
Using functions that return many values is often tedious.
Wish provides selectable return values to solve this issue.

Quickstart
--------------------------------------------------------------------------------

 1. Install wish with pip ([instructions](installation)).

 2. Replace your function with many arguments `f` with

        def f(...):
            ...
            return a, b, c, ..., z

    with


        import wish

        def f(..., returns="a, b"):
            ...
            return wish.grant(returns)

 3. Update the documentation of your function


    !!! Note ""

        **Parameters:**
        
          - ...

          - `returns`: string, optional.
            Select the returned values, among `a`, `b`, ..., `z`.
            Default is `"a, b"`.

        **Returns:**

          - `a`: ...

          - `b`: ...

          - `c`: ..., not returned by default

          - ...

          - `z`: ..., not returned by default

  4. Use the flexibility of the new API

         >>> a, b = f(...)
         >>> w, i, s, h = f(..., returns="w, i, s, h")


