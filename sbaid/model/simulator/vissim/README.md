# Vissim

## Threading

Some Vissim calls tend to take a long time which is
why we shouldn't do them on the main thread. However
COM doesn't play nice with threading which means we
basically have to do all COM stuff in the same thread.

For maintainability and to avoid confusion about in which
thread we currently are we have strict separation between
classes used in the main thread and classes used in the
vissim thread.
