# Ricardian Trade & Comparative Advantage Analyzer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Economics](https://img.shields.io/badge/Focus-Business%20Economics-success)
![Data Visualization](https://img.shields.io/badge/Data%20Visualization-Matplotlib-orange)

A lightweight, portfolio-ready Python analysis tool for applying **Ricardian trade theory** to practical business economics and international logistics scenarios.

## Overview & Business Context

Global supply chain strategy depends on efficient production specialization across regions. This project operationalizes comparative advantage by quantifying opportunity costs and identifying when two countries can both gain from trade.

Use it to support undergraduate analysis, classroom case studies, and portfolio demonstrations where theory is connected to modern sourcing and trade decisions.

## Features

- Typed, modular analysis workflow in `analyzer.py`
- Opportunity cost calculations for two goods and two countries
- Automatic comparative advantage assignment
- Mutually beneficial terms-of-trade range detection
- PPF (Production Possibility Frontier) visualization with:
  - labeled intercepts
  - annotated slopes
  - pre-trade country comparison
- Built-in default demo:
  - Spain: Sofas = 55, Radios = 73
  - Germany: Sofas = 133, Radios = 90

## Methodology

For each country:

- Opportunity cost of Good 1 in Good 2 units:
  \[
  OC_{G1} = \frac{G2}{G1}
  \]
- Opportunity cost of Good 2 in Good 1 units:
  \[
  OC_{G2} = \frac{G1}{G2}
  \]

Comparative advantage is assigned to the country with the **lower opportunity cost** for each good.

Mutually beneficial terms of trade for a good exist when the negotiated price falls strictly between the two countries' opportunity costs for that good.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run default demo:

```bash
python analyzer.py
```

Run with custom inputs:

```bash
python analyzer.py \
  --country-a "Country A" --country-b "Country B" \
  --good-1 "Sofas" --good-2 "Radios" \
  --a-good-1 55 --a-good-2 73 \
  --b-good-1 133 --b-good-2 90 \
  --plot-path ppf_pre_trade.png
```

## Sample Output & Analysis (Spain vs. Germany)

Expected opportunity costs (rounded to 2 decimals):

- Spain:
  - OC(Sofas) in Radios = 1.33
  - OC(Radios) in Sofas = 0.75
- Germany:
  - OC(Sofas) in Radios = 0.68
  - OC(Radios) in Sofas = 1.48

Comparative advantage:

- **Germany** in Sofas
- **Spain** in Radios

Mutually beneficial terms of trade:

- Sofas in Radios: `0.68 < price < 1.33`
- Radios in Sofas: `0.75 < price < 1.48`

The script also saves a visualization file (`ppf_pre_trade.png`) showing both countries' pre-trade PPFs.

## License

MIT License
