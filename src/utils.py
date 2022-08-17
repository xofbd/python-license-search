import os
import pickle


def cache(cache_dir):
    def wrapped(func):
        def wrapper(*args):
            if not os.path.exists(cache_dir):
                os.mkdir(cache_dir)
            path = os.path.join(cache_dir, "_".join(args) + ".pkl")

            result = func(*args)
            with open(path, "wb") as f:
                pickle.dump(result, f)

            return result

        return wrapper

    return wrapped
