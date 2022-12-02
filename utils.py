from pipe import Pipe


def lines(filepath: str):
    """
    Generator that returns each line of the file, one by one.
    """
    import pathlib
    from os import path
    with open(path.join(pathlib.Path(__file__).parent.resolve(), filepath), 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            yield line.removesuffix('\n')


@Pipe
def reduce(iter, op):
    return op(iter)


@Pipe
def log(iter):
    print(iter)


def day_number(filepath: str):
    import pathlib
    return pathlib.Path(filepath).stem
