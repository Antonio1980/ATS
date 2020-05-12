import inspect
import functools


def automation_logger(logger):

    def decorator(func):

        @functools.wraps(func)
        def log_wrapper(*args, **kwargs):
            cls_ = _get_class_that_defined_method(func)
            try:
                cls_name = cls_.__name__
            except AttributeError:
                cls_name = ''
            try:
                f_name = func.__name__
            except AttributeError:
                f_name = ''
            try:
                logger.logger.info(" {0} --> {1}".format(cls_name, f_name))
                return func(*args, **kwargs)
            except Exception as e:
                err = f_name + " {0} automation_wrapper throws an exception: {1}".format(e.__class__.__name__,
                                                                                         e.__cause__)
                logger.logger.fatal(err, exc_info=True)
                raise e

        return log_wrapper

    return decorator


def _get_class_that_defined_method(method):
    if inspect.ismethod(method):
        for cls in inspect.getmro(method.__self__.__class__):
            if cls.__dict__.get(method.__name__) is method:
                return cls
        method = method.__func__
    if inspect.isfunction(method):
        cls = getattr(inspect.getmodule(method),
                      method.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
