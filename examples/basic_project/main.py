"""
Basic project example for PyllmValidate.
"""

from .math_operations import add, subtract


def main():
    """Main function demonstrating basic operations."""
    a = 10
    b = 5
    
    print(f"Adding {a} and {b}: {add(a, b)}")
    print(f"Subtracting {b} from {a}: {subtract(a, b)}")


if __name__ == "__main__":
    main() 