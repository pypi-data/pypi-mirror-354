from ._core import __doc__, __version__, add, subtract


def cli():
    print(f"1 + 2 = {add(1,2)}")


if __name__ == "__main__":
    cli()
