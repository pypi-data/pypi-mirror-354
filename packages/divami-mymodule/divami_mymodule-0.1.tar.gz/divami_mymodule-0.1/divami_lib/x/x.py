def Harshith(name):
    print(f"Hi This was {name} Module")

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: Harshith <name>")
        sys.exit(1)
    name = sys.argv[1]
    Harshith(name)