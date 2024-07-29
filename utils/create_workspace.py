
## Create workspace storing information with RooParametricHist

import ROOT
from ROOT import RooRealVar, RooDataHist, RooArgList, RooWorkspace, RooParametricHist, RooFit, RooAddition, RooFormulaVar
import os


def __get_histograms_regions(process, input_file):
    hist_nameA = "A/" + "h_" + process + "_A"
    hist_nameB = "B/" + "h_" + process + "_B"
    hist_nameC = "C/" + "h_" + process + "_C"
    hist_nameD = "D/" + "h_" + process + "_D"
    print ("Reading histogram: ", hist_nameA)
    print ("Reading histogram: ", hist_nameB)
    print ("Reading histogram: ", hist_nameC)
    print ("Reading histogram: ", hist_nameD)
    histA = input_file.Get(hist_nameA)
    histA.SetDirectory(0)
    histB = input_file.Get(hist_nameB)
    histB.SetDirectory(0)
    histC = input_file.Get(hist_nameC)
    histC.SetDirectory(0)
    histD = input_file.Get(hist_nameD)
    histD.SetDirectory(0)

    return histA , histB, histC, histD

#main code starting here
def main():

    #get current directory
    current_directory = os.getcwd()
    card_output_directory = current_directory + "/example_cards/"
    input_file_bkg = ROOT.TFile.Open(current_directory+ "/generated_histograms/background.root")
    input_file_sgn = ROOT.TFile.Open(current_directory+ "/generated_histograms/mPhi_1500.root")
    signal = "mPhi_1500"

    #Output file and workspace
    output_file_ws =  ROOT.TFile(card_output_directory+"param_ws.root","RECREATE")
    ws = RooWorkspace("wspace","wspace")

    #Define a RooRealVar for the observable z to fit
    variable_z = RooRealVar( "z", "z", 200, 14000, "GeV")

    #Save data in RooDataHist (here assume data is background)
    histA_obs , histB_obs, histC_obs, histD_obs =  __get_histograms_regions("bkg", input_file_bkg)

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
    histA_sgn , histB_sgn, histC_sgn, histD_sgn =  __get_histograms_regions("sgn", input_file_sgn)
    histSgn_A = RooDataHist(signal+"_A", "Sgn Data region A",  RooArgList(variable_z), histA_sgn, 1.)
    histSgn_B = RooDataHist(signal+"_B", "Sgn Data region B",  RooArgList(variable_z), histB_sgn, 1.)
    histSgn_C = RooDataHist(signal+"_C", "Sgn Data region C",  RooArgList(variable_z), histC_sgn, 1.)
    histSgn_D = RooDataHist(signal+"_D", "Sgn Data region D",  RooArgList(variable_z), histD_sgn, 1.)

    #Import signals in workspace
    getattr(ws, "import")(histSgn_A, RooFit.Rename(signal+"_A"))
    getattr(ws, "import")(histSgn_B, RooFit.Rename(signal+"_B"))
    getattr(ws, "import")(histSgn_C, RooFit.Rename(signal+"_C"))
    getattr(ws, "import")(histSgn_D, RooFit.Rename(signal+"_D"))

    #here we define the background histograms from "data" (which in our case is equal to the background), they will be used to build the parametric histograms  
    histA_pr , histB_pr, histC_pr, histD_pr =  __get_histograms_regions("bkg", input_file_bkg)        

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
        bin_B_i = RooRealVar("Bkg_B_region_bin_"+str(i),"Background yield in control region B bin " + str(i),histB_obs.GetBinContent(i),0.,2.0*histB_obs.GetBinContent(i))
        process_B_region_bins_list.append(bin_B_i)


    for idx,binB_i in enumerate(process_B_region_bins_list):
        process_B_region_bins.add(binB_i)

    #Add yields in C and D Region as RooRealVar in RooArgList (C and D regions are used to compute the transfer factor)
    for i in range(1,histC_obs.GetNbinsX()+1):
        bin_C_i = RooRealVar("Bkg_C_region_bin_"+str(i),"Background yield in control region C bin " + str(i),histC_obs.GetBinContent(i),0.,2.0*histC_obs.GetBinContent(i))
        process_C_region_bins_list.append(bin_C_i)

    for idx,binC_i in enumerate(process_C_region_bins_list):
        process_C_region_bins.add(binC_i)

    for i in range(1,histD_obs.GetNbinsX()+1):
        bin_D_i = RooRealVar("Bkg_D_region_bin_"+str(i),"Background yield in control region D bin " + str(i),histD_obs.GetBinContent(i),0.,2.0*histD_obs.GetBinContent(i))
        process_D_region_bins_list.append(bin_D_i)

    for idx,binD_i in enumerate(process_D_region_bins_list):
        process_D_region_bins.add(binD_i)


    #Parametric histogram for control region B (transfering region, to be related via transfer factor to SR)
    param_hist_B_region = RooParametricHist("Bkg_B", "Background PDF in B region",variable_z,process_B_region_bins,histB_pr)
    param_Bkg_B_norm = RooAddition("Bkg_B"+"_norm","Total Number of events from background in control region B",process_B_region_bins)
    getattr(ws, "import")(param_hist_B_region, RooFit.Rename("Bkg_B"))
    getattr(ws, "import")(param_Bkg_B_norm, RooFit.Rename("Bkg_B"+"_norm"),RooFit.RecycleConflictNodes())

    #Parametric histograms for control regions C (used to compute transfer factor) 
    param_hist_C_region = RooParametricHist("Bkg_C", "Background PDF in C region",variable_z,process_C_region_bins,histC_pr)
    param_Bkg_C_norm = RooAddition("Bkg_C"+"_norm","Total Number of events from background in control region C",process_C_region_bins)
    getattr(ws, "import")(param_hist_C_region, RooFit.Rename("Bkg_C"))
    getattr(ws, "import")(param_Bkg_C_norm, RooFit.Rename("Bkg_C"+"_norm"),RooFit.RecycleConflictNodes())

    #Parametric histograms for control regions D (used to compute transfer factor)
    param_hist_D_region = RooParametricHist("Bkg_D", "Background PDF in D region",variable_z,process_D_region_bins,histD_pr)
    param_Bkg_D_norm = RooAddition("Bkg_D"+"_norm","Total Number of events from background in control region D",process_D_region_bins)
    getattr(ws, "import")(param_hist_D_region, RooFit.Rename("Bkg_D"))
    getattr(ws, "import")(param_Bkg_D_norm, RooFit.Rename("Bkg_D"+"_norm"),RooFit.RecycleConflictNodes())

    #Relate SR (A) to control region B via transfer factors
    process_AB_region_bins = RooArgList()
    TF_list = []
    process_AB_region_bins_list = []


    #Compute per-bin transfer factor
    for i in range(1,histB_pr.GetNbinsX()+1):
        TF_i = RooFormulaVar("TF"+str(i),"Transfer factor C/D bin " + str(i),"(@0/@1)",RooArgList(ws.obj("Bkg_C_region_bin_"+str(i)) , ws.obj("Bkg_D_region_bin_"+str(i)) ))
        TF_list.append(TF_i)
        bin_AB_i = RooFormulaVar("Bkg_AB_region_bin_"+str(i),"Background yield in SR A region bin " + str(i), "@0*@1", RooArgList(TF_i, ws.obj("Bkg_B_region_bin_"+str(i)) ))
        process_AB_region_bins_list.append(bin_AB_i)
    for binAB_i in process_AB_region_bins_list:
        process_AB_region_bins.add(binAB_i)


    #Create parametric histogram for signal region (A)   
    param_hist_A_region = RooParametricHist("Bkg_A", "Background PDF in A region",variable_z,process_AB_region_bins,histB_pr)
    param_bkg_A_norm = RooAddition("Bkg_A"+"_norm","Total Number of events from background in A region",process_AB_region_bins)
    getattr(ws, "import")(param_hist_A_region, RooFit.Rename("Bkg_A"))
    getattr(ws, "import")(param_bkg_A_norm, RooFit.Rename("Bkg_A"+"_norm"),RooFit.RecycleConflictNodes())

    #Save workspace in output file
    output_file_ws.cd()
    ws.Write()
    output_file_ws.Close()



if __name__ == "__main__":

    main()






