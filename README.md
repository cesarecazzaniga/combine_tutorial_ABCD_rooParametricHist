# combine_tutorial_ABCD_rooParametricHist
tutorial for Combine using RooParamertricHist to perform the ABCD method

## Introduction
The goal of this tutorial is to exemplify the usage of ```RooParametricHist``` in [CMS Combine](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/) to implement a bin-by-bin ABCD method.
In this tutorial we will work with a toy example that could resamble a real physics analysis case. We consider the search for a BSM particle $\Phi$ with a mass range between 1500 and 5000 GeV that leads some excess in the tails of an observable $z$ (which could be $p_{T,\mathrm{miss}}$ ). We assume that we have found two uncorrelated discriminating features $x$ and $y$ that can be used to build the ABCD plane (the regions A,B,C,D will be defined by cutting on $x,y$), and we assume that $z$ is uncorrelated with respect to these two features. In this way, binning the variable $z$ in the same way in the regions A,B,C,D, per-bin transfer factors in the $z$ variable can be derived with the ABCD method to obtain the estimate of the background in the signal region.

The tutorial has 4 main parts:

1. [Generate input data](#inputs)
2. [Prepare Combine datacards](#datacards)
3. [Run fit](#fit)
4. [Produce limits](#limits)

## Generate input data
<a id="inputs"></a>
The histograms for the $z$ observable in the different regions A,B,C,D can be produced using the [jupyter notebook](https://github.com/cesarecazzaniga/combine_tutorial_ABCD_rooParametricHist/blob/main/ABCD_combine_tutorial_input_histograms.ipynb). In the notebook the expected rates for different signal hypothesis (as a function of $\Phi$ mass $\m_{\Phi} \in \{1500, 2000, 3000, 4000, 5000 \}$ GeV) and the background yields are specified, as well as the distributions in $x,y,z$ of the signals and backgrounds. In $x,y$, the signal and the background are assumed to be distributed as multivariate gaussians, with the background centred at $(0,2,0.2)$ in $(x,y)$ while the signals centred in the upper-right corner of the plane ($x,y>0.5$). For the $z$ feature, the background and the signal distributions are sampled from an exponential, for the signal the tails of the exponential get enhance with the mass parameter $\m_{\Phi}$. 

![input distributions](docs/inputs.png)

## Prepare Combine datacards 
<a id="datacards"></a>

## Run Fit
<a id="fit"></a>

## Produce limits
<a id="limits"></a>
