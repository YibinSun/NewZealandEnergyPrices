# New Zealand Energy Prices Datasets

This project aims to abstract data from the [Electricity Market Information website][link] for data stream regression, anomaly detection, and time-series tasks.

[link]:https://www.emi.ea.govt.nz/
New Zealand introduced the real-time electricity pricing system on 1 November 2022, replacing the old ex-post final prices system. This results in a new price series -- [Dispatch Energy Prices][dispatch]. 

[dispatch]:https://www.emi.ea.govt.nz/Wholesale/Datasets/DispatchAndPricing/DispatchEnergyPrices
The data is fully and publicly accessible and updated daily. Although other types of data are also provided on the website, this project focuses only on the Dispatch Energy Prices.

This project provides an approach to download data within a desired period and preprocess it into learnable datasets.

## Preprocess and Simple Analysis

The code in the `end_to_end_process.ipynb` file provides the entire procedure:
1. Download full data
2. Create datasets based on the full data by different requests
3. Apply simple data stream analysis and algorithms
   - Regression
   - Prediction Interval
   - Drift analysis

## Multiple Datasets Generation

`datasets_from_multiple_PoCs.ipynb` provides an integrated function to generate datasets from different Points of Connection (PoCs), periods, and target delays.
Example regression datasets can be found in the `datasets` repository, generated by the code in `datasets_from_multiple_PoCs.ipynb`.
Users can easily create datasets for specific locations and periods with minor changes to the code.

## Anomaly Detection Analysis

While analyzing the obtained datasets, we found that the energy price, although rare, can become extremely high.
Therefore, we extended the project with anomaly detection analysis.

In `anomaly_detection_related.ipynb`, functions to convert the regression datasets to anomaly datasets are defined, followed by an experiment with the Half-Space Trees algorithm.
This requires further investigation concerning the current status.

## Fetch All Data

If you are intended to fetch all data, you can try the `fetch_all_data.py` or `parallel_fetch.py` scripts.
These will try to retrieve all data from the website in parallel, saving some time.

## Cite Us

If you use the code or data in this project, please cite us:

```
@inproceedings{sun2024real,
  title={Real-Time Energy Pricing in New Zealand: An Evolving Stream Analysis},
  author={Sun, Yibin and Gomes, Heitor Murilo and Pfahringer, Bernhard and Bifet, Albert},
  booktitle={Pacific Rim International Conference on Artificial Intelligence},
  pages={91--97},
  year={2024},
  organization={Springer}
}
```