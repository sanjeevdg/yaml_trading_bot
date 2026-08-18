from copy import deepcopy

from optimizer.grid import GridSearch
from optimizer.result import OptimizationResult

from backtest.engine import BacktestEngine

from strategies.factory import StrategyFactory
from indicators.factory import IndicatorFactory
from indicators.engine import IndicatorEngine


class Optimizer:

    def __init__(self, strategy, config):

        self.strategy = strategy
        self.config = config

    # ---------------------------------------------------------
    # BUILD INDICATORS
    # ---------------------------------------------------------

    def build_indicators(self, params, dataframe):

        engine = IndicatorEngine()

        working_df = dataframe.copy()

        #
        # Find all EMA indicators.
        #
        # This lets us distinguish:
        #
        # EMA #1 -> fast
        # EMA #2 -> slow
        #
        # for ema_cross.
        #

        ema_indexes = []

        for index, indicator_cfg in enumerate(
            self.config.indicators
        ):

            cfg = indicator_cfg.model_dump(
                exclude_none=True
            )

            if cfg["type"].lower() == "ema":

                ema_indexes.append(index)

        #
        # Rebuild every indicator from YAML
        #

        for index, indicator_cfg in enumerate(
            self.config.indicators
        ):

            cfg = deepcopy(
                indicator_cfg.model_dump(
                    exclude_none=True
                )
            )

            indicator_type = cfg["type"].lower()

            parameters = cfg.setdefault(
                "parameters",
                {}
            )

            #
            # ---------------------------------------------
            # EMA
            # ---------------------------------------------
            #

            if indicator_type == "ema":

                #
                # A strategy such as ema_macd or ema_rsi
                # has one EMA controlled by "ema".
                #

                if "ema" in params:

                    parameters["period"] = params["ema"]

                #
                # ema_cross has two EMA indicators.
                #
                # First EMA = fast
                # Second EMA = slow
                #

                elif (
                    "fast" in params
                    and len(ema_indexes) >= 2
                ):

                    ema_position = ema_indexes.index(
                        index
                    )

                    if ema_position == 0:

                        parameters["period"] = (
                            params["fast"]
                        )

                    elif ema_position == 1:

                        parameters["period"] = (
                            params["slow"]
                        )

            #
            # ---------------------------------------------
            # RSI
            # ---------------------------------------------
            #

            elif indicator_type == "rsi":

                if "period" in params:

                    parameters["period"] = (
                        params["period"]
                    )

            #
            # ---------------------------------------------
            # MACD
            # ---------------------------------------------
            #

            elif indicator_type == "macd":

                if "fast" in params:

                    parameters["fast"] = (
                        params["fast"]
                    )

                if "slow" in params:

                    parameters["slow"] = (
                        params["slow"]
                    )

                if "signal" in params:

                    parameters["signal"] = (
                        params["signal"]
                    )

            #
            # ---------------------------------------------
            # Bollinger Bands
            # ---------------------------------------------
            #

            elif indicator_type == "bollinger":

                if "period" in params:

                    parameters["period"] = (
                        params["period"]
                    )

                if "stddev" in params:

                    parameters["stddev"] = (
                        params["stddev"]
                    )

            #
            # ---------------------------------------------
            # ATR
            # ---------------------------------------------
            #

            elif indicator_type == "atr":

                if "period" in params:

                    parameters["period"] = (
                        params["period"]
                    )

            #
            # ---------------------------------------------
            # SuperTrend
            # ---------------------------------------------
            #

            elif indicator_type == "supertrend":

                if "period" in params:

                    parameters["period"] = (
                        params["period"]
                    )

                if "multiplier" in params:

                    parameters["multiplier"] = (
                        params["multiplier"]
                    )

            #
            # Build indicator through factory
            #

            indicator = IndicatorFactory.create(
                cfg
            )

            engine.add(indicator)

        #
        # Apply all indicators to a fresh dataframe
        #

        return engine.apply(
            working_df
        )

    # ---------------------------------------------------------
    # BUILD PARAMETER GRID
    # ---------------------------------------------------------

    def build_parameter_grid(self):

        optimize = (
            self.config.optimize
            or {}
        )

        parameter_grid = {}

        for name, values in optimize.items():

            parameter_grid[name] = range(
                values["start"],
                values["stop"] + 1,
                values["step"]
            )

        return parameter_grid

    # ---------------------------------------------------------
    # RUN OPTIMIZATION
    # ---------------------------------------------------------

    def run(self, dataframe):

        parameter_grid = (
            self.build_parameter_grid()
        )

        #
        # If there is nothing to optimize,
        # still run exactly one combination.
        #

        combinations = GridSearch.build(
            parameter_grid
        )

        results = []

        count = 0

        for params in combinations:

            count += 1

            if count % 100 == 0:

                print(
                    f"Completed "
                    f"{count} combinations..."
                )

            #
            # ---------------------------------------------
            # Clone strategy configuration
            # ---------------------------------------------
            #

            strategy_cfg = deepcopy(
                self.config.strategy
            )

            #
            # Make sure parameters exists
            #

            if strategy_cfg.parameters is None:

                strategy_cfg.parameters = {}

            #
            # Apply optimized parameters
            #

            strategy_cfg.parameters.update(
                params
            )

            #
            # Create strategy from YAML
            #

            strategy = StrategyFactory.create(
                strategy_cfg
            )

            #
            # ---------------------------------------------
            # Rebuild indicators
            # ---------------------------------------------
            #

            working_df = self.build_indicators(
                params,
                dataframe
            )

            #
            # ---------------------------------------------
            # Backtest
            # ---------------------------------------------
            #

            result = BacktestEngine(
                strategy=strategy,cfg=self.config
            ).run(working_df)

            trades = result["trades"]
            metrics = result["metrics"]

            

            #
            # ---------------------------------------------
            # Save result
            # ---------------------------------------------
            #

            results.append(
                OptimizationResult(

                    parameters=params,

                    trades=metrics["trades"],

                    wins=metrics["wins"],

                    losses=metrics["losses"],

                    net_profit=metrics["net_profit"],

                    win_rate=metrics["win_rate"],

                    profit_factor=metrics["profit_factor"]

                )
            )

        #
        # Best results first
        #

        return sorted(
            results,
            key=lambda result: result.net_profit,
            reverse=True
        )