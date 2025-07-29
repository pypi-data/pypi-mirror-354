"""Monitor the overhead of just executing any edea command."""


def target():
    from edea.cli import version

    version()


if __name__ == "__main__":
    target()
