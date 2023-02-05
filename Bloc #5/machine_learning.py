import argparse
import os
import pandas as pd
import time
import mlflow
from mlflow.models.signature import infer_signature
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import  StandardScaler, FunctionTransformer, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

if __name__ == "__main__":

    ### MLFLOW Experiment setup
    experiment_name="price prediction"
    mlflow.set_experiment(experiment_name)
    experiment = mlflow.get_experiment_by_name(experiment_name)

    os.environ["AWS_ACCESS_KEY_ID"] = "AKIAUIFQUFRWNIV5KEX3"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "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"

    client = mlflow.tracking.MlflowClient()
    mlflow.set_tracking_uri("https://mlflow202.herokuapp.com")

    run = client.create_run(experiment.experiment_id)

    print("training model...")
    
    # Time execution
    start_time = time.time()

    # Call mlflow autolog
    #mlflow.sklearn.autolog(log_models=False) # We won't log models right away

    # Parse arguments given in shell script
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", default=1)
    parser.add_argument("--min_samples_split", default=2)
    args = parser.parse_args()

    # Load Get Around Pricing dataset
    dataset = pd.read_csv('/Users/marjorylamothe/Downloads/Projet Get Around/get_around_pricing_project.csv')
    
    # Apply preprocessing
    dataset=dataset.drop(columns='Unnamed: 0')
    value_counts_model = dataset['model_key'].value_counts()
    to_rename_model = value_counts_model[value_counts_model <= 3].index
    dataset['model_key']=dataset['model_key'].apply(lambda x: 'Other' if x in to_rename_model else x)

    alue_counts_fuel = dataset['fuel'].value_counts()
    to_rename_fuel = value_counts_fuel[value_counts_fuel <= 8].index
    dataset['fuel']=dataset['fuel'].apply(lambda x: 'other' if x in to_rename_fuel else x)

    value_counts_paint = dataset['paint_color'].value_counts()
    to_rename_paint = value_counts_paint[value_counts_paint <= 6].index
    dataset['paint_color']=dataset['paint_color'].apply(lambda x: 'other' if x in to_rename_paint else x)

    value_counts_type = dataset['car_type'].value_counts()
    to_rename_type = value_counts_type[value_counts_type <= 1].index
    dataset['car_type']=dataset['car_type'].apply(lambda x: 'Other' if x in to_rename_type else x)

    dataset["price_category"] = dataset["rental_price_per_day"].apply(lambda x: "0-50" if x >= 0 and x <= 50 
                                            else "51-100" if x >= 51 and x <= 100 
                                            else "101-150" if x >= 101 and x <= 150 
                                            else "151-200" if x >= 151 and x <= 200 
                                            else "201-250" if x >= 201 and x <= 250 
                                            else "251-300" if x >= 251 and x <= 300 
                                            else "301-450" if x >= 301 and x <= 450 
                                            else x)

    dataset["mileage_cat"] = dataset["mileage"].apply(lambda x: "0-50000" if x >= 0 and x <= 50000 
                                            else "50001-100000" if x >= 50001 and x <= 100000 
                                            else "100001-150000" if x >= 100001 and x <= 150000 
                                            else "150001-200000" if x >= 150001 and x <= 200000 
                                            else "200001-250000" if x >= 200001 and x <= 250000 
                                            else "250001-300000" if x >= 250001 and x <= 300000
                                            else "300001-350000" if x >= 300001 and x <= 350000
                                            else "350001-400000" if x >= 350001 and x <= 400000
                                            else "other")

    dataset["power_cat"] = dataset["engine_power"].apply(lambda x: "0-50" if x >= 0 and x <= 50 
                                            else "51-100" if x >= 51 and x <= 100 
                                            else "101-150" if x >= 101 and x <= 150 
                                            else "151-200" if x >= 151 and x <= 200 
                                            else "201-250" if x >= 201 and x <= 250
                                            else "251-300" if x >= 251 and x <= 300 
                                            else '301-350' if x >= 301 and x <= 350 
                                            else '351-400' if x >= 351 and x <= 400 
                                            else '401-450' if x >= 401 and x <= 450 
                                            else x)

    dataset=dataset.drop(columns=["rental_price_per_day","mileage","engine_power"])




    # Split dataset into X features and Target variable
    target_variable = "price_category"

    X = dataset.drop(target_variable, axis = 1)
    Y = dataset.loc[:,target_variable]

    # Automatically detect names of numeric/categorical columns
    numeric_features = []
    categorical_features = []
    for i,t in X.dtypes.iteritems():
        if ('float' in str(t)) or ('int' in str(t)) :
            numeric_features.append(i)
        else :
            categorical_features.append(i)

    # Split our training set and our test set 
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

    # Visualize dataset 
    X_train.head()

    # Create pipeline for categorical features
    categorical_transformer = OneHotEncoder(drop='first') # no missing values in categorical data, so we only need the OHE
 
    # Use ColumnTransformer to make a preprocessor object that describes all the treatments to be done
    preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features)
    ])

    dataset=dataset.astype(str)

    X_train = preprocessor.fit_transform(X_train.astype(str))
    encoder = LabelEncoder()
    Y_train = encoder.fit_transform(Y_train.astype(str))
    X_test = preprocessor.transform(X_test.astype(str)) 
    Y_test = encoder.transform(Y_test.astype(str))

    # Pipeline 
    n_estimators = int(args.n_estimators)
    min_samples_split=int(args.min_samples_split)

    model = Pipeline(steps=[
        ("Regressor",RandomForestClassifier(n_estimators=n_estimators, min_samples_split=min_samples_split))
    ])
    
    mlflow.sklearn.autolog()

    # Log experiment to MLFlow
    with mlflow.start_run() as run:
        model.fit(X_train, Y_train)
        predictions = model.predict(X_train)

        # Log model seperately to have more flexibility on setup 
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="appointment_cancellation_detector",
            registered_model_name="appointment_cancellation_detector_RF",
            signature=infer_signature(X_train, predictions)
        )
        
    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")