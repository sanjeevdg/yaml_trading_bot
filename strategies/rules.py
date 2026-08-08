from strategies.base import Strategy
from signals.signal import Signal, Action


class RuleStrategy(Strategy):

    def __init__(self, parameters=None, buy=None, sell=None):
        self.params = parameters or {}
        self.buy_rules = buy or {}
        self.sell_rules = sell or {}

    def evaluate(self, df):

        if len(df) < 2:
            return Signal(
                action=Action.HOLD,
                symbol=df.iloc[-1]["symbol"],
                price=float(df.iloc[-1]["close"]),
                reason="Not enough data"
            )

        current = df.iloc[-1]
        previous = df.iloc[-2]

        if self.evaluate_group(
            self.buy_rules,
            current,
            previous
        ):
            return Signal(
                action=Action.BUY,
                symbol=current["symbol"],
                price=float(current["close"]),
                reason="YAML buy rules satisfied"
            )

        if self.evaluate_group(
            self.sell_rules,
            current,
            previous
        ):
            return Signal(
                action=Action.SELL,
                symbol=current["symbol"],
                price=float(current["close"]),
                reason="YAML sell rules satisfied"
            )

        return Signal(
            action=Action.HOLD,
            symbol=current["symbol"],
            price=float(current["close"]),
            reason="No YAML rule satisfied"
        )

    def evaluate_group(self, group, current, previous):

        if not group:
            return False

        if "all" in group:

            return all(
                self.evaluate_rule(
                    rule,
                    current,
                    previous
                )
                for rule in group["all"]
            )

        if "any" in group:

            return any(
                self.evaluate_rule(
                    rule,
                    current,
                    previous
                )
                for rule in group["any"]
            )

        return False

    def evaluate_rule(self, rule, current, previous):

        left = self.resolve_value(
            rule["left"],
            current,
            previous
        )

        right = self.resolve_value(
            rule["right"],
            current,
            previous
        )

        op = rule["op"]

        if op == ">":
            return left > right

        if op == "<":
            return left < right

        if op == ">=":
            return left >= right

        if op == "<=":
            return left <= right

        if op == "==":
            return left == right

        if op == "!=":
            return left != right

        if op == "crossover":

            previous_left = self.resolve_value(
                rule["left"],
                previous
            )

            previous_right = self.resolve_value(
                rule["right"],
                previous
            )

            return (
                previous_left <= previous_right
                and left > right
            )

        if op == "crossunder":

            previous_left = self.resolve_value(
                rule["left"],
                previous
            )

            previous_right = self.resolve_value(
                rule["right"],
                previous
            )

            return (
                previous_left >= previous_right
                and left < right
            )

        raise ValueError(
            f"Unknown rule operator: {op}"
        )

    def resolve_value(
        self,
        value,
        current,
        previous=None
    ):

        if isinstance(value, (int, float)):
            return float(value)

        #
        # Dictionary expression
        #

        if isinstance(value, dict):

            expression = value.get("expression")

            if expression is None:
                raise ValueError(
                    f"Invalid rule expression: {value}"
                )

            return self.evaluate_expression(
                expression,
                current,
                previous
            )

        if not isinstance(value, str):
            raise ValueError(
                f"Invalid rule value: {value}"
            )

        #
        # Strategy parameter
        #

        if value in self.params:

            return float(
                self.params[value]
            )

        #
        # Current dataframe column
        #

        if value in current.index:

            return float(
                current[value]
            )

        #
        # Previous candle column
        #

        if value.startswith("previous."):

            if previous is None:
                raise ValueError(
                    "Previous candle unavailable"
                )

            column = value.split(
                ".", 1
            )[1]

            if column not in previous.index:
                raise ValueError(
                    f"Unknown previous column: {column}"
                )

            return float(
                previous[column]
            )

        #
        # Parameter substitution
        #

        if "{" in value and "}" in value:

            resolved = value

            for name, parameter in self.params.items():

                resolved = resolved.replace(
                    f"{{{name}}}",
                    str(parameter)
                )

            value = resolved

            if value in current.index:

                return float(
                    current[value]
                )

        #
        # Numeric value
        #

        try:
            return float(value)

        except ValueError:
            pass

        raise ValueError(
            f"Unable to resolve rule value: {value}"
        )


    def evaluate_expression(
        self,
        expression,
        current,
        previous
    ):

        expression = expression.strip()

        #
        # Previous candle high
        #

        expression = expression.replace(
            "previous.high",
            str(float(previous["high"]))
        )

        #
        # Previous candle low
        #

        expression = expression.replace(
            "previous.low",
            str(float(previous["low"]))
        )

        #
        # Current ATR
        #

        if "ATR" in expression:

            if "ATR" not in current.index:
                raise ValueError(
                    "ATR column not found"
                )

            expression = expression.replace(
                "ATR",
                str(float(current["ATR"]))
            )

        #
        # Strategy parameters
        #

        for name, value in self.params.items():

            expression = expression.replace(
                name,
                str(value)
            )

        #
        # Evaluate arithmetic expression
        #

        try:

            return float(
                eval(
                    expression,
                    {
                        "__builtins__": {}
                    }
                )
            )

        except Exception as exc:

            raise ValueError(
                f"Unable to evaluate expression "
                f"'{expression}': {exc}"
            )    
        