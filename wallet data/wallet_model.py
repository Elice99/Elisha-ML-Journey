import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, KFold
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import pickle

print("✓ All libraries imported successfully!\n")

#parameters
C = 1.0
n_splits = 5

output_file = f'wallet_classifer={C}.bin'


df = pd.read_csv('dune_data.csv')

print("\n" + "=" * 80)
print(" EXPLORATORY DATA ANALYSIS")
print("=" * 80)

# Check target variable distribution:
print(df['target_variable'].value_counts())

# Encode target variable: convert '🔴 Bad Trader' to 0 and '🟢 Good Trader' to 1
df.target_variable = (df.target_variable == '🟢 Good Trader' ).astype(int)
df = df.drop(columns=['wallet']) # This is an identifier  and has no predictive power, so it's removed.


# Standardize string values
string_cols = df.select_dtypes(include='object').columns
for col in string_cols:
    df[col] = df[col].str.lower().str.replace(' ', '_')

print("✓ Column names and values standardized\n")
vol_logs = np.log1p(df.total_volume)

print("\n" + "=" * 80)
print(" SPLIT DATASET")
print("=" * 80)


df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)
len(df_full_train), len(df_test)


# Apply feature engineering to both training and test sets
def add_features(df):
    df['vol_per_tx'] = df['total_volume'] / df['tx_count_365d'].replace(0, 1)
    df['activity_per_week'] = df['tx_count_365d'] / df['active_weeks'].replace(0, 1)
    df['avg_weekly_vol'] = df['total_volume'] / df['active_weeks'].replace(0, 1)
    return df

df_full_train = add_features(df_full_train)
df_test = add_features(df_test)



numerical = [
              
             'tx_count_365d', 
             'vol_per_tx', 
             'activity_per_week', 
             'avg_weekly_vol']

#Training
def train(df_train, y_train, C=1.0):
    dicts = df_train[numerical].to_dict(orient='records')
    
    dv = DictVectorizer(sparse=False)
    X_train = dv.fit_transform(dicts)
    
    model = LogisticRegression(C=C, max_iter=1000)
    
    model.fit(X_train, y_train) 
    
    return dv, model

def predict(df, dv, model):
    dicts = df[numerical].to_dict(orient='records') 
    
    X = dv.transform(dicts)
    y_pred = model.predict_proba(X)[:, 1] 
    
    return y_pred   



#validation
print(f'doing validation with C={C}')
kfold = KFold(n_splits=n_splits, shuffle=True, random_state=1)

scores = []
fold = 0
for train_idx, val_idx in kfold.split(df_full_train):
    df_train = df_full_train.iloc[train_idx]
    df_val = df_full_train.iloc[val_idx]
    
    y_train = df_train.target_variable.values
    y_val = df_val.target_variable.values
    
    dv, model = train(df_train, y_train, C=C)
    y_pred = predict(df_val, dv, model)
    
    
    auc = roc_auc_score(y_val, y_pred)
    scores.append(auc)
    print(f'auc on fold {fold} is {auc}')
    fold = fold + 1

print('validation result: ')    
print(f'C=%s %.3f +- %.3f' % (C, np.mean(scores), np.std(scores)))   
scores


#training the final model
print('training the final model')
dv, model = train(df_full_train, df_full_train.target_variable.values, C=1.0)
y_pred = predict(df_test, dv, model) 

y_test = df_test.target_variable.values
auc = roc_auc_score(y_test, y_pred)
print(f'auc={auc}')

#saving the model
with open(output_file, 'wb') as f_out:
    pickle.dump((dv, model), f_out)
    
print(f'the model is saved to {output_file}')