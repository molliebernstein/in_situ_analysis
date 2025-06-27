In Situ Analysis
==========================================

This repository contains code for quantifying cell populations and marker intensities from in situ hybridization experiments, using output files from QuPath. The analysis is available both as a Python script (`in_situ.py`) and as a Jupyter notebook (`in_situ.ipynb`). You can use either for batch processing and summary statistics.

The main features of this code are:

- **Batch processing** of QuPath CSV output files (single- or multi-channel)
- **Group mapping** based on user assigned mouse/sample IDs
- **Counts** of cells positive for each marker or marker combination (e.g., Th, Trpc6, Th:Trpc6)
- **Calculation of mean intensities** for each marker across all cells, Th⁺ cells, and Th⁻ cells
- **Output of summary CSVs** at the slice and mouse level

----------------------------------------------------------------
Example Data
------------

Three example CSV files are provided:

1. 123_3.csv
    - Data from mouse_ID 123, slice 3

2. 9937_2.csv
    - Data from mouse_ID 9937, slice 2
  
3. 9937_4.csv
    - Data from mouse_ID 9937, slice 4
   
----------------------------------------------------------------
Scripts Included
----------------

1. **in_situ.py**
    - Extracts cell counts and mean intensities for specified combinations of genes.
    - Generates: insitu_results_all.csv (slice-level results) and insitu_results_by_mouse.csv (mouse-level averages)
    - Also provided as notebook-style cells for interactive use.
  
----------------------------------------------------------------
How to Use in a Notebook
------------------------

- Copy and paste the notebook cells from the README or `.ipynb` files.
- Upload the corresponding example CSV to your notebook environment.
- Run cells step by step; outputs and saved files will be shown or downloaded as needed.

----------------------------------------------------------------
Requirements
------------

Python 3.x with:

- pandas
- os

Install with:
    pip install -r requirements.txt

----------------------------------------------------------------
Repository Structure (example)
-----------------------------

- README.txt
- requirements.txt
- in_situ.py
- in_situ.ipynb
- 123_3.csv
- 9937_2.csv
- 9937_4.csv

----------------------------------------------------------------
Contact & Author
----------------

Questions? Open an issue or pull request on GitHub.

Author: Mollie Bernstein, 2025

mollie.bernstein@gmail.com
