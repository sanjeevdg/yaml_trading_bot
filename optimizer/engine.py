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

    def build_indicators(self, params, dataframe):

        engine = IndicatorEngine()

        working_df = dataframe.copy()

        #
        # Rebuild every indicator from YAML
        #

        for indicator_cfg in self.config.indicators:

            cfg = deepcopy(
                indicator_cfg.model_dump(exclude_none=True)
            )

            p = cfg.setdefault("parameters", {})

            #print("PARAMS :", params)
            #print("BEFORE:", cfg)

            #
            # Override optimized values
            #

            indicator_type = cfg["type"].lower()

            if indicator_type == "ema":

                if "ema" in params:
                    p["period"] = params["ema"]

                elif "fast" in params and p.get("period") == 10:
                    p["period"] = params["fast"]

                elif "slow" in params and p.get("period") == 20:
                    p["period"] = params["slow"]

            elif indicator_type == "rsi":

                if "period" in params:
                    p["period"] = params["period"]

            elif indicator_type == "macd":

                if "fast" in params:
                    p["fast"] = params["fast"]

                if "slow" in params:
                    p["slow"] = params["slow"]

                if "signal" in params:
                    p["signal"] = params["signal"]

            elif indicator_type == "bollinger":

                if "period" in params:
                    p["period"] = params["period"]

                if "stddev" in params:
                    p["stddev"] = params["stddev"]

            elif indicator_type == "atr":

                if "period" in params:
                    p["period"] = params["period"]

            #
            # Let the factory build the indicator
            #
            #print(cfg)
            engine.add(
                IndicatorFactory.create(cfg)
            )

        return engine.apply(working_df)

    def run(self, dataframe):

        optimize = self.config.strategy.optimize

        parameter_grid = {}

        for name, values in optimize.items():

            parameter_grid[name] = range(
                values["start"],
                values["stop"] + 1,
                values["step"]
            )

        results = []
        count = 0
        for params in GridSearch.build(parameter_grid):

            #
            # Create strategy
            #
            count += 1

            if count % 100 == 0:
                print(f"Completed {count} combinations...")
            strategy_cfg = deepcopy(self.config.strategy)

            strategy_cfg.parameters.update(params)

            strategy = StrategyFactory.create(strategy_cfg)

            #
            # Rebuild indicators
            #
            #print(params)
            working_df = self.build_indicators(
                params,
                dataframe
            )

            #
            # Run backtest
            #

            trades = BacktestEngine(
                strategy=strategy
            ).run(working_df)

            wins = sum(t.pnl > 0 for t in trades)
            losses = len(trades) - wins
            net = sum(t.pnl for t in trades)

            results.append(

                OptimizationResult(

                    parameters=params,

                    trades=len(trades),

                    wins=wins,

                    losses=losses,

                    net_profit=net,

                    win_rate=(
                        100 * wins / len(trades)
                        if trades else 0
                    ),

                    profit_factor=0
                )

            )

        return sorted(
            results,
            key=lambda r: r.net_profit,
            reverse=True
        )