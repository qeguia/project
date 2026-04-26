# Housing Affordability Analysis in Europe

---

## Description

This project analyses housing affordability across European countries using real-world data from:

* **Eurostat API** (European data)
* **INE API** (Spanish national data)

The objective is to understand how housing prices evolve and compare affordability between countries and regions using data science and statistical methods.

The project integrates:

* Data collection from APIs
* Data cleaning and transformation
* Comparative analysis
* Visualisation
* A statistical scoring model

---

## Key Features:

* Real-time data from APIs
* Data cleaning and preprocessing pipelines
* Country comparison (e.g. Spain vs Portugal)
* Spain vs EU average analysis
* Data visualisation (trend plots and bar charts)
* Statistical scoring model
* Command-line interface (CLI)
* Test Driven Development (TDD)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/qeguia/project.git
cd project
```

### 2. Create the environemnt using the .yml file

```bash
conda env create -f environment.yml
```

### 3. Activate the environemnt
```bash
conda activate project
```

---

## Usage

The project is executed from the command line.

### Eurostat analysis:

```bash
python main_eurostat.py
```

### Country comparison:

```bash
python main_eurostat.py --country1 ES --country2 PT
```

### INE analysis (Spain regions)

```bash
python main_ine.py
```

---

## Data Pipeline

```
API → Raw Data → Cleaning → Transformation → Analysis → Visualization
```

### Example pipeline:

```python
raw = load_eurostat_data()
clean = clean_eurostat_data(raw)
df_long = prepare_hpi_long(clean)
```

---

## Analysis

### Spain vs EU:

```python
df_plot = build_spain_vs_eu_dataset(eurostat_long)
```

### Country comparison:

```python
df_plot = build_country_comparison_dataset(
    eurostat_long,
    "ES",
    "PT"
)
```

---

## Visualisation

### Example plot

```python
p = plot_country_comparison(df_plot, "ES", "PT")
p.show()
```

### INE regional analysis

```python
ggplot(clean_ine, aes(x='region', y='value', fill='dwelling'))
```
---

## Example Output

ADD SCREENSHOTS HERE

---

## Statistical Model

The project includes a scoring function to evaluate country performance:

S_i = \alpha P_i + (1 - \alpha) \frac{A_i}{\max(A)}

Where:

* ( P_i ): probability of outperforming other countries
* ( A_i ): risk-adjusted return
* ( \alpha ): weighting parameter (default = 0.7)

### Example:

```python
from mainstats import compute_final_scores

P = [0.6, 0.7, 0.8]
A = [100, 120, 90]

scores = compute_final_scores(P, A)
print(scores)
```

---

## Project Structure

```
project/
│── src/
    │──  analysis/
        │── __init__.py
        │── analysis.py
    │── data_cleaning/
        │── __init__.py
        │── cleaning.py
    │──  plot/
        │── main.py
        │── main_eurostat.py
        │── main_ine.py
        │── mainstats.py
        │── banner.py
│── tests/
    │── __init__.py
    │── test_core.py
    │── test_edge_cases.py
    │── test_imports.py
│── docs/
│── .gitignore
│── README.md
│── environment.yml
│── setup.py
```

---

## Testing

Run all tests:

```bash
pytest
```

Tests cover:

* Data cleaning
* Analysis functions
* Error handling
* Edge cases

---

## Technologies:

* Python
* Pandas
* NumPy
* Plotnine / Matplotlib
* Eurostat API
* INE API (ineapy)
* Pytest
* Sphinx (documentation)

---

## Contributing:

* Use feature branches
* Write clear commit messages
* Open pull requests

---

## Versioning:

Git is used with multiple branches for:

* Feature development
* Testing
* Integration

---

## License:

Academic project for **Computer Programming II and Probability**.

