from strategies.base import Strategy
from signals.signal import Signal, Action
from strategies.expression import SafeExpressionEvaluator
from strategies.resolver import IndicatorValueResolver

class RuleStrategy(Strategy):

    def __init__(self, parameters=None, signals=None):
        self.params = parameters or {}
        self.signals = signals or {}

        self.buy_rules = self.signals.get("BUY", {})
        self.sell_rules = self.signals.get("SELL", {})
        '''
        for action, rules in self.signals.items():
            if self.evaluate_group(rules, current, previous):
                return Signal(
                    action=Action[action],
                    symbol=current["symbol"],
                    price=float(current["close"]),
                    reason=f"YAML {action} rules satisfied"
                )
        '''
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
        #print("RULE PARAMS:", self.params)
        #print("BUY RULES:", self.buy_rules)
        #print("SELL RULES:", self.sell_rules)
        #print("COLUMNS:", df.columns.tolist())    
        return Signal(
            action=Action.HOLD,
            symbol=current["symbol"],
            price=float(current["close"]),
            reason="No YAML rule satisfied"
        )

    def evaluate_group(
        self,
        group,
        current,
        previous
    ):

        if not group:
            return False

        #
        # ALL
        #

        if "all" in group:

            return all(
                self.evaluate_item(
                    item,
                    current,
                    previous
                )
                for item in group["all"]
            )

        #
        # ANY
        #

        if "any" in group:

            return any(
                self.evaluate_item(
                    item,
                    current,
                    previous
                )
                for item in group["any"]
            )

        #
        # A group itself can also be a rule
        #

        return self.evaluate_item(
            group,
            current,
            previous
        )

    def evaluate_item(
        self,
        item,
        current,
        previous
    ):

        #
        # Nested ALL group
        #

        if "all" in item:

            return self.evaluate_group(
                item,
                current,
                previous
            )

        #
        # Nested ANY group
        #

        if "any" in item:

            return self.evaluate_group(
                item,
                current,
                previous
            )

        #
        # Normal comparison rule
        #

        return self.evaluate_rule(
            item,
            current,
            previous
        )    

    def evaluate_rule(self, rule, current, previous):

        #
        # Evaluate the rule against the CURRENT candle
        #

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

        #
        # Crossover
        #

        if op == "crossover":

            previous_left = self.resolve_value(
                rule["left"],
                previous,
                None
            )

            previous_right = self.resolve_value(
                rule["right"],
                previous,
                None
            )

            return (
                previous_left <= previous_right
                and left > right
            )

        #
        # Crossunder
        #

        if op == "crossunder":

            previous_left = self.resolve_value(
                rule["left"],
                previous,
                None
            )

            previous_right = self.resolve_value(
                rule["right"],
                previous,
                None
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

        #
        # Dictionary expression
        #

        if isinstance(value, dict):

            expression = value.get("expression")

            if expression is None:
                raise ValueError(
                    f"Invalid expression: {value}"
                )

            return self.evaluate_expression(
                expression,
                current,
                previous
            )

        #
        # String / numeric / indicator resolution
        #

        return IndicatorValueResolver.resolve(
            value,
            current=current,
            previous=previous,
            parameters=self.params
        )


    

        
    def evaluate_expression(
        self,
        expression,
        current,
        previous
    ):

        variables = {}

        #
        # Current candle
        #

        for column in current.index:

            value = current[column]

            try:
                variables[column] = float(value)
            except (TypeError, ValueError):
                pass

        #
        # Previous candle
        #

        if previous is not None:

            for column in previous.index:

                value = previous[column]

                try:
                    variables[f"previous_{column}"] = float(value)
                except (TypeError, ValueError):
                    pass

            #
            # Explicit aliases for expressions
            #

            try:
                variables["previous_open"] = float(previous["open"])
                variables["previous_high"] = float(previous["high"])
                variables["previous_low"] = float(previous["low"])
                variables["previous_close"] = float(previous["close"])
                variables["previous_volume"] = float(previous["volume"])
            except (KeyError, TypeError, ValueError):
                pass

        #
        # Strategy parameters
        #

        for name, value in self.params.items():

            try:
                variables[name] = float(value)

            except (TypeError, ValueError):
                pass

        #
        # Convert friendly YAML references
        #
        # previous.high
        # previous.low
        # previous.close
        #
        # into safe variable names.
        #

        expression = expression.replace(
            "previous.high",
            "previous_high"
        )

        expression = expression.replace(
            "previous.low",
            "previous_low"
        )

        expression = expression.replace(
            "previous.close",
            "previous_close"
        )

        expression = expression.replace(
            "previous.open",
            "previous_open"
        )

        expression = expression.replace(
            "previous.volume",
            "previous_volume"
        )
        #print("EXPRESSION:", expression)
        #print("VARIABLES:", variables)
        evaluator = SafeExpressionEvaluator(
            variables
        )

        return evaluator.evaluate(
            expression
        )
