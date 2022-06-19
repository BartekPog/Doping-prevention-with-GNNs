# Dataset

| Field | Description |
| ------- | ------ |
| ID_random | a random athlete identifier |
| Gender | M or F |
| SpecificGravity | the measured “density” of the urine sample, which is used to correct for differences in urine concentration due to factors such as hydration state. The SG is used to calculated the corrected concentrations of the steroid profile, denoted by “corr” below. |
| In Comp | was the sample taken in competition or not (Y/N) |
| Adiol (ng/mL) |  5αAdiol = 5α-Androstane-3α,17β-diol |
| Bdiol (ng/mL) | 5βAdiol = 5β-Androstane-3α,17β-diol |
| Androsterone (ng/mL) | Andro |
| Etiocholanolone (ng/mL) | Etio |
| Epitestosterone (ng/mL) | E |
| Testosterone (ng/mL) | T |
| T_E_ratio |
| Andro_T_ratio |
| Andro_Etio_ratio |
| Adiol_Bdiol_ratio |
| Adiol_E_ratio |
| Adiol_corr (ng/mL) | corrected by specific gravity |
| Bdiol_corr (ng/mL) | corrected by specific gravity |
| Androsterone_corr (ng/mL) | corrected by specific gravity |
| Etiocholanolone_corr (ng/mL) | corrected by specific gravity |
| Epitestosterone_corr (ng/mL) | corrected by specific gravity |
| Testosterone_corr (ng/mL) | corrected by specific gravity |
| Total Observation | total number of samples collected for that particular athlete i.e. total no. of samples in the longitudinal steroid profile of that particular athlete |


We’ve provided both the measured and the specific gravity-corrected concentrations for the **6 steroids**, and each provides useful information. Overall, the corrected concentrations are more suitable for comparison to each other as they are normalized for differences in urine density caused by factors such as hydration state. The uncorrected concentrations, on the other hand, provide information on the potential effects of analytical variation, in the event that you may wish to incorporate analytical uncertainty into your model.

The formula for the correction using specific gravity is:

<img src="https://latex.codecogs.com/gif.latex?Conc_corr=Conc\_measured\cdot\frac{1.02-1}{SG-1}" />



You can also follow this literature to understand more about the data:
Van Renterghem, P., Van Eenoo, P., Geyer, H., Schänzer, W., & Delbeke, F. T. (2010). Reference ranges for urinary concentrations and ratios of endogenous steroids, which can be used as markers for steroid misuse, in a Caucasian population of athletes. Steroids, 75(2), 154–163. https://doi.org/10.1016/j.steroids.2009.11.008
 

 

 

 

