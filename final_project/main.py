from my_interpreter import Interpreter
import sys

def main():
    if len(sys.argv) > 1:
        # Run the interpreter with a program file
        file_path = sys.argv[1]
        interpreter = Interpreter()
        interpreter.run_program(file_path)
    else:
        print("Welcome to My Interpreter!")
        # Run the interpreter in interactive mode
        interpreter = Interpreter()
        interpreter.repl()

if __name__ == "__main__":
    main()