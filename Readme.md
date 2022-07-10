# Problem description
Sports officials worldwide face incredible challenges due to the unfair means of practices performed by the athletes to improve their performance in the game. One of the methods is **sample swapping**. Some athletes try to swap their doped urine samples with their clean urine samples or from another individual to pass the doping test. The project aims to study the steroid profile and **develop a model based on graph networks** to detect the suspicious activities of athlete.

## Tasks
- [ ] Understanding the problem statement and the domain of steroid doping. &#8592;
- [ ] Developing a graph neural network model to detect the sample swapping cases. &#8592;
- [ ] Interpretation of the results.
- [ ] Developing a final prototype for the end-user.
- [ ] Bonus: Use the advantage of Quantum Networks in model development.


# How to get the data
1. Download the [data.xlsx](https://drive.google.com/drive/folders/1grn0BNDL4azKUvL-5whKiGLE49w5vUjH) file to the `data` directory.
1.  Install the required dependencied - the recommended package manager is [pipenv](https://pypi.org/project/pipenv/). If you have pipenv installed, you can run `pipenv install` and `pipenv shell` to run your shell in a virtual environment. In case of any problems with that feel free to use any other environment manager - the reuqired dependencies can be found in the `requirements.txt` file.
1. Add the following lines to your python notebook/script

```python
from src.data_preparation import DataPreprocessor

df = DataPreprocessor().get_dataframe()
```
`DataPreprocessor` class modifies the dataset columns - please use the column names described in the dataset decription below. 

# Dataset Description

| Field | Description |
| ------- | ------ |
| ~~ID_random~~ &#8594; **athlete_id** | the athlete identifier after swapping|
| **athlete_id_real** | the athlete identifier - ground truth |
| **sample_id** | the sample identifier|
| **swapped_with_sample_id** | identifier of sample with which the sample has been swapped |
| ~~is_swapped~~ | whether the athlete is swapped or not |
| **is_male** | True or False | 
| ~~SpecificGravity~~ &#8594; specific_gravity | the measured “density” of the urine sample, which is used to correct for differences in urine concentration due to factors such as hydration state. The SG is used to calculated the corrected concentrations of the steroid profile, denoted by “corr” below. |
| ~~In Comp~~ &#8594; **in_competition** | was the sample taken in competition or not (Y/N) |
| adiol | (ng/mL)  5αAdiol = 5α-Androstane-3α,17β-diol |
| bdiol | (ng/mL) 5βAdiol = 5β-Androstane-3α,17β-diol |
| androsterone | (ng/mL) Andro |
| etiocholanolone | (ng/mL) Etio |
| epitestosterone | (ng/mL) E |
| testosterone | (ng/mL) T |
| t_e_ratio |
| andro_t_ratio |
| andro_etio_ratio |
| adiol_bdiol_ratio |
| adiol_e_ratio |
| adiol_corr | (ng/mL) corrected by specific gravity |
| bdiol_corr | (ng/mL) corrected by specific gravity |
| androsterone_corr | (ng/mL) corrected by specific gravity |
| etiocholanolone_corr | (ng/mL) corrected by specific gravity |
| epitestosterone_corr | (ng/mL) corrected by specific gravity |
| testosterone_corr | (ng/mL) corrected by specific gravity |
| ~~ID_random~~ | a random athlete identifier |
| ~~Gender~~| M or F |
| ~~Total Observation~~ &#8594; **total_observations**| total number of samples collected for that particular athlete i.e. total no. of samples in the longitudinal steroid profile of that particular athlete |



We’ve provided both the measured and the specific gravity-corrected concentrations for the **6 steroids**, and each provides useful information. Overall, the corrected concentrations are more suitable for comparison to each other as they are normalized for differences in urine density caused by factors such as hydration state. The uncorrected concentrations, on the other hand, provide information on the potential effects of analytical variation, in the event that you may wish to incorporate analytical uncertainty into your model.

The formula for the correction using specific gravity is:

<img src="https://latex.codecogs.com/gif.latex?Conc_corr=Conc\_measured\cdot\frac{1.02-1}{SG-1}" />



You can also follow this literature to understand more about the data:
Van Renterghem, P., Van Eenoo, P., Geyer, H., Schänzer, W., & Delbeke, F. T. (2010). Reference ranges for urinary concentrations and ratios of endogenous steroids, which can be used as markers for steroid misuse, in a Caucasian population of athletes. Steroids, 75(2), 154–163. https://doi.org/10.1016/j.steroids.2009.11.008
 


 


#### Other DataPreprocessor usage example:
```python
from src.data_preparation import DataPreprocessor

df = DataPreprocessor(data_path='data/data.xlsx', swap_rate=0.01).get_dataframe()

raw_df = DataPreprocessor().get_raw_dataframe()
```

# How to generate the graph object

1. Split the data into train and test sets using the following command:
```
python src/generate_splits.py
```
If your excel datafile is not in './data' directory, you can specify the path using: `--datapath <path>`.

2. Generate train and test graphs:

This can be done in two ways-
* shuffled - An athelete in the test set may also be present in the training set (other samples of same athlete)
* mutually_exclusive - Athletes belonging to the test set are not included in the training set (default)

```python
from src.graph_data_loader import graph_loader

train_graph, test_graph = graph_loader() # uses mutually_exclusive setting
```
The default swap_rate is 0.01 and by default there are no edges between the clusters of atheletes having the same 'athelete_id' (no edges between swapped samples).

### To change the split_type, swap_rate, or get edges between the clusters, use:
```python
from src.graph_data_loader import graph_loader

train_graph, test_graph = graph_loader('shuffled', new_swap_rate, edge_bw_swapped=True)
```

Few examples of graph properties that can be viewed are provided in `GraphDataExp.ipynb`.

Each graph node represents 1 data sample. Each node contains the following features.
1. 'adiol'
2. 'adiol_bdiol_ratio' 
3. 'adiol_corr'
4. 'adiol_e_ratio'
5. 'andro_etio_ratio'
6. 'andro_t_ratio'
7. 'androsterone'
8. 'androsterone_corr'
9. 'bdiol'
10. 'bdiol_corr'
11. 'epitestosterone'
12. 'epitestosterone_corr'
13. 'etiocholanolone'
14. 'etiocholanolone_corr'
15. 'in_competition'
16. 'is_male'
17. 'specific_gravity'
18. 't_e_ratio'
19. 'testosterone'
20. 'testosterone_corr'

# How to use Train and Predict using PyGod Models

```python
from src.models import PyGod

model = PyGod(model_name, swap_rate)

model.train(train_graph)

train_outlier_scores = model.get_train_scores()

test_outlier_scores = model.predict(test_graph)
```

Valid Model Names: 'mlpae', 'gcnae', 'dominant', 'scan', 'radar', 'anomalous', 'one', 'done', 'adone', 'gaan', 'ocgnn'