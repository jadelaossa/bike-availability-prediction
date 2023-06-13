# From the basic features configuration, creates a rich right input for the trained model.
# Pipeline:
# 1. tweak_bicing -> merges the data tables
# 2. Feature transformation (outputs a .pkl file with the test data transformed -> /artifacts)
# Loads saved model with the best score (model.pkl)
# Makes prediction and outputs a .csv file with the right format (index + precentage_docks_available) for a kaggle submission -> /artifacts.