import pandas as pd
import os

# Define the paths to your raw healthcare data
general_path = 'data/Hospital_General_Information.csv'
safety_path = 'data/Complications_and_Deaths-Hospital.csv'

try:
    print("Reading healthcare datasets...")
    general_df = pd.read_csv(general_path)
    safety_df = pd.read_csv(safety_path)

    # 1. Standardize Facility IDs to 6 digits (Critical for clinical joins)
    general_df['Facility ID'] = general_df['Facility ID'].astype(str).str.zfill(6)
    safety_df['Facility ID'] = safety_df['Facility ID'].astype(str).str.zfill(6)

    # 2. Clean suppressed 'Not Available' clinical data
    general_df.replace('Not Available', pd.NA, inplace=True)
    safety_df.replace('Not Available', pd.NA, inplace=True)

    # 3. Create cleaned files for your analysis
    general_df.to_csv('data/cleaned_general_info.csv', index=False)
    safety_df.to_csv('data/cleaned_safety_scores.csv', index=False)

    print("✅ Success: Cleaned clinical data generated in the /data folder.")

except Exception as e:
    print(f"❌ Error: {e}. Check if your CSV files are in the 'data' folder.")