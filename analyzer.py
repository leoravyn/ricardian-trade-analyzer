from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class CountryProduction:
    name: str
    good_1: float
    good_2: float

    def __post_init__(self) -> None:
        if self.good_1 <= 0 or self.good_2 <= 0:
            raise ValueError(f"{self.name} production values must be greater than zero.")


@dataclass(frozen=True)
class OpportunityCosts:
    good_1_in_good_2: float
    good_2_in_good_1: float


def calculate_opportunity_costs(country: CountryProduction) -> OpportunityCosts:
    return OpportunityCosts(
        good_1_in_good_2=country.good_2 / country.good_1,
        good_2_in_good_1=country.good_1 / country.good_2,
    )


def determine_comparative_advantage(
    country_a: CountryProduction,
    country_b: CountryProduction,
    costs_a: OpportunityCosts,
    costs_b: OpportunityCosts,
    good_1_name: str,
    good_2_name: str,
) -> Dict[str, str]:
    advantages: Dict[str, str] = {}

    if costs_a.good_1_in_good_2 < costs_b.good_1_in_good_2:
        advantages[good_1_name] = country_a.name
    elif costs_b.good_1_in_good_2 < costs_a.good_1_in_good_2:
        advantages[good_1_name] = country_b.name
    else:
        advantages[good_1_name] = "Tie"

    if costs_a.good_2_in_good_1 < costs_b.good_2_in_good_1:
        advantages[good_2_name] = country_a.name
    elif costs_b.good_2_in_good_1 < costs_a.good_2_in_good_1:
        advantages[good_2_name] = country_b.name
    else:
        advantages[good_2_name] = "Tie"

    return advantages


def mutually_beneficial_terms(
    country_a: CountryProduction,
    country_b: CountryProduction,
    costs_a: OpportunityCosts,
    costs_b: OpportunityCosts,
    good_1_name: str,
    good_2_name: str,
) -> Dict[str, str]:
    advantages = determine_comparative_advantage(
        country_a, country_b, costs_a, costs_b, good_1_name, good_2_name
    )

    if advantages[good_1_name] == "Tie" or advantages[good_2_name] == "Tie":
        return {"status": "No mutually beneficial range due to equal opportunity costs."}

    if advantages[good_1_name] == advantages[good_2_name]:
        return {
            "status": (
                "No mutually beneficial trade range because one country has comparative "
                "advantage in both goods."
            )
        }

    exporter_good_1 = country_a if advantages[good_1_name] == country_a.name else country_b
    importer_good_1 = country_b if exporter_good_1 == country_a else country_a

    exporter_cost_good_1 = (
        costs_a.good_1_in_good_2 if exporter_good_1 == country_a else costs_b.good_1_in_good_2
    )
    importer_cost_good_1 = (
        costs_b.good_1_in_good_2 if importer_good_1 == country_b else costs_a.good_1_in_good_2
    )

    exporter_cost_good_2 = (
        costs_a.good_2_in_good_1 if advantages[good_2_name] == country_a.name else costs_b.good_2_in_good_1
    )
    importer_cost_good_2 = (
        costs_b.good_2_in_good_1 if advantages[good_2_name] == country_a.name else costs_a.good_2_in_good_1
    )

    return {
        "status": "Mutually beneficial range exists.",
        f"{good_1_name} in terms of {good_2_name}": (
            f"{exporter_cost_good_1:.2f} < price < {importer_cost_good_1:.2f}"
        ),
        f"{good_2_name} in terms of {good_1_name}": (
            f"{exporter_cost_good_2:.2f} < price < {importer_cost_good_2:.2f}"
        ),
        "note": f"{exporter_good_1.name} should export {good_1_name}; {importer_good_1.name} should export {good_2_name}.",
    }


def create_ppf_plot(
    country_a: CountryProduction,
    country_b: CountryProduction,
    good_1_name: str,
    good_2_name: str,
    output_path: Path,
) -> None:
    try:
        x_a = np.linspace(0, country_a.good_1, 100)
        y_a = country_a.good_2 - (country_a.good_2 / country_a.good_1) * x_a

        x_b = np.linspace(0, country_b.good_1, 100)
        y_b = country_b.good_2 - (country_b.good_2 / country_b.good_1) * x_b

        plt.figure(figsize=(10, 6))
        plt.plot(x_a, y_a, label=f"{country_a.name} PPF", linewidth=2)
        plt.plot(x_b, y_b, label=f"{country_b.name} PPF", linewidth=2)

        plt.scatter([country_a.good_1, 0], [0, country_a.good_2], s=45)
        plt.scatter([country_b.good_1, 0], [0, country_b.good_2], s=45)

        plt.annotate(f"{country_a.name}: ({country_a.good_1:.0f}, 0)", (country_a.good_1, 0), xytext=(8, 8), textcoords="offset points")
        plt.annotate(f"{country_a.name}: (0, {country_a.good_2:.0f})", (0, country_a.good_2), xytext=(8, 8), textcoords="offset points")
        plt.annotate(f"{country_b.name}: ({country_b.good_1:.0f}, 0)", (country_b.good_1, 0), xytext=(8, -14), textcoords="offset points")
        plt.annotate(f"{country_b.name}: (0, {country_b.good_2:.0f})", (0, country_b.good_2), xytext=(8, -14), textcoords="offset points")

        plt.text(
            country_a.good_1 * 0.50,
            country_a.good_2 * 0.35,
            f"{country_a.name} slope: {-country_a.good_2 / country_a.good_1:.2f}",
        )
        plt.text(
            country_b.good_1 * 0.50,
            country_b.good_2 * 0.75,
            f"{country_b.name} slope: {-country_b.good_2 / country_b.good_1:.2f}",
        )

        plt.title("Production Possibility Frontiers (Pre-Trade)")
        plt.xlabel(f"{good_1_name} per worker/day")
        plt.ylabel(f"{good_2_name} per worker/day")
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
        plt.close()
    except Exception as error:  # pragma: no cover - plotting backend failures are environment-specific
        raise RuntimeError(f"Failed to generate PPF plot: {error}") from error


def build_results_table(
    country_a: CountryProduction,
    country_b: CountryProduction,
    costs_a: OpportunityCosts,
    costs_b: OpportunityCosts,
    good_1_name: str,
    good_2_name: str,
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Country": [country_a.name, country_b.name],
            f"OC({good_1_name}) in {good_2_name}": [
                round(costs_a.good_1_in_good_2, 2),
                round(costs_b.good_1_in_good_2, 2),
            ],
            f"OC({good_2_name}) in {good_1_name}": [
                round(costs_a.good_2_in_good_1, 2),
                round(costs_b.good_2_in_good_1, 2),
            ],
        }
    )


def run_analysis(
    country_a: CountryProduction,
    country_b: CountryProduction,
    good_1_name: str,
    good_2_name: str,
    output_plot_path: Path,
) -> Tuple[pd.DataFrame, Dict[str, str], Dict[str, str]]:
    costs_a = calculate_opportunity_costs(country_a)
    costs_b = calculate_opportunity_costs(country_b)

    results_table = build_results_table(country_a, country_b, costs_a, costs_b, good_1_name, good_2_name)
    advantages = determine_comparative_advantage(
        country_a, country_b, costs_a, costs_b, good_1_name, good_2_name
    )
    terms = mutually_beneficial_terms(
        country_a, country_b, costs_a, costs_b, good_1_name, good_2_name
    )

    create_ppf_plot(country_a, country_b, good_1_name, good_2_name, output_plot_path)

    return results_table, advantages, terms


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ricardian Trade & Comparative Advantage Analyzer"
    )
    parser.add_argument("--country-a", default="Spain", help="Name of country/region A")
    parser.add_argument("--country-b", default="Germany", help="Name of country/region B")
    parser.add_argument("--good-1", default="Sofas", help="Name of good 1")
    parser.add_argument("--good-2", default="Radios", help="Name of good 2")
    parser.add_argument("--a-good-1", type=float, default=55, help="Country A output of good 1")
    parser.add_argument("--a-good-2", type=float, default=73, help="Country A output of good 2")
    parser.add_argument("--b-good-1", type=float, default=133, help="Country B output of good 1")
    parser.add_argument("--b-good-2", type=float, default=90, help="Country B output of good 2")
    parser.add_argument(
        "--plot-path",
        default="ppf_pre_trade.png",
        help="File path for saved PPF chart",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        country_a = CountryProduction(args.country_a, args.a_good_1, args.a_good_2)
        country_b = CountryProduction(args.country_b, args.b_good_1, args.b_good_2)

        results, advantages, terms = run_analysis(
            country_a,
            country_b,
            args.good_1,
            args.good_2,
            Path(args.plot_path),
        )

        print("\nRicardian Trade & Comparative Advantage Analyzer\n")
        print("Opportunity Costs (rounded to 2 decimals):")
        print(results.to_string(index=False))

        print("\nComparative Advantage:")
        for good, country in advantages.items():
            print(f"- {good}: {country}")

        print("\nMutually Beneficial Terms of Trade:")
        for key, value in terms.items():
            print(f"- {key}: {value}")

        print(f"\nPPF chart saved to: {Path(args.plot_path).resolve()}")
    except ValueError as error:
        raise SystemExit(f"Input error: {error}")
    except RuntimeError as error:
        raise SystemExit(f"Plot error: {error}")


if __name__ == "__main__":
    main()
