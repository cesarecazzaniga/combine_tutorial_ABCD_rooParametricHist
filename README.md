# combine_tutorial_ABCD_rooParametricHist
tutorial for Combine using RooParamertricHist to perform the ABCD method

## Introduction
The goal of this tutorial is to exemplify the usage of ```RooParametricHist``` in [CMS Combine](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/) to implement a bin-by-bin ABCD method.
In this tutorial we will work with a toy example that could resamble a real physics analysis case. We consider the search for a BSM particle $\Phi$ with a mass range between 1500 and 5000 GeV that leads some excess in the tails of an observable $z$ (which could be $p_{T,\mathrm{miss}}$ ). We assume that we have found two uncorrelated discriminating features $x$ and $y$ that can be used to build the ABCD plane (the regions A,B,C,D will be defined by cutting on $x,y$), and we assume that $z$ is uncorrelated with respect to these two features. In this way, binning the variable $z$ in the same way in the regions A,B,C,D, per-bin transfer factors in the $z$ variable can be derived with the ABCD method to obtain the estimate of the background in the signal region. In our example we will call ```data``` the nominal background distribution we have generated, and the background will be estimated from these data from the control regions B,C,D and compared to data in the Signal Region A.

The tutorial has 4 main parts:

1. [Generate input data](#inputs)
2. [Prepare Combine datacards](#datacards)
3. [Run fit](#fit)
4. [Produce limits](#limits)

## Generate input data
<a id="inputs"></a>

The histograms for the $z$ observable in the different regions A,B,C,D can be produced using the [jupyter notebook](https://github.com/cesarecazzaniga/combine_tutorial_ABCD_rooParametricHist/blob/main/ABCD_combine_tutorial_input_histograms.ipynb). In the notebook the expected rates for different signal hypothesis (as a function of $\Phi$ mass $m_{\Phi} \in \{1500, 2000, 3000, 4000, 5000 \}$ GeV) and the background yields are specified, as well as the distributions in $x,y,z$ of the signals and backgrounds. In $x,y$, the signal and the background are assumed to be distributed as multivariate gaussians, with the background centred at $(0,2,0.2)$ in $(x,y)$ while the signals centred in the upper-right corner of the plane ($x,y>0.5$). For the $z$ feature, the background and the signal distributions are sampled from an exponential, for the signal the tails of the exponential get enhance with the mass parameter $m_{\Phi}$. 

![input distributions](docs/inputs.png)

The ABCD boundaries are chosen in the example to be $(0.5,0.5)$, and A is defined as the signal region, while the others are control regions used for the estimation of the background. From the example provided, the signal contamination in the control regions is expected to be low, and the non-closure of the background estimation to be small. The histograms for the different regions are saved in separate root files for each signal hypothesis and total background. 

## Prepare Combine datacards 
<a id="datacards"></a>

From the input histograms, for each signal hypothesis, 4 datacards can be built, one for each region of the ABCD plane. Examples of the templates for the datacards (for a signal mass point at 1500 GeV) can be found in the following. All the example datacards are stored in the directory [datacards](https://github.com/cesarecazzaniga/combine_tutorial_ABCD_rooParametricHist/tree/main/datacards). 

<details>
<summary> Datacard Region A  </summary>
  
```
imax * number of bins 
jmax * number of processes minus 1 
kmax * number of nuisance parameters
-----------------------------------------------------------------------------------
shapes   data_obs  A    param_ws.root    wspace:data_obs_A
shapes   Bkg  A    param_ws.root    wspace:bkg_A
shapes   mPhi1500  A    param_ws.root    wspace:mPhi1500_A
-----------------------------------------------------------------------------------
bin               A
observation       -1
-----------------------------------------------------------------------------------
bin                                     A                                            A                                          
process                                 Bkg                                          mPhi1500                                   
process                                 1                                           0                                          
rate                                    1                                           -1                                         
-----------------------------------------------------------------------------------
lumi                lnN                 -                                            1.0160000000
BkgRate             lnN                 1.05                                         - 

```

</details>

<details>
<summary> Datacard Region B  </summary>

```
imax * number of bins 
jmax * number of processes minus 1 
kmax * number of nuisance parameters
-----------------------------------------------------------------------------------
shapes   data_obs  B    param_ws.root    wspace:data_obs_B
shapes   Bkg  B    param_ws.root    wspace:bkg_B
shapes   mPhi1500  B    param_ws.root    wspace:mPhi1500_B
-----------------------------------------------------------------------------------
bin               B
observation       -1
-----------------------------------------------------------------------------------
bin                                     B                                           B                                          
process                                 Bkg                                         mPhi1500                                   
process                                 1                                           0                                          
rate                                    1                                           -1                                         
-----------------------------------------------------------------------------------
lumi                lnN                 -                                          1.0160000000

```

</details>

<details>
<summary> Datacard Region C  </summary>
  
```
imax * number of bins 
jmax * number of processes minus 1 
kmax * number of nuisance parameters
-----------------------------------------------------------------------------------
shapes   data_obs  C    param_ws.root    wspace:data_obs_C
shapes   Bkg  C    param_ws.root    wspace:bkg_C
shapes   mPhi1500  C    param_ws.root    wspace:mPhi1500_C
-----------------------------------------------------------------------------------
bin               C
observation       -1
-----------------------------------------------------------------------------------
bin                                     C                                           C                                          
process                                 Bkg                                         mPhi1500                                   
process                                 1                                           0                                          
rate                                    1                                           -1                                         
-----------------------------------------------------------------------------------
lumi                lnN                 -                                          1.0160000000

```

</details>

<details>
<summary> Datacard Region D  </summary>
  
```
imax * number of bins 
jmax * number of processes minus 1 
kmax * number of nuisance parameters
-----------------------------------------------------------------------------------
shapes   data_obs  D    param_ws.root    wspace:data_obs_D
shapes   Bkg  D    param_ws.root    wspace:bkg_D
shapes   mPhi1500  D    param_ws.root    wspace:mPhi1500_D
-----------------------------------------------------------------------------------
bin               D
observation       -1
-----------------------------------------------------------------------------------
bin                                     D                                           D                                          
process                                 Bkg                                         mPhi1500                                   
process                                 1                                           0                                          
rate                                    1                                           -1                                         
-----------------------------------------------------------------------------------
lumi                lnN                 -                                          1.0160000000

```
</details>

As an example, for each datacard, we have assigned a systematic uncertainty of 1.6% due to lumi to the signal processes, and a systematic of 5% to background in the SR (to take into account of non-closure of the method). 
Notice that each datacard for each region has a ```shapes``` section for the observed data ```data_obs```, for the background ```Bkg``` and for the signal. The signal and data shapes are stored in a workspace ```wspace``` linked to the shapes section in the datacard, while the background shapes are stored in a ```RooParametricHist``` object (for what a RooParametricHist is look [here](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/part3/nonstandard/?h=rooparametrichist#rooparametrichist-gamman-for-shapes)). In the following we show how to build the workspace.

First create a RooWorkspace, implement a function ```__get_histograms_regions``` to read the input histograms from the A,B,C,D regions and import them as ```RooDataHist``` in the workspace.

<details>
<summary> Import histograms in workspace for signal and observed data  </summary>
  
``` 
#Output file and workspace
output_file_ws =  TFile(card_output_directory+"param_ws.root","RECREATE")
ws = RooWorkspace("wspace","wspace")

#Define a RooRealVar for the observable z to fit
variable_z = RooRealVar( "z", "z", 200, 14000, "GeV")

#Save data in RooDataHist
histA_obs , histB_obs, histC_obs, histD_obs =  __get_histograms_regions(channel, "data_obs", input_file)


histData_A = RooDataHist("data_obs_A", "Obs Data region A",  RooArgList(variable_z), histA_obs, 1.)
histData_B = RooDataHist("data_obs_B", "Obs Data region B",  RooArgList(variable_z), histB_obs, 1.)
histData_C = RooDataHist("data_obs_C", "Obs Data region C",  RooArgList(variable_z), histC_obs, 1.)
histData_D = RooDataHist("data_obs_D", "Obs Data region D",  RooArgList(variable_z), histD_obs, 1.)

#Import data in workspace
getattr(ws, "import")(histData_A, RooFit.Rename("data_obs_A"))
getattr(ws, "import")(histData_B, RooFit.Rename("data_obs_B"))
getattr(ws, "import")(histData_C, RooFit.Rename("data_obs_C"))
getattr(ws, "import")(histData_D, RooFit.Rename("data_obs_D"))

#Save signals in RooDataHist
histA_sgn , histB_sgn, histC_sgn, histD_sgn =  __get_histograms_regions(channel, signal, input_file)
histSgn_A = RooDataHist(signal+"_A", "Sgn Data region A",  RooArgList(variable_z), histA_sgn, 1.)
histSgn_B = RooDataHist(signal+"_B", "Sgn Data region B",  RooArgList(variable_z), histB_sgn, 1.)
histSgn_C = RooDataHist(signal+"_C", "Sgn Data region C",  RooArgList(variable_z), histC_sgn, 1.)
histSgn_D = RooDataHist(signal+"_D", "Sgn Data region D",  RooArgList(variable_z), histD_sgn, 1.)

#Import signals in workspace
getattr(ws, "import")(histSgn_A, RooFit.Rename(signal+"_A"))
getattr(ws, "import")(histSgn_B, RooFit.Rename(signal+"_B"))
getattr(ws, "import")(histSgn_C, RooFit.Rename(signal+"_C"))
getattr(ws, "import")(histSgn_D, RooFit.Rename(signal+"_D"))

```
</details>

For B,C,D regions, create a ```RooParametricHist``` object, storing the content of the background bins in B,C,D as ```RooRealVar``` :

<details>
<summary> Create RooParametricHist for control regions background templates  </summary>

```
#get the background histograms  
histA_pr , histB_pr, histC_pr, histD_pr =  __get_histograms_regions(channel, process, input_file)        

#bins for RooParametricHist used for transfer region
process_B_region_bins = RooArgList()
process_B_region_bins_list = []

#bins for RooParametricHist used for C and D regions
process_C_region_bins = RooArgList()
process_C_region_bins_list = []
process_D_region_bins = RooArgList()
process_D_region_bins_list = []


#Add yields in B Region per each bin (including overflow) as RooRealVar in RooArgList - B region is assumed to be the Control region to be related to A (SR)                                                                                                
for i in range(1,histB_obs.GetNbinsX()+1):
    bin_B_i = RooRealVar(process+"_B_region_bin_"+str(i),"Background yield in control region B bin " + str(i),histB_obs.GetBinContent(i),0.,2.0*histB_obs.GetBinContent(i))
    process_B_region_bins_list.append(bin_B_i)


for idx,binB_i in enumerate(process_B_region_bins_list):
    process_B_region_bins.add(binB_i)

#Add yields in C and D Region as RooRealVar in RooArgList (C and D regions are used to compute the transfer factor)
for i in range(1,histC_obs.GetNbinsX()+1):
    bin_C_i = RooRealVar(process+"_C_region_bin_"+str(i),"Background yield in control region C bin " + str(i),histC_obs.GetBinContent(i),0.,2.0*histC_obs.GetBinContent(i))
    process_C_region_bins_list.append(bin_C_i)

for idx,binC_i in enumerate(process_C_region_bins_list):
    process_C_region_bins.add(binC_i)

for i in range(1,histD_obs.GetNbinsX()+1):
    bin_D_i = RooRealVar(process+"_D_region_bin_"+str(i),"Background yield in control region D bin " + str(i),histD_obs.GetBinContent(i),0.,2.0*histD_obs.GetBinContent(i))
    process_D_region_bins_list.append(bin_D_i)

for idx,binD_i in enumerate(process_D_region_bins_list):
    process_D_region_bins.add(binD_i)


#Parametric histogram for control region B (transfering region, to be related via transfer factor to SR)
param_hist_B_region = RooParametricHist(process+"_B", "Background PDF in B region",variable_z,process_B_region_bins,histB_pr)
param_Bkg_B_norm = RooAddition(process+"_B"+"_norm","Total Number of events from background in control region B",process_B_region_bins)
getattr(ws, "import")(param_hist_B_region, RooFit.Rename(process+"_B"))
getattr(ws, "import")(param_Bkg_B_norm, RooFit.Rename(process+"_B"+"_norm"),RooFit.RecycleConflictNodes())

#Parametric histograms for control regions C (used to compute transfer factor) 
param_hist_C_region = RooParametricHist(process+"_C", "Background PDF in C region",variable_z,process_C_region_bins,histC_pr)
param_Bkg_C_norm = RooAddition(process+"_C"+"_norm","Total Number of events from background in control region C",process_C_region_bins)
getattr(ws, "import")(param_hist_C_region, RooFit.Rename(process+"_C"))
getattr(ws, "import")(param_Bkg_C_norm, RooFit.Rename(process+"_C"+"_norm"),RooFit.RecycleConflictNodes())

#Parametric histograms for control regions D (used to compute transfer factor)
param_hist_D_region = RooParametricHist(process+"_D", "Background PDF in D region",variable_z,process_D_region_bins,histD_pr)
param_Bkg_D_norm = RooAddition(process+"_D"+"_norm","Total Number of events from background in control region D",process_D_region_bins)
getattr(ws, "import")(param_hist_D_region, RooFit.Rename(process+"_D"))
getattr(ws, "import")(param_Bkg_D_norm, RooFit.Rename(process+"_D"+"_norm"),RooFit.RecycleConflictNodes())

```
</details>

For the signal region A, create a ```RooParamtricHist``` with each bin made from a ```RooFormulaVar``` relating the C,D,B regions to A via the ABCD formula. 

<details>
<summary> Create RooParametricHist for SR background template  </summary>

```
#Relate SR (A) to control region B via transfer factors
process_AB_region_bins = RooArgList()
TF_list = []
process_AB_region_bins_list = []


#Compute per-bin transfer factor
for i in range(1,histB_pr.GetNbinsX()+1):
    TF_i = RooFormulaVar("TF"+str(i),"Transfer factor C/D bin " + str(i),"(@0/@1)",RooArgList(ws.obj(process+"_C_region_bin_"+str(i)) , ws.obj(process+"_D_region_bin_"+str(i)) ))
    TF_list.append(TF_i)
    bin_AB_i = RooFormulaVar(process+"_AB_region_bin_"+str(i),"Background yield in SR A region bin " + str(i), "@0*@1", RooArgList(TF_i, ws.obj(process+"_B_region_bin_"+str(i)) ))
    process_AB_region_bins_list.append(bin_AB_i)
for binAB_i in process_AB_region_bins_list:
    process_AB_region_bins.add(binAB_i)


#Create parametric histogram for signal region (A)   
param_hist_A_region = RooParametricHist(process+"_A", "Background PDF in A region",variable_z,process_AB_region_bins,histA_pr)
param_bkg_A_norm = RooAddition(process+"_A"+"_norm","Total Number of events from background in A region",process_AB_region_bins)
getattr(ws, "import")(param_hist_A_region, RooFit.Rename(process+"_A"))
getattr(ws, "import")(param_bkg_A_norm, RooFit.Rename(process+"_A"+"_norm"),RooFit.RecycleConflictNodes())

```
</details>

The datacards can be combined then using the usual command:

```combineCards.py mPhi1500_*2018*.txt > combinedExclusion_mPhi1500_2018.txt```

<details>
<summary> Datacard with A,B,C,D regions combined  </summary>

```
Combination of mPhi1500_Catany_2018_CR_B.txt  mPhi1500_Catany_2018_CR_C.txt  mPhi1500_Catany_2018_CR_D.txt  mPhi1500_Catany_2018_SR.txt
imax 4 number of bins
jmax 1 number of processes minus 1
kmax 2 number of nuisance parameters
----------------------------------------------------------------------------------------------------------------------------------
shapes Bkg       ch1       param_ws.root wspace:bkg_B
shapes data_obs  ch1       param_ws.root wspace:data_obs_B
shapes mPhi1500  ch1       param_ws.root wspace:mPhi1500_B
shapes Bkg       ch2       param_ws.root wspace:bkg_C
shapes data_obs  ch2       param_ws.root wspace:data_obs_C
shapes mPhi1500  ch2       param_ws.root wspace:mPhi1500_C
shapes Bkg       ch3       param_ws.root wspace:bkg_D
shapes data_obs  ch3       param_ws.root wspace:data_obs_D
shapes mPhi1500  ch3       param_ws.root wspace:mPhi1500_D
shapes Bkg       ch4       param_ws.root wspace:bkg_A
shapes data_obs  ch4       param_ws.root wspace:data_obs_A
shapes mPhi1500  ch4       param_ws.root wspace:mPhi1500_A
----------------------------------------------------------------------------------------------------------------------------------
bin          ch1    ch2    ch3    ch4  
observation  -1     -1     -1     -1   
----------------------------------------------------------------------------------------------------------------------------------
bin                             ch1       ch1       ch2       ch2       ch3       ch3       ch4       ch4     
process                         mPhi1500  Bkg       mPhi1500  Bkg       mPhi1500  Bkg       mPhi1500  Bkg     
process                         0         1         0         1         0         1         0         1       
rate                            -1        1         -1        1         -1        1         -1        1       
----------------------------------------------------------------------------------------------------------------------------------
BkgRate                 lnN     -         -         -         -         -         -         -         1.05    
lumi                    lnN     1.016     -         1.016     -         1.016     -         1.016     -


```
</details>



## Run Fit
<a id="fit"></a>

From the combined datacard for all the regions, one can run the usual fit diagnostics as follows:

```combine -M FitDiagnostics combinedExclusion_mPhi1500_2018.txt -m 1500 --saveShapes --saveWithUncertainties --saveNormalizations```

Using the output ```higgsCombineTest.FitDiagnostics.mH1500.root```, one can run the script ```utils/mlfitNormsToText.py``` to get the predictions for the normalizations.

<details>
<summary> Normalizations predictions </summary>
```
Channel                                  Process                                Pre-fit              S+B Fit           B-Only Fit
---------------------------------------------------------------------------------------------------------------------------------
ch1                                      mPhi1500                               615.153                0.036                0.000
ch2                                      mPhi1500                               588.446                0.034                0.000
ch3                                      mPhi1500                               233.459                0.014                0.000
ch4                                      mPhi1500                              1563.698                0.092                0.000
ch1                                      Bkg                                 235694.916           235691.655           235690.631
ch2                                      Bkg                                 237436.123           237432.755           237431.725
ch3                                      Bkg                                 382527.975           382533.256           382531.586
ch4                                      Bkg                                 146323.145           144860.251           144857.582

```
</details>

Moreover, one can run the script ``````utils/postFitPlot.py``` to get pre-fit and post-fit plots in the signal region (in the combined datacard ```ch_4```).

![input distributions](docs/post_fit_plots_A.png)

## Produce limits
<a id="limits"></a>

Limits can be computed from the combined datacard for all the regions using the following command (in case of asymptotic limits):

```combine -M -n combinedExclusion_mPhi1500_2018 -m 1500  combinedExclusion_mPhi1500_2018.txt  2>&1 | tee  asymp_limits_mPhi1500_2018.txt```

Both the observed (from nominal Monte Carlo) and the expected limits are computed for each mass point. The same exercise can be repeated generating a workspace where the control regions are depleted from the signal (see datacards [here](https://github.com/cesarecazzaniga/combine_tutorial_ABCD_rooParametricHist/tree/main/datacards/no_sgn_CRs) ), and re-running the limits. This should give a hint of how much the signal contamination in the control regions is worsening the limits.  

<img src="docs/limits.png" width="600" />

As we can see the expected limit without signal in the control regions is better compared to the one taking into account the signal, showing that in this example there is an impact from the signal contamination of the control regions affecting the final sensitivity. Instead, the observed line is showing the impact of the non-closure of the ABCD method: mainly the background is overestimated, thus leading to slightly worse expected limits (equivalent to an underfluctuation of the data).

