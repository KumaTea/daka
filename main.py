import os

if os.name == 'posix':
    import uvloop
    uvloop.install()

from session import dk
from starting import starting

starting()

if __name__ == '__main__':
    dk.run()
