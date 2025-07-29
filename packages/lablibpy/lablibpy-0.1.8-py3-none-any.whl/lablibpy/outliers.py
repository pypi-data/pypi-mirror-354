import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def create_features(data):
    housing_df = data.frame
    numerical_features = housing_df.select_dtypes(include=[np.number]).columns
    return housing_df, numerical_features

def feature_histplot(housing_df, numerical_features, figsize, num_cols, color):
    plt.figure(figsize=figsize)
    for i, feature in enumerate(numerical_features):
        plt.subplot(num_cols, num_cols, i + 1)
        sns.histplot(housing_df[feature], kde=True, bins=30, color=color)
        plt.title(f'Distribution of {feature}')
    plt.tight_layout()
    plt.show()

def feature_boxplot(housing_df, numerical_features, figsize, num_cols, color):
    plt.figure(figsize=figsize)
    for i, feature in enumerate(numerical_features):
        plt.subplot(num_cols, num_cols, i + 1)
        sns.boxplot(x=housing_df[feature], color=color)
        plt.title(f'Box Plot of {feature}')
    plt.tight_layout()
    plt.show()

def get_outliers_summary(housing_df, numerical_features, q1_quantile, q3_quantile):
    outliers_summary = {}
    for feature in numerical_features:
        Q1 =housing_df[feature].quantile(q1_quantile)
        Q3 =housing_df[feature].quantile(q3_quantile)
        IQR = Q3-Q1
        lower_bound = Q1- 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = housing_df[(housing_df[feature] < lower_bound) | (housing_df[feature] > upper_bound)]
        outliers_summary[feature] = len(outliers)
    return outliers_summary