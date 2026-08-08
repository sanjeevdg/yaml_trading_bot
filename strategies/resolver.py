class IndicatorValueResolver:

    MARKET_COLUMNS = {
        "open",
        "high",
        "low",
        "close",
        "volume",
        "trade_count",
        "vwap",
    }

    @staticmethod
    def resolve(
        name,
        current,
        previous=None,
        parameters=None
    ):

        parameters = parameters or {}

        #
        # Numeric values
        #

        if isinstance(name, (int, float)):
            return float(name)

        #
        # Strategy parameters
        #

        if name in parameters:
            return float(parameters[name])

        #
        # Previous candle
        #

        if isinstance(name, str) and name.startswith("previous."):

            if previous is None:
                raise ValueError(
                    "Previous candle is not available"
                )

            column = name.split(".", 1)[1]

            if column not in previous.index:
                raise ValueError(
                    f"Unknown previous column: {column}"
                )

            return float(previous[column])

        #
        # Indicator aliases
        #

        alias_value = IndicatorValueResolver.resolve_alias(
            name,
            current
        )

        if alias_value is not None:
            return alias_value

        #
        # Direct DataFrame column
        #

        if name in current.index:
            return float(current[name])

        #
        # Parameterised indicator names
        #

        if isinstance(name, str):

            resolved_name = name

            for key, value in parameters.items():

                resolved_name = resolved_name.replace(
                    f"{{{key}}}",
                    str(value)
                )

            if resolved_name in current.index:
                return float(
                    current[resolved_name]
                )

        #
        # Numeric string
        #

        try:
            return float(name)

        except (TypeError, ValueError):
            pass

        raise ValueError(
            f"Unable to resolve value: {name}"
        )

    @staticmethod
    def resolve_alias(name, current):

        aliases = {
            "macd": "MACD",
            "macd_signal": "MACD_SIGNAL",
            "macd_hist": "MACD_HIST",
            "atr": "ATR",
            "supertrend": "SUPERTREND",
            "supertrend_direction": "SUPERTREND_DIRECTION",
            "bb_upper": "BB_UPPER",
            "bb_middle": "BB_MIDDLE",
            "bb_lower": "BB_LOWER",
        }

        key = name.lower()

        column = aliases.get(
            key,
            name
        )

        if column in current.index:
            return float(current[column])

        return None    