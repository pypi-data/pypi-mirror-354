# Sports Prediction Framework

A modular and extensible machine learning framework for predicting sports outcomes and evaluating betting strategies.

This framework enables seamless data ingestion, model training, prediction, and betting simulation for sports analytics. Designed for research, experimentation, and scalable deployment, it supports tabular and graph-based models, MLflow logging, and sophisticated evaluation tools.


> ⚠️ **Heads Up!**  
> Looking for **detailed documentation**, examples, and deeper insights?  
> 👉 Check out the full guide here: [📚 Full Documentation](https://vetrope2.github.io/sports_prediction_framework/)

## Table of Contents
- [Overview](#overview)
- [Modules](#modules)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Using Database Data in the Framework](#using-database-data-in-the-framework)
- [Self-Contained Demonstration](#self-contained-demonstration)
- [Commented Workflow](#commented-workflow)
- [Evaluation Metrics](#-evaluation-metrics)
- [Full Documentation](https://vetrope2.github.io/sports_prediction_framework/)



---

## Overview

This framework provides a comprehensive pipeline for sports prediction, including:

- **Data Loading & Parsing:** Flexible connectors and parsers to ingest and preprocess sports data from multiple sources.
- **Data Wrappers:** Clean abstractions over raw data for various sports and competitions, supporting feature extraction and label management.
- **Modeling:** Support for diverse predictive models, including flat and graph neural network architectures.
- **Training & Evaluation:** Learner, trainer, and tester components streamline the training process and enable robust model evaluation.
- **Simulation & Betting Strategies:** Implementations of multiple betting simulations to assess strategy performance using historical match data.
- **Optimization:** Integration with hyperparameter optimization tools to fine-tune model performance.
- **Data Transformation & Scoping:** Powerful mechanisms to segment and iterate over datasets for temporal or categorical analysis.

---

## Modules

- `dataloader`: Handles data ingestion and parsing.
- `datawrapper`: Wraps raw data into usable formats per sport.
- `model`: Contains model definitions and training logic.
- `learner`: Coordinates training and evaluation.
- `simulation`: Betting strategies and evaluation methods.
- `transformer`: Tools for data segmentation and transformation.
- `optimizer`: Hyperparameter tuning support.
- `utils`: Utility functions and helpers.

---

## Installation

Install the framework locally from the folder:

```bash
pip install .
```

Install from pypi:
```bash
pip install sports-prediction-framework
```

## Getting Started

Welcome to the framework! There are two main ways to get started depending on your setup and needs:

### 1. Connect to a Database

If you want to work with your own or a remote database, make sure to configure your environment by creating a `.env` file in your current working directory. This file should include your database credentials and, if necessary, SSH tunnel settings.

> See [Database Configuration](#using-database-data-in-the-framework) for detailed instructions.

### 2. Use the Self-Contained Examples

If you prefer a quick start without needing database access, you can explore our self-contained demonstrations. These run in Google Colab and use the sample data provided in the `examples` directory (`data.parquet`).

> Check out the [Examples and Demos](#self-contained-demonstration) to open the notebooks directly.

---

Feel free to choose the option that best fits your workflow. If you’re new, we recommend starting with the examples for a smooth introduction!


## Using Database Data in the Framework

To use data from a database within the framework, you **must** have a `.env` file located in your current working directory. This file should contain the necessary configuration variables for database connection.

### Required `.env` Variables

Below is an example of the essential variables your `.env` file should include:


```env
DB_HOST=your_db_host
DB_PORT=your_db_port
DB_NAME=your_db_name
DB_USER=your_db_username
DB_PASSWORD=your_db_password
```

> **⚠️ Warning:**  
> The following SSH-related variables are **only required** if you are connecting to the database via an SSH tunnel.


```env
SSH_HOST=ssh_server
SSH_USER=ssh_user
SSH_KEY_PATH=path_to_your_key
```


## Self-Contained Demonstration

We provide a self-contained demonstration that does **not** require any database access. This makes it easy to explore and test the framework without setting up a database connection.

The demonstration runs in **Google Colab** and uses the `data.parquet` file located in the `examples` directory of the repository.



You can open and run the notebooks directly via the following links:

- [Flat Model](https://colab.research.google.com/drive/1cvTSVJl9IKZ5zetAArQoUHMiGpkao_N1?usp=sharing)

- [Other Flat](https://colab.research.google.com/drive/1s_RPveoUixcFV2rnhW3lM3VRf8ynknlg?usp=sharing)

- [Model Evaluation](https://colab.research.google.com/drive/1h-C7imynYpMc1OvjwBnfxgcU2mvczJsb?usp=sharing)

- [Optimization](https://colab.research.google.com/drive/1PDxtwabuDKNq8BPbRyAJmk8nsWcuTvUy?usp=sharing)

- [Simulation example](https://colab.research.google.com/drive/18KNe19nwtR_dQaZLlF6deUjtP77b12B9?usp=sharing)

Feel free to explore these notebooks to get a hands-on understanding of the framework using real data samples.


### Example of `data.parquet` Content 

| Date       | Home          | Away           | HS | AS | WDL | odds_1 | odds_X | odds_2 |
|------------|---------------|----------------|----|----|-----|--------|--------|--------|
| 2004-01-21 | Bayern Munich | Hamburger SV   | 3  | 0  | 1   | 1.39   | 4.00   | 6.50   |
| 2004-01-22 | Wolfsburg     | Dortmund       | 1  | 2  | 2   | 1.83   | 3.25   | 3.75   |
| 2004-01-22 | Nurnberg      | Kaiserslautern | 1  | 3  | 2   | 2.10   | 3.25   | 3.00   |
| 2004-01-22 | Nurnberg      | Kaiserslautern | 1  | 3  | 2   | 2.00   | —      | 3.25   |
| 2004-01-22 | Mainz         | Stuttgart      | 2  | 3  | 2   | 2.79   | 3.25   | 2.20   |

> **Note:** This is a small excerpt of the `data.parquet` file. The actual dataset contains many more rows and columns with additional information.

---
## Commented Workflow

### 1. Load Bundesliga Data Including Bookmaker Odds (bet365)

In this step, we load Bundesliga match data filtered by league name and including bookmaker odds from "bet365". The data is wrapped for convenient use within the framework.

This method **shields the user from having to manually connect to a database or parse raw data based on the database format**. It returns a ready-to-use wrapped dataset for downstream tasks.
```python
# Load Bundesliga football match data with bet365 bookmaker odds
dw = DataLoader.load_and_wrap_odds(
    "football",
    "Matches",
    lambda c: c.League == "Bundesliga",
    SportType.FOOTBALL,
    bookmaker="bet365"
)
```

 
#### Excerpt of loaded data

| Date       | Home          | Away           | HS | AS | WDL | odds_1 | odds_X | odds_2 |
|------------|---------------|----------------|----|----|-----|--------|--------|--------|
| 2004-01-21 | Bayern Munich | Hamburger SV   | 3  | 0  | 1   | 1.39   | 4.00   | 6.50   |
| 2004-01-22 | Wolfsburg     | Dortmund       | 1  | 2  | 2   | 1.83   | 3.25   | 3.75   |
| 2004-01-22 | Nurnberg      | Kaiserslautern | 1  | 3  | 2   | 2.10   | 3.25   | 3.00   |
| 2004-01-22 | Nurnberg      | Kaiserslautern | 1  | 3  | 2   | 2.00   | —      | 3.25   |
| 2004-01-22 | Mainz         | Stuttgart      | 2  | 3  | 2   | 2.79   | 3.25   | 2.20   |


### 2. Apply Basic Transformations

In this step, we apply standard preprocessing transformations to the wrapped data using the framework’s `Transformer` class.

This step ensures that the raw data is cleaned and standardized for modeling. Transformations may include parsing dates, encoding categorical variables, or formatting numerical features.

```python
from sports_prediction_framework.transformer.Transformer import *
#Applies basic transformations to the dataframe.
t = Transformer()
dw = t.transform(dw)
print(dw)
```

By default, this transformation adds unique numeric identifiers for each team (Team ID columns), which are often used in embedding-based models.

#### Sample of Transformed Match Data

| Date       | Home           | Away            | HID | AID | HS | AS | WDL | odds_1 | odds_X | odds_2 |
|------------|----------------|------------------|-----|-----|----|----|-----|--------|--------|--------|
| 2004-01-21 | Bayern Munich  | Hamburger SV     |  5  | 17  |  3 |  0 |  1  |  1.39  |  4.00  |  6.50  |
| 2004-01-22 | Wolfsburg      | Dortmund         | 35  |  9  |  1 |  2 |  2  |  1.83  |  3.25  |  3.75  |
| 2004-01-22 | Nurnberg       | Kaiserslautern   | 27  | 24  |  1 |  3 |  2  |  2.10  |  3.25  |  3.00  |
| 2004-01-22 | Nurnberg       | Kaiserslautern   | 27  | 24  |  1 |  3 |  2  |  2.00  |   —    |  3.25  |
| 2004-01-22 | Mainz          | Stuttgart        | 26  | 32  |  2 |  3 |  2  |  2.79  |  3.25  |  2.20  |

> *Note: This is only a small sample of the available data. The full dataset contains additional rows and possibly other columns. Missing values are represented as em dashes (—).*

### 3. Define Training and Prediction Scopes

Before training, we define the scopes that determine which parts of the data will be used for training (relevant scope) and prediction (prediction scope). 

In this example, both scopes are created using `WindowSelector` combined with `ScopeExpander`, which slices the data by the 'Season' column, selecting windows starting from 2004 up to 2008 with a size of 1 season and a stride of 2 seasons.

The `DataSelector` then combines these scopes, managing the data segmentation for iterative training and testing.

```python
from sports_prediction_framework.transformer.Scope import *
from sports_prediction_framework.transformer.DataSelector import *

relevant_scope = [WindowSelector(ScopeExpander(dw, {
    'col': 'Season', 'start': 2004, 'max': 2008, 'size': 1, 'stride': 2
}))]
prediction_scope = [WindowSelector(ScopeExpander(dw, {
    'col': 'Season', 'start': 2004, 'max': 2008, 'size': 1, 'stride': 2
}))]
scope = DataSelector(relevant_scope, prediction_scope)
```

 

### 4. Create Model and Setup Learner

Next, we instantiate a `FlatModel` with chosen parameters and configure a `Learner` and an `UpdatingLearner` to manage the training and evaluation process over the defined data scopes.

The `UpdatingLearner` supports iterative updates by coordinating one or more nested learners, enabling flexible training workflows.

```python
from sports_prediction_framework.model.FlatModel import FlatModel
from sports_prediction_framework.learner.Learner import Learner, UpdatingLearner, Tester, Trainer

params = {
    'embed_dim': 32,
    'out_dim': 3,
    'n_dense': 4,
    'dense_dim': 64,
    'architecture_type': 'rectangle',
    'batch_size': 64,
}
flat = FlatModel(params)

#Setup learner and updating learner
l1 = Learner(Trainer(flat), Tester(flat), scope)
l = UpdatingLearner(Trainer(flat), Tester(flat), scope, [l1])
```

### 5. Generate Predictions

After training, we use the learner to compute predictions on the dataset. The predicted probabilities for each outcome are stored in columns labeled `0`, `1`, and `2`.

This allows you to easily access the model’s confidence for each class or outcome.

```python
prob = l.compute(dw)
#Predictions stored in 0,1,2 columns.
print(prob)
```

#### Example Output

| Date       | Home          | Away          | HID | AID | HS | AS | WDL | odds_1 | odds_X | odds_2 | 1        | 0        | 2        |
|------------|---------------|---------------|-----|-----|----|----|-----|--------|--------|--------|----------|----------|----------|
| 2004-01-21 | Bayern Munich | Hamburger SV  | 5   | 17  | 3  | 0  | 1   | 1.39   | 4.00   | 6.50   | 0.596798 | 0.201601 | 0.201601 |
| 2004-01-22 | Wolfsburg     | Dortmund      | 35  | 9   | 1  | 2  | 2   | 1.83   | 3.25   | 3.75   | 0.174244 | 0.340452 | 0.485304 |
| 2004-01-22 | Nurnberg      | Kaiserslautern| 27  | 24  | 1  | 3  | 2   | 2.10   | 3.25   | 3.00   | 0.082314 | 0.082314 | 0.835371 |
| 2004-01-22 | Nurnberg      | Kaiserslautern| 27  | 24  | 1  | 3  | 2   | 2.00   |        | 3.25   | 0.082314 | 0.082314 | 0.835371 |
| 2004-01-22 | Mainz         | Stuttgart     | 26  | 32  | 2  | 3  | 2   | 2.79   | 3.25   | 2.20   | 0.031287 | 0.031287 | 0.937426 |


## 📈 Evaluation Metrics

The framework supports multiple evaluation metrics to assess the performance of predictive models across different tasks and objectives:

| Metric        | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| **Accuracy**  | Measures the proportion of correct predictions among all predictions.       |
| **Precision** | Evaluates the number of true positives out of all predicted positives.      |
| **Recall**    | Measures the number of true positives out of all actual positives.          |
| **F1 Score**  | Harmonic mean of Precision and Recall, balancing false positives and false negatives. |
| **Brier Score** | Quantifies the accuracy of probabilistic predictions (lower is better).    |
| **RPS**       | Ranked Probability Score — evaluates the quality of multi-class probabilistic forecasts. |

