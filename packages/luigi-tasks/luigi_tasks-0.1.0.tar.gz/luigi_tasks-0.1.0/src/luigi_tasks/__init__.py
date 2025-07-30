from .tasks import HelloTask, PrintTask

__version__ = "0.1.0"
__all__ = ['HelloTask', 'PrintTask']

def main() -> None:
    print("Hello from luigi-tasks!")
