class ASTNode:
    # Base class for all AST nodes
    pass

class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name  # Name of the function
        self.params = params  # List of parameters
        self.body = body  # Body of the function

    def __repr__(self):
        return f"FunctionDef(name={self.name}, params={self.params}, body={self.body})"

class LambdaExpr(ASTNode):
    def __init__(self, params, body):
        self.params = params  # List of parameters
        self.body = body  # Body of the lambda expression

    def __repr__(self):
        return f"LambdaExpr(params={self.params}, body={self.body})"

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left  # Left operand
        self.op = op  # Operator (e.g., +, -, *, /)
        self.right = right  # Right operand

    def __repr__(self):
        return f"BinOp(left={self.left}, op={self.op}, right={self.right})"

class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op  # Operator (e.g., -, !)
        self.expr = expr  # Expression to which the operator is applied

    def __repr__(self):
        return f"UnaryOp(op={self.op}, expr={self.expr})"

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name  # Name of the variable

    def __repr__(self):
        return f"Variable(name={self.name})"

class Number(ASTNode):
    def __init__(self, value):
        self.value = value  # Numeric value

    def __repr__(self):
        return f"Number(value={self.value})"

class Boolean(ASTNode):
    def __init__(self, value):
        self.value = value  # Boolean value (True or False)

    def __repr__(self):
        return f"Boolean(value={self.value})"

class Call(ASTNode):
    def __init__(self, func, args):
        self.func = func  # Function being called
        self.args = args  # Arguments to the function

    def __repr__(self):
        return f"Call(func={self.func}, args={self.args})"

class Conditional(ASTNode):
    def __init__(self, condition, true_expr, false_expr):
        self.condition = condition  # Condition expression
        self.true_expr = true_expr  # Expression if condition is true
        self.false_expr = false_expr  # Expression if condition is false

    def __repr__(self):
        return (f"Conditional(condition={self.condition}, "
                f"true_expr={self.true_expr}, false_expr={self.false_expr})")
