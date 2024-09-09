from AST_Node import ASTNode, FunctionDef, LambdaExpr, BinOp, UnaryOp, Variable, Number, Boolean, Call, Conditional
from my_lexer import tokenize
from my_parser import Parser


class Closure:
    def __init__(self, func, env):
        self.func = func
        self.env = env


class Interpreter:
    def __init__(self):
        self.global_scope = {}
        self.call_stack = []

    def execute(self, node):
        # Execute the given AST node based on its type
        if isinstance(node, FunctionDef):
            # Store function definitions in the global scope
            self.global_scope[node.name] = node
        elif isinstance(node, LambdaExpr):
            # Return a closure for lambda expressions
            return Closure(node, self.global_scope.copy())
        elif isinstance(node, BinOp):
            # Handle binary operations
            if node.op == '||':
                left = self.execute(node.left)
                if left:
                    return left
                return self.execute(node.right)
            elif node.op == '&&':
                left = self.execute(node.left)
                if not left:
                    return left
                return self.execute(node.right)
            else:
                left = self.execute(node.left)
                right = self.execute(node.right)
                return self.evaluate_binop(node.op, left, right)
        elif isinstance(node, UnaryOp):
            # Handle unary operations
            expr = self.execute(node.expr)
            return self.evaluate_unaryop(node.op, expr)
        elif isinstance(node, Variable):
            # Look up variable values
            value = self.lookup_variable(node.name)
            return value
        elif isinstance(node, Number):
            # Return number values directly
            return node.value
        elif isinstance(node, Boolean):
            # Return boolean values directly
            return node.value
        elif isinstance(node, Call):
            # Handle function calls
            return self.execute_call(node)
        elif isinstance(node, Conditional):
            # Handle conditional expressions
            condition = self.execute(node.condition)
            if condition:
                return self.execute(node.true_expr)
            else:
                return self.execute(node.false_expr)
        else:
            raise Exception(f"Unknown AST node: {node}")

    def evaluate_binop(self, op, left, right):
        # Evaluate binary operations
        if op == '&&':
            return left and right
        elif op == '||':
            return left or right
        elif op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right == 0:
                raise ZeroDivisionError("Error: Division by zero")
            return left // right
        elif op == '%':
            return left % right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '>':
            return left > right
        elif op == '<':
            return left < right
        elif op == '>=':
            return left >= right
        elif op == '<=':
            return left <= right
        else:
            raise Exception(f"Unknown operator: {op}")

    def evaluate_unaryop(self, op, expr):
        # Evaluate unary operations
        if op == '!':
            return not expr
        elif op == '-':
            return -expr
        else:
            raise Exception(f"Unknown unary operator: {op}")

    def lookup_variable(self, name):
        # Look up variable values in the current scope and call stack
        if name in self.global_scope:
            return self.global_scope[name]
        for scope in reversed(self.call_stack):
            if name in scope:
                return scope[name]
        raise Exception(f"Undefined variable: {name}")

    def execute_call(self, node):
        # Execute function calls
        if isinstance(node.func, Closure):
            func = node.func.func
            env = node.func.env
        elif isinstance(node.func, LambdaExpr):
            func = node.func
            env = self.global_scope.copy()
        else:
            func = self.lookup_variable(node.func)
            env = self.global_scope.copy()

        # Check if the function is a named FunctionDef (not a lambda)
        if isinstance(func, FunctionDef):
            # Perform argument count check only for named functions
            if len(node.args) != len(func.params):
                raise Exception(f"Error: {func.name} expects {len(func.params)} arguments but got {len(node.args)}")

        if isinstance(func, FunctionDef) or isinstance(func, LambdaExpr):
            # Evaluate arguments
            evaluated_args = [self.execute(arg) for arg in node.args]

            if isinstance(func, FunctionDef):
                func_params = func.params
                func_body = func.body
            else:  # LambdaExpr
                func_params = func.params
                func_body = func.body

            # Create a new scope for the function call
            new_scope = env.copy()
            new_scope.update(dict(zip(func_params, evaluated_args)))
            self.call_stack.append(self.global_scope.copy())
            self.global_scope = new_scope

            # Execute the function body
            result = self.execute(func_body)

            # Restore the previous scope
            self.global_scope = self.call_stack.pop()

            # If the result is another Closure, execute it with the remaining arguments
            while isinstance(result, Closure) and len(node.args) > len(func_params):
                remaining_args = node.args[len(func_params):]
                result = self.execute(Call(func=result, args=remaining_args))

            return result
        else:
            raise Exception(f"Unknown function: {node.func}")

    def repl(self):
        # Read-Eval-Print Loop (REPL) for interactive execution
        print("Type 'exit' or 'quit' to leave the interactive mode.")
        while True:
            try:
                code = input(">>> ")
                if code.lower() in {'exit', 'quit'}:
                    print("Goodbye!")
                    break
                tokens = tokenize(code)
                parser = Parser(tokens)
                ast = parser.parse()
                print(ast)
                for node in ast:
                    result = self.execute(node)
                    if result is not None:
                        print(result)
                        print()
            except Exception as e:
                print(e)
                print()

    def run_program(self, file_path):
        # Execute a program from a file
        try:
            with open(file_path, 'r') as file:
                code = file.read()
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return

        try:
            tokens = tokenize(code)
            parser = Parser(tokens)
            ast = parser.parse()
        except Exception as e:
            print(f"An error occurred while parsing the code: {e}")
            return

        for node in ast:
            print(node)
            try:
                result = self.execute(node)
                if result is not None:
                    print(result)
                    print()
            except Exception as e:
                print(f"An error occurred during execution: {e}")
                print()
