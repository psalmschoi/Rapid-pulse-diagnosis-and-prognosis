# Rapid and non-destructive diagnosis of lithium-ion batteries via quantification of anode spatial degradation
These are the codes for the paper: Rapid and non-destructive diagnosis of lithium-ion batteries via quantification of anode spatial degradation. Inwoo Kim, Seongha An, Jang Wook Choi


**Data preparation**

Kim, Inwoo; An, Seongha; Choi, Jang Wook (2025), “The Dataset for: Rapid and non-destructive diagnosis of lithium-ion batteries via quantification of anode spatial degradation”, Mendeley Data, V1, doi: 10.17632/p5vbbytz3x.1


**Code overview**

From the main directory, run the following commands.

For all .py scripts, use the command format: python -m <filename>

Place the file SOC_Point_Data.csv in the same directory as the Jupyter notebook before running the deep learning model.


[Scripts]
- Pulse_Extractor.py: Data processing of SOC-dependent relaxation voltage from relaxation data at each RPT point (excluding the final RPT).
- Final_Pulse_Extractor.py: Data processing of SOC-dependent relaxation voltage from relaxation data at the final RPT.
- Grid_Search_Optimize.py: Calculation of Pearson correlation coefficients between time & SOC ranges and current & future SOH.
- Calculate_PIOV.py: Calculation of pulse-induced overvoltage (PIOV)
- Final_Clustering.py: Execution of unsupervised clustering.


[Plotting]
- Show_Single_Pulse.py: Plotting SOC-dependent relaxation voltage for a specific cell.
- Show_Individual_Retention.py: Plotting capacity retention for a specific cell.
- Show_Anomal_Retention.py: Comparative plotting of retention across cells subjected to the same usage scenario.
- Show_Whole_Retention.py: Plotting capacity retention for all cells.


[Deep learning modeling]
- Processed input_MLP.ipynb: Capacity prediction with MLP based on PIOV features.
- Raw input_2D CNN_MLP.ipynb: Data-driven feature extraction using 2D CNN, followed by capacity prediction with MLP.
- Raw input_EN_MLP.ipynb: Data-driven feature extraction using elastic net (EN), followed by capacity prediction with MLP.
- Raw input_GRU_MLP.ipynb: Data-driven feature extraction using GRU, followed by capacity prediction.
