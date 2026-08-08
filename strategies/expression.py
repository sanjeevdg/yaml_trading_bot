import ast
import operator


class SafeExpressionEvaluator:

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def __init__(self, variables):
        self.variables = variables

    def evaluate(self, expression):

        try:
            tree = ast.parse(
                expression,
                mode="eval"
            )
        except SyntaxError as exc:
            raise ValueError(
                f"Invalid expression: {expression}"
            ) from exc

        return float(
            self._evaluate_node(tree.body)
        )

    def _evaluate_node(self, node):

        #
        # Numeric constants
        #

        if isinstance(node, ast.Constant):

            if isinstance(
                node.value,
                (int, float)
            ):
                return float(node.value)

            raise ValueError(
                "Only numeric constants are allowed"
            )

        #
        # Variables
        #

        if isinstance(node, ast.Name):

            if node.id not in self.variables:

                raise ValueError(
                    f"Unknown variable: {node.id}"
                )

            return float(
                self.variables[node.id]
            )

        #
        # Arithmetic operations
        #

        if isinstance(node, ast.BinOp):

            operation = self.OPERATORS.get(
                type(node.op)
            )

            if operation is None:

                raise ValueError(
                    f"Operator not allowed: "
                    f"{type(node.op).__name__}"
                )

            left = self._evaluate_node(
                node.left
            )

            right = self._evaluate_node(
                node.right
            )

            return operation(
                left,
                right
            )

        #
        # Unary + / -
        #

        if isinstance(node, ast.UnaryOp):

            operation = self.OPERATORS.get(
                type(node.op)
            )

            if operation is None:

                raise ValueError(
                    f"Operator not allowed: "
                    f"{type(node.op).__name__}"
                )

            value = self._evaluate_node(
                node.operand
            )

            return operation(value)

        #
        # Everything else is forbidden
        #

        raise ValueError(
            f"Expression element not allowed: "
            f"{type(node).__name__}"
        )