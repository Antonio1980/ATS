import pytest


def run(self):
    pytest.main(['-rxXs', '--capture=sys', '--capture=fd', '.', '-m', 'liveness', '-rEf'])


if __name__ == "__main__":
    run(None)
