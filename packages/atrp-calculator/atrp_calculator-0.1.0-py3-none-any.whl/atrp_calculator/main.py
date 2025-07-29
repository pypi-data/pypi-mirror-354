import os
import pandas as pd
from calculator import process_excel_and_generate_recipes


def main():
    # ---- USER INPUT ----
    file_path = "C:/Users/Cesar/Box/Sync files/2023/Experiments/CR1_32 DP Exp HighRes/test/Polymer_sheet_DP Var 05303025.xlsx"  # ← change this if needed

    # ---- CREATE OUTPUT FOLDER ----
    output_folder = os.path.splitext(file_path)[0] + "_output"
    os.makedirs(output_folder, exist_ok=True)

    # ---- RUN PROCESSING ----
    result_df = process_excel_and_generate_recipes(file_path)

    # ---- SAVE OUTPUT ----
    output_file = os.path.join(output_folder, "atrp_recipes.xlsx")
    result_df.to_excel(output_file, index=False)
    print(f"\n✅ Recipes saved to: {output_file}\n")


if __name__ == "__main__":
    main()


# Need to run these in one line
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# .\venv\Scripts\Activate.ps1
