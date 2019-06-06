#!/usr/bin/python

"""
Main file for the computational model Herice C. and Sakata S. (2019)

Sleep/wake regulation model and synapses alterations.
Original model from Costa et al. (2016) and Diniz Behn et al. (2012).

Charlotte HERICE - January 2019
"""

import os
import sleepCompModel
import sleepPlot

# os.path.join()

print("--")

simDuration = 16
nbSims = 1
toShow = "y"

alterationSite = "ctrl"
dirName = "Control"
alterationTitle = "Control conditions"

g_RRe = 1.6
g_RWe = 1.0
g_WNi = -2.0
g_WRi = -4.0
g_NRi = -1.3
g_NWi = -1.68
	
for simNumber in range(1, nbSims+1):
	sleepCompModel.RunSim(simDuration, simNumber, alterationSite, dirName, g_RRe, g_RWe, g_WNi, g_WRi, g_NRi, g_NWi) 
	sleepPlot.SleepPlots(simDuration, dirName, simNumber, alterationSite, alterationTitle, toShow)


dirName = "Lesion"
alterationTitle = "Alteration REM to REM (full lesion)"

# alterationSite = "ctrl"

# g_RRe = 1.6
# g_RWe = 1.0
# g_WNi = -2.0
# g_WRi = -4.0
# g_NRi = -1.3
# g_NWi = -1.68
	
# for simNumber in range(1, nbSims+1):
# 	sleepCompModel.RunSim(simDuration, simNumber, alterationSite, dirName, g_RRe, g_RWe, g_WNi, g_WRi, g_NRi, g_NWi) 
# 	sleepPlot.SleepPlots(simDuration, dirName, simNumber, alterationSite, alterationTitle, toShow)

# alterationSite = "g_RRe"

# g_RRe = 0
# g_RWe = 1.0
# g_WNi = -2.0
# g_WRi = -4.0
# g_NRi = -1.3
# g_NWi = -1.68
	
# for simNumber in range(1, nbSims+1):
# 	sleepCompModel.RunSim(simDuration, simNumber, alterationSite, dirName, g_RRe, g_RWe, g_WNi, g_WRi, g_NRi, g_NWi) 
# 	sleepPlot.SleepPlots(simDuration, dirName, simNumber, alterationSite, alterationTitle, toShow)


# sleepCompModel.SleepRegulation.testFunc1()


# sleepPlot.SleepPlots.testFunc2()

# print("h")






