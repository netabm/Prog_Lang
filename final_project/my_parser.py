from AST_Node import ASTNode, FunctionDef, LambdaExpr, BinOp, UnaryOp, Variable, Number, Boolean, Call, Conditional


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0  # Position of the current token in the tokens list
        self.current_token = self.tokens[self.pos] if tokens else None
        self.current_lambda_expr = None  # Track current lambda expression for calls

    def eat(self, token_type):
        """
            Consume the current token if it matches the expected token_type,
            then advance to the next token. Raise an exception if the expected token is not found.
        """
        # print(f"Trying to eat {token_type}, current token: {self.current_token}")  # Debug
        if self.current_token and self.current_token[0] == token_type:
            # print(f"Token {self.current_token} matched {token_type}, advancing...")  # Debug
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
            else:
                self.current_token = (None, None)  # End of token stream
        else:
            raise Exception(f"Expected token {token_type} but got {self.current_token}")

    def parse(self):
        """
            Parse the entire token stream by repeatedly parsing statements until no tokens remain.
        """
        statements = []
        while self.current_token[0] is not None:  # Continue until no more tokens
            statement = self.parse_statement()
            if statement is not None:
                statements.append(statement)  # Add valid parsed statements to the list
        return statements

    def parse_statement(self):
        """
            Parse a statement, which can be a function definition, lambda expression, or any expression.
        """
        # print(f"Parsing statement with token: {self.current_token}")  # Debug
        if self.current_token[0] == 'DEFUN':
            return self.parse_function_def()
        elif self.current_token[0] == 'LAMBDA':
            return self.parse_lambda_expr()
        else:
            return self.parse_expression()

    def parse_function_def(self):
        """
            Parse a function definition of the form:
            Defun { name : identifier, arguments : (params) } body
        """
        # print("Parsing function definition")  # Debug
        self.eat('DEFUN')
        self.eat('LBRACE')
        self.eat('IDENTIFIER')  # Keyword 'name'
        self.eat('COLON')
        func_name = self.parse_identifier()  # Parse function name
        self.eat('COMMA')
        self.eat('IDENTIFIER')  # Keyword 'arguments'
        self.eat('COLON')
        params = self.parse_params()  # Parse function parameters
        self.eat('RBRACE')
        body = self.parse_expression()  # Parse the function body (expression)
        return FunctionDef(func_name, params, body)  # Return the function definition AST node

    def parse_lambda_expr(self):
        """
            Parse a lambda expression of the form:
            Lambd (params) . expression
        """
        # print("Parsing lambda expression")  # Debug
        self.eat('LAMBDA')
        params = []
        # Parse lambda parameters (comma-separated)
        while self.current_token[0] == 'IDENTIFIER':
            params.append(self.parse_identifier())
            # print(f"Lambda parameter: {params[-1]}")  # Debug
            if self.current_token[0] == 'COMMA':
                self.eat('COMMA')
        self.eat('DOT')
        body = self.parse_expression()
        lambda_expr = LambdaExpr(params, body)
        # print(f"Constructed lambda expression: {lambda_expr}")  # Debug

        # Check if the lambda expression is immediately followed by a call (lambda call)
        if self.current_token[0] == 'LPAREN':
            # print("Lambda expression is followed by a call, parsing lambda call")  # Debug
            return self.parse_lambda_call(lambda_expr)
        return lambda_expr

    def parse_lambda_call(self, lambda_expr):
        """
            Parse a lambda call of the form:
            lambda_expr(args)
        """
        # print("Parsing lambda call")  # Debug
        self.eat('LPAREN')
        args = self.parse_args()  # Parse the arguments of the lambda call
        self.eat('RPAREN')
        # print(f"Lambda call with args: {args}")  # Debug
        return Call(lambda_expr, args)  # Return a call node with the lambda expression and its arguments

    def parse_params(self):
        """
            Parse a list of parameters enclosed in parentheses: (param1, param2, ...)
        """
        params = []
        self.eat('LPAREN')
        while self.current_token[0] == 'IDENTIFIER':
            params.append(self.parse_identifier())
            # print(f"Function parameter: {params[-1]}")  # Debug
            if self.current_token[0] == 'COMMA':
                self.eat('COMMA')
        self.eat('RPAREN')  # Close the parameter list
        return params

    def parse_args(self):
        """
            Parse a list of arguments, separated by commas.
        """
        args = []
        # print(f"Parsing args, current token: {self.current_token}")  # Debug
        while self.current_token[0] != 'RPAREN':  # Continue until the closing parenthesis
            args.append(self.parse_expression())  # Parse each argument
            # print(f"Added argument: {args[-1]}")  # Debug
            if self.current_token[0] == 'COMMA':
                # print("Found comma, continuing to next argument")  # Debug
                self.eat('COMMA')  # Consume commas between arguments
            elif self.current_token[0] == 'RPAREN':
                # print("End of argument list found")  # Debug
                break
            else:
                raise Exception(f"Unexpected token in argument list: {self.current_token}")
        return args

    def parse_expression(self):
        """
            Parse an expression, which could be a comparison, arithmetic, boolean, function call,
            lambda expression, or conditional expression.
        """
        # print(f"Parsing expression with token: {self.current_token}")  # Debug
        expr = self.parse_comparison_expr()  # Start by parsing comparison expressions
        if self.current_token[0] == 'QUESTION':  # If a '?' is found, parse a conditional expression
            return self.parse_conditional_expr(expr)
        return expr

    def parse_conditional_expr(self, condition):
        # print("Parsing conditional expression")  # Debug
        self.eat('QUESTION')  # Expect the '?' token
        true_branch = self.parse_expression()  # Parse the true branch
        self.eat('COLON')  # Expect the ':' token
        false_branch = self.parse_expression()  # Parse the false branch
        return Conditional(condition, true_branch, false_branch)

    def parse_comparison_expr(self):
        """
            Parse a comparison expression, which can involve comparison operators (==, !=, <, >, etc.).
        """
        left = self.parse_boolean_expr()  # Parse the left-hand side of the comparison
        while self.current_token[0] == 'COMP_OP':  # Continue if comparison operators are found
            op = self.current_token[1]
            self.eat('COMP_OP')
            right = self.parse_boolean_expr()
            left = BinOp(left, op, right)
        return left

    def parse_boolean_expr(self):
        """
            Parse a boolean expression involving &&, ||, and ! operators.
        """
        left = self.parse_arithmetic_expr()  # Start with arithmetic expressions
        while self.current_token[0] == 'BOOL_OP':  # Continue if boolean operators are found
            op = self.current_token[1]
            self.eat('BOOL_OP')
            right = self.parse_arithmetic_expr()
            left = BinOp(left, op, right)
        return left

    def parse_arithmetic_expr(self):
        """
            Parse arithmetic expressions involving +, -, *, /, and % operators.
        """

        def parse_factor():
            return self.parse_term()  # A factor is a single term

        def parse_term():
            left = parse_factor()
            while self.current_token[0] == 'ARITH_OP' and self.current_token[1] in ['*', '/', '%']:
                op = self.current_token[1]
                self.eat('ARITH_OP')
                right = parse_factor()
                left = BinOp(left, op, right)
            return left

        left = parse_term()  # Parse a full term (with *, /, %)
        while self.current_token[0] == 'ARITH_OP' and self.current_token[1] in ['+', '-']:
            op = self.current_token[1]
            self.eat('ARITH_OP')
            right = parse_term()
            left = BinOp(left, op, right)
        return left

    def parse_term(self):
        """
            Parse a term, which can be a variable, number, boolean, unary operation, or expression in parentheses.
        """
        if self.current_token[0] == 'NOT':
            self.eat('NOT')
            return UnaryOp('!', self.parse_term())  # Parse a unary NOT operation
        elif self.current_token[0] == 'ARITH_OP' and self.current_token[1] == '-':
            self.eat('ARITH_OP')
            return UnaryOp('-', self.parse_term())  # Parse a unary minus operation
        elif self.current_token[0] == 'IDENTIFIER':
            # Check if it's a function call
            if (self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == 'LPAREN'):
                return self.parse_function_call()  # Parse a function call
            identifier = Variable(self.parse_identifier())  # Parse an identifier
            return identifier
        elif self.current_token[0] == 'INTEGER':
            number = Number(self.current_token[1])  # Parse an integer literal
            self.eat('INTEGER')
            return number
        elif self.current_token[0] == 'BOOLEAN':
            boolean = Boolean(self.current_token[1])  # Parse a boolean literal
            self.eat('BOOLEAN')
            return boolean
        elif self.current_token[0] == 'LPAREN':
            self.eat('LPAREN')
            expr = self.parse_expression()  # Parse an expression in parentheses
            self.eat('RPAREN')  # Ensure the expression is closed properly

            # Check if the expression was a lambda expression and is followed by arguments (a lambda call)
            if isinstance(expr, LambdaExpr) and self.current_token[0] == 'LPAREN':
                return self.parse_lambda_call(expr)
            return expr
        elif self.current_token[0] == 'LAMBDA':
            lambda_expr = self.parse_lambda_expr()
            # Check if the lambda expression is followed by a lambda call (arguments)
            if self.current_token[0] == 'LPAREN':
                return self.parse_lambda_call(lambda_expr)
            return lambda_expr
        else:
            raise Exception(f"Unexpected token: {self.current_token}")

    def parse_function_call(self):
        """
            Parse a function call of the form:
            function_name(args)
        """
        # print(f"Parsing function call for: {self.current_token}")  # Debug
        func_name = self.parse_identifier()
        self.eat('LPAREN')
        args = self.parse_args()
        self.eat('RPAREN')
        # print(f"Function call '{func_name}' with args: {args}")  # Debug
        return Call(func_name, args)

    def parse_identifier(self):
        """
            Parse an identifier and return its value.
        """
        if self.current_token[0] == 'IDENTIFIER':
            identifier = self.current_token[1]
            self.eat('IDENTIFIER')
            return identifier
        raise Exception(f"Expected IDENTIFIER but got {self.current_token}")
