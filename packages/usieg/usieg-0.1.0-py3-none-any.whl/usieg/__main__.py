import argparse
import json
from usieg.arpf1 import from_rttm
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_path", help="The rttm file path of the model output")
    parser.add_argument("label_path", help="The rttm file path of the label")
    args = parser.parse_args()
	
    result = from_rttm(args.model_path, args.label_path)
    df = pd.DataFrame(result)
    print(df)

if __name__=="__main__":
	main()