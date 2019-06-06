#!/usr/bin/python

"""
Plotting file for computational model Herice C. and Sakata S. (2019)

Sleep/wake regulation model and synapses alterations.
Original model from Costa et al. (2016) and Diniz Behn et al. (2012).

Charlotte HERICE - January 2019
"""

import numpy as np
import os
import matplotlib.pylab as plt


################################################
# Extracting simulations data and plot results
################################################

class SleepPlots(object):

	def __init__(self, simDuration, dirName, simNumber, alterationSite, alterationTitle, toShow):
		"""
			simDuration: simulation duration in hours
			dirName: main directory for synaptic alteration condition
			simNumber: current simulation number
			alterationSite: name of the altered synapse 
			alterationTitle: figure title with the name of the altered synapse 
			toShow: "y" or "n" if the figure will be displayed anf saved or just saved
		"""
		print("init_Plot")
		self.simDuration = simDuration
		self.dirName = dirName
		self.simNumber = simNumber
		self.alterationSite = alterationSite
		self.alterationTitle = alterationTitle
		self.toShow = toShow
		self.lw = 4
		self.alphaVal = 0.2

		self.loadResults()
		self.setAxisLabels()
		self.makePlots()


	def testFunc2(self):
		print("func_Plot")


	def loadResults(self):
		"""
		Load data from result files
		"""

		self.dataDirName_ctrl = self.dirName + "/Alterations_ctrl_" + str(self.simDuration) + "h/Sim" + str(self.simNumber)

		self.Time 		= np.load(self.dataDirName_ctrl  + "/time_Herice_Model_Alteration_" + self.dirName 	+ "_ctrl_sim" + str(self.simNumber) + ".npy")

		self.f_R_ctrl 	= np.load(self.dataDirName_ctrl  + "/f_R_Herice_Model_Alteration_" 	+ self.dirName 	+ "_ctrl_sim" + str(self.simNumber) + ".npy")
		self.f_N_ctrl 	= np.load(self.dataDirName_ctrl  + "/f_N_Herice_Model_Alteration_" 	+ self.dirName 	+ "_ctrl_sim" + str(self.simNumber) + ".npy")
		self.f_W_ctrl 	= np.load(self.dataDirName_ctrl  + "/f_W_Herice_Model_Alteration_" 	+ self.dirName 	+ "_ctrl_sim" + str(self.simNumber) + ".npy")
		self.c_NXi_ctrl = np.load(self.dataDirName_ctrl  + "/C_NXi_Herice_Model_Alteration_" + self.dirName + "_ctrl_sim" + str(self.simNumber) + ".npy")
		self.c_WXi_ctrl = np.load(self.dataDirName_ctrl  + "/C_WXi_Herice_Model_Alteration_" + self.dirName + "_ctrl_sim" + str(self.simNumber) + ".npy")
		self.c_RXe_ctrl = np.load(self.dataDirName_ctrl  + "/C_RXe_Herice_Model_Alteration_" + self.dirName + "_ctrl_sim" + str(self.simNumber) + ".npy")
		self.h_ctrl   	= np.load(self.dataDirName_ctrl  + "/h_Herice_Model_Alteration_" 	+ self.dirName 	+ "_ctrl_sim" + str(self.simNumber) + ".npy")

		self.dataDirName = self.dirName + "/Alterations_" + self.alterationSite + "_" + str(self.simDuration) + "h/Sim" + str(self.simNumber)

		self.f_R_alt 	= np.load(self.dataDirName  + "/f_R_Herice_Model_Alteration_" 	+ self.dirName + "_" + self.alterationSite + "_sim" + str(self.simNumber) + ".npy")
		self.f_N_alt 	= np.load(self.dataDirName  + "/f_N_Herice_Model_Alteration_" 	+ self.dirName + "_" + self.alterationSite + "_sim" + str(self.simNumber) + ".npy")
		self.f_W_alt 	= np.load(self.dataDirName  + "/f_W_Herice_Model_Alteration_" 	+ self.dirName + "_" + self.alterationSite + "_sim" + str(self.simNumber) + ".npy")
		self.c_NXi_alt 	= np.load(self.dataDirName  + "/C_NXi_Herice_Model_Alteration_" + self.dirName + "_" + self.alterationSite + "_sim" + str(self.simNumber) + ".npy")
		self.c_WXi_alt 	= np.load(self.dataDirName  + "/C_WXi_Herice_Model_Alteration_" + self.dirName + "_" + self.alterationSite + "_sim" + str(self.simNumber) + ".npy")
		self.c_RXe_alt 	= np.load(self.dataDirName  + "/C_RXe_Herice_Model_Alteration_" + self.dirName + "_" + self.alterationSite + "_sim" + str(self.simNumber) + ".npy")
		self.h_alt   	= np.load(self.dataDirName  + "/h_Herice_Model_Alteration_"   	+ self.dirName + "_" + self.alterationSite + "_sim" + str(self.simNumber) + ".npy")


	def setAxisLabels(self):
		"""
		Customise x-axis labels with hours
		"""
		# For axis labels 
		self.hoursNb = []
		self.hoursId = []
		self.cpt = 0

		for i in range(len(self.Time)):
			if (int(self.Time[i])%3600 == 0):
				if (self.simDuration == 24):
					if (int(self.cpt) in [0,4,8,12,16,20,24]):
						self.hoursNb.append(self.Time[i])
						self.hoursId.append(str(cpt))
					self.cpt += 1
				if (self.simDuration == 48):
					if (int(self.cpt) in [0,4,8,12,16,20,24,28,32,36,40,44,48]):
						self.hoursNb.append(self.Time[i])
						self.hoursId.append(str(cpt))
					self.cpt += 1


	def buildHypnogram(self, c_WXi, c_RXe):
		"""
		Building hypnograms depending the WXi and RXe concentrations.
		Returns a table containing the hypnogram values (1 for NREM, 2 for REM and 3 for Wake)
			c_WXi: WXi concentration
			c_RXe: RXe concentration
		"""

		sleepStates = {"Wake" : [], "REM": [], "NREM": []}
		hypno = []

		cpt_Wake = 0
		cpt_REM = 0
		cpt_NREM = 0

		for i in range(len(self.Time)):
			if (c_WXi[i] < 0.4): # NREM
				if (c_RXe[i] > 0.4): # REM
					hypno.append(2)
					sleepStates["REM"].append(self.Time[i]) 
					cpt_REM += 1
					# print("REM at ", Time[i], "s")
				else:# NREM
					hypno.append(1)
					sleepStates["NREM"].append(self.Time[i]) 
					cpt_NREM += 1
					# print("NREM at ", Time[i], "s")
			else: # Wake
				hypno.append(3)
				sleepStates["Wake"].append(self.Time[i])
				cpt_Wake += 1 
				# print("Wake at ", Time[i], "s")
		return hypno


	def makePlots(self):
		"""
		Preparation of the plots for the final figure
		"""
		self.hypno_ctrl = self.buildHypnogram(self.c_WXi_ctrl, self.c_RXe_ctrl)
		self.hypno_alt = self.buildHypnogram(self.c_WXi_alt, self.c_RXe_alt)

		self.buildFullPlots()


	def buildFullPlots(self):
		"""
		Plotting the final figure with firing rates, concentrations and hypnogram
		"""

		plt.figure(figsize=(14, 7))
		supTitle = "State dependency of neural populations activities and neurotransmitters concentrations"
		plt.suptitle(supTitle, weight="bold", size=14)

		plt.subplot(311)
		plt.plot(self.Time, self.f_W_alt, label="Wake-promoting", color="darkorange", linewidth=self.lw)
		plt.plot(self.Time, self.f_N_alt, label="NREM-promoting", color="limegreen", 	linewidth=self.lw)
		plt.plot(self.Time, self.f_R_alt, label="REM-promoting", 	color="darkblue", linewidth=self.lw)
		plt.plot(self.Time, self.f_W_ctrl, color="darkorange", 	linewidth=self.lw, alpha=self.alphaVal, linestyle='--')
		plt.plot(self.Time, self.f_N_ctrl, color="limegreen", 	linewidth=self.lw, alpha=self.alphaVal, linestyle='--')
		plt.plot(self.Time, self.f_R_ctrl, color="darkblue", 		linewidth=self.lw, alpha=self.alphaVal, linestyle='--')
		plt.ylabel("Population activity (Hz)", size=11, weight="bold")
		plt.title(self.alterationTitle, weight="bold", size=13)
		plt.legend(loc=6, prop={'size': 13})
		plt.xticks(self.hoursNb, self.hoursId)
		plt.yticks(size=12, weight="bold")

		plt.subplot(312)
		plt.plot(self.Time, self.c_WXi_alt, label="WXi", 				color="sandybrown", linewidth=self.lw)
		plt.plot(self.Time, self.c_NXi_alt, label="NXi", 				color="chartreuse", linewidth=self.lw)
		plt.plot(self.Time, self.c_RXe_alt, label="RXe", 				color="blue", 		linewidth=self.lw)
		plt.plot(self.Time, self.h_alt, 	label="Homeostatic Force", 	color="violet", 	linewidth=self.lw)
		plt.plot(self.Time, self.c_WXi_ctrl, color="sandybrown", 	linewidth=self.lw, alpha=self.alphaVal, linestyle='--')
		plt.plot(self.Time, self.c_NXi_ctrl, color="chartreuse", 	linewidth=self.lw, alpha=self.alphaVal, linestyle='--')
		plt.plot(self.Time, self.c_RXe_ctrl, color="blue", 			linewidth=self.lw, alpha=self.alphaVal, linestyle='--')
		plt.plot(self.Time, self.h_ctrl,   color="violet", 		linewidth=self.lw, alpha=self.alphaVal, linestyle='--')
		plt.ylabel("Concentration (aU)", size=11, weight="bold")
		plt.legend(loc=6, prop={'size': 13})
		plt.xticks(self.hoursNb, self.hoursId)
		plt.yticks(size=12, weight="bold")

		plt.subplot(313)
		plt.plot(self.Time, self.hypno_alt, 	label="Hypnogram", color="black", linewidth=2)
		plt.plot(self.Time, self.hypno_ctrl, 	color="black", 	linewidth=self.lw/2, alpha=self.alphaVal, linestyle='--')
		plt.legend(loc=6, prop={'size': 13})
		plt.xticks(self.hoursNb, self.hoursId, size=12, weight="bold")
		plt.yticks([1, 2, 3], ["NREM", "REM", "Wake"], size=11, weight="bold")
		plt.xlabel("Time (h)", size=12, weight="bold")

		plt.subplots_adjust(left=0.05, bottom=0.07, right=0.99, top=0.92, wspace=0.19, hspace=0.05)

		if (self.toShow == "y"):
			plt.savefig(self.dataDirName + "/Activities_Alterations_" + self.dirName + "_" + self.alterationSite + "_sim" + str(self.simNumber) + ".jpg", dpi=(500))
			plt.show()
		elif (self.toShow == "n"):
			plt.savefig(self.dataDirName + "/Activities_Alterations_" + self.dirName + "_" + self.alterationSite + "_sim" + str(self.simNumber) + ".jpg", dpi=(500))







