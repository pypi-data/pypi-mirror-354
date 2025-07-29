import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def adjust_format(cent_report):
    '''Takes a centrifugeReport.txt file and returns a list containing lines with
slightly tweaked format to mirror the ML model training data.'''
    taxRank_list = ['species', 'genus', 'subspecies', 'leaf']
    total = total_reads(cent_report)
    line_list = []
    with open(cent_report, "r") as f_in:
        for line in f_in:
            if not line.split("\t")[0] == "name":
                line = line.replace(",","")
                tmp_list = []
                reads = int(line.split("\t")[4])
                abundance = float(reads/total)
                taxID = line.split("\t")[1].strip()
                line = line.split("\t")
                taxRank = line[2].strip()
                if taxRank in taxRank_list:
                    genus = line[0].split(" ")[0]
                else:
                    genus = "NA"
                for x in range(0, len(line)-1, 1):
                    tmp_list.append(line[x])
                line_list.append(f"{','.join(tmp_list)},{abundance},{genus},0,0")
            else:
                line = line.replace("\t", ",").strip()
                line_list.append(f"{line},genus,presence,sim_abundance")
    return line_list

def total_reads(cent_report):
    total = []
    with open(cent_report, "r") as f_in:
        for line in f_in:
            if not line.startswith("name"):
                reads = line.split("\t")[4]
                total.append(int(reads))
    return sum(total)

def convert_file(cent_report):
    '''Very basic function; creates new file with the output from "adjust_format()". '''
    with open(f"{os.path.splitext(cent_report)[0]}_data.txt", "w") as f_out:
        for items in adjust_format(cent_report):
            f_out.write(f"{items}\n")
    return f"Data file {os.path.splitext(cent_report)[0]}_data.txt created"


def train_model(data_folder, model_save_path='trained_model.joblib'):
    '''RandomForestClassifier model. Trained on provided simulated data set.
Returns the trained model.'''
    # Specify the expected column names
    expected_columns = ['name', 'taxID', 'taxRank', 'genomeSize', 'numReads', 'numUniqueReads',
                        'abundance', 'genus', 'presence', 'sim_abundance']

    # Step 1: Load and preprocess the data for each population (Training Data)
    all_files = os.listdir(data_folder)

    # Initialize empty lists to store data from all populations
    all_data = []

    for file_name in all_files:
        if file_name.endswith('.txt'):
            file_path = os.path.join(data_folder, file_name)

            # Load data for the current population
            print(f'Processing file: {file_path}')
            try:
                # Read the comma-separated file with expected column names
                data = pd.read_csv(file_path, names=expected_columns, header=0)
            except pd.errors.ParserError as e:
                print(f"Error reading file {file_path}: {e}")
                continue

            # Handle missing values if necessary
            data.dropna(inplace=True)

            # Drop non-numeric columns
            data_numeric = data.select_dtypes(include='number')

            # Append data from the current population to the list
            all_data.append(data_numeric)

    # Combine data from all populations for training
    if all_data:
        combined_data = pd.concat(all_data, axis=0)

        if not combined_data.empty:
            # Step 3: Model selection
            model = RandomForestClassifier(random_state=42)

            # Split the combined data into features (X) and labels (y)
            X = combined_data.drop(['presence', 'sim_abundance'], axis=1)
            y = combined_data['presence']

            # Step 4: Model training
            model.fit(X, y)

            # Save the trained model
            joblib.dump(model, model_save_path)

            print(f"Model trained and saved to {model_save_path}")
        else:
            print("No valid data after preprocessing. Check your data format and preprocessing steps.")
    else:
        print("No valid TXT files found in the training data folder.")


def make_predictions(input_file_path, model_path=None):
    '''Function takes the trained model output from "train_model()" and a modified centrifugeReport
created using "convert_file() and returns "presence" predictions and "certainty_scores".'''
    # Load the trained model
    if model_path is None:
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'trained_model.joblib')

    model = joblib.load(model_path)
    # Specify the expected column names
    expected_columns = ['name', 'taxID', 'taxRank', 'genomeSize', 'numReads', 'numUniqueReads',
                        'abundance', 'genus', 'presence', 'sim_abundance']


    # Load the input file for prediction
    input_data = pd.read_csv(input_file_path, names=expected_columns, header=0)
    input_data.dropna(inplace=True)

    # Extract species name, taxID, and numeric features for prediction
    input_data_numeric = input_data.select_dtypes(include='number')
    X_pred = input_data_numeric.drop(['presence', 'sim_abundance'], axis=1)
    species_name = input_data['name']
    taxID = input_data['taxID']

    # Make predictions and get certainty scores
    predictions = model.predict(X_pred)
    certainty_scores = model.predict_proba(X_pred)[:, 1]  # Probability for class 1

    # Collect results in a list of dictionaries
    results = []
    for pred, certainty, name, tax_id in zip(predictions, certainty_scores, species_name, taxID):
        if pred == 1:  # Only include positive class predictions
            result_entry = {
                'Species': name,
                'TaxID': tax_id,
                'Prediction': pred,
                'Certainty': round(certainty, 2)
            }
            results.append(result_entry)

    return results
