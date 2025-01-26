import os
import yaml
import pandas as pd

class YAML:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def yaml_to_dataframe(self, yaml_file):
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
        if isinstance(data, list) and data:
            df = pd.DataFrame(data) 

            if 'Ticker' in df.columns:
                for Ticker, group in df.groupby('Ticker'):
                    stock_file = os.path.join(self.output_folder, f"{Ticker}.csv")
                    file_exists = os.path.isfile(stock_file)
                    group.to_csv(stock_file, mode= 'a', index=False, header=not file_exists)
                    print(f"Saved: {Ticker}")
        else:
            print(f"Skipping unsupported or empty YAML structure: {yaml_file}")
            return pd.DataFrame()

    def combine_files(self):
        os.makedirs(self.output_folder, exist_ok=True)       
        for dirpath, _, filenames in os.walk(self.input_folder):
            for file in filenames:
                if file.endswith(".yaml") or file.endswith(".yml"):
                    yaml_path = os.path.join(dirpath, file)
                    print(f"Processing: {yaml_path}")
                    self.yaml_to_dataframe(yaml_path)

if __name__ == "__main__":
    input_folder = "c:/Users/ganes/Documents/DataScienceLearnings/Guvi/Project_2 Data-Driven Stock Analysis/Input/Data-20241230T123422Z-001/Data/data/"
    output_folder = "c:/Users/ganes/Documents/DataScienceLearnings/Guvi/Project_2 Data-Driven Stock Analysis/Input/Data-20241230T123422Z-001/Data_csv/"

    converter = YAML(input_folder, output_folder)
    converter.combine_files()