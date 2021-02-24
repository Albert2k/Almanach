import numpy as np
from scipy import stats as scistats
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import collections
import matplotlib.mlab as mlab
import os
import math
import latex_tabellen
import latex_figure

#-----------------------------------------------------------------------------------

def latex_kurslücken(daten, basiswert):

	list_header = latex_ks_header()
	list_ks = latex_ks(daten)

	list_latex = list_header
	for i in list_ks:
		list_latex.append(i)

	return list_latex

#-----------------------------------------------------------------------------------

def latex_ks_header():

	list = []

	list.append(r'%%%%%%%%%%%%% Beginn Kapitel Kurslücken %%%%%%%%%%%%%%%%%')
	list.append(r'\chapter{Kurslücken}')
	list.append(r'')

	return list

#-----------------------------------------------------------------------------------

def latex_ks(daten):

	ks = kurslücken(daten[1],daten[3],daten[2],daten[4],daten[5])
	print(ks)
	list = []

	list.append(r' blablabla')
	list.append(r'')



	return list

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------

def kurslücken(ope, low, high, close, differenz):
	
	pos_kur = 0
	neg_kur = 0
	pos_kl_li = []
	neg_kl_li = []
	pos_kl_open = 0
	neg_kl_open = 0
	schritte = 5
	schrittlänge = 0.2
	schritte2 = 4
	schrittlänge2 = 0.5

	anz_pos = []
	for i in range(2):
		anz_pos += [[]]
		for j in range(schritte + 1):
			anz_pos[i] += [0]

	perf_pos = []

	for i in range(3):
		perf_pos += [[]]
		for l in range(2):
			perf_pos[i] += [[]]
			for j in range(schritte + 1):
				perf_pos[i][l] += [[]]
				for k in range((schritte2 + 1)*2+1):
					perf_pos[i][l][j] += [0]

	anz_neg = []

	for i in range(2):
		anz_neg += [[]]
		for j in range(schritte + 1):
			anz_neg[i] += [0]

	perf_neg = []

	for i in range(3):
		perf_neg += [[]]
		for l in range(2):
			perf_neg[i] += [[]]
			for j in range(schritte + 1):
				perf_neg[i][l] += [[]]
				for k in range((schritte2+1)*2+1):
					perf_neg[i][l][j] += [0]

	verh_ks_gesch = []

	for i in range(2):
		verh_ks_gesch += [[]]
		for j in range(5):
			verh_ks_gesch[i] += [0]

	nb_ks = []

	for i in range(2):
		nb_ks += [[]]
		for j in range((schritte2+1)*2+1):
			nb_ks[i] += [0]

	for i in range(len(ope)-2):
		if ope[i+1] > close[i]:
			if low[i+1] < close[i]:
				gro = (close[i+1]-close[i])/close[i]*100
				if gro < 0:
					schwelle3 = - 10000
					schwelle4 = - schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro < schwelle4 and gro >= schwelle3:
							nb_ks[0][l] = nb_ks[0][l] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
				elif gro == 0:
					nb_ks[0][schritte2+1] = nb_ks[0][schritte2+1] + 1
				else:
					schwelle5 = 10000
					schwelle6 = + schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro <= schwelle5 and gro > schwelle6:
							nb_ks[0][(schritte2+1)*2-l] = nb_ks[0][(schritte2+1)*2-l] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
			pos_kur = pos_kur + 1
			rand = close[i]			
			ab = 0
			j = 1
			while ab == 0:
				if i + j < len(ope):
					if rand < low[i+j]:
						j = j + 1

						if j == 2:
							große_ab = (ope[i+1]-close[i])
							rücklauf_ab = (ope[i+1] - low[i+1])
							verh_ks = rücklauf_ab/große_ab
							sch1_ks = 0
							sch2_ks = 0.2
							for k in range(5):
								if sch1_ks <= verh_ks and sch2_ks > verh_ks:
									verh_ks_gesch[0][k] += 1
									sch1_ks = sch2_ks
									sch2_ks = sch2_ks + 0.2
								sch1_ks = sch2_ks
								sch2_ks = sch2_ks + 0.2

						if j == 2:
							gro = (ope[i+1]-close[i])/ope[i]*100
							schwelle1 = 10000
							schwelle2 = schritte * schrittlänge
							for k in range(schritte+1):
								if gro <= schwelle1 and gro > schwelle2:
									anz_pos[0][k] = anz_pos[0][k] + 1
									schwelle1 = schwelle2
									schwelle2 = schwelle2-schrittlänge
									if differenz[i+2] < 0:
										schwelle3 = - 10000
										schwelle4 = - schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+2] < schwelle4 and differenz[i+2] >= schwelle3:
												perf_pos[0][0][k][l] = perf_pos[0][0][k][l] + 1
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
											else:
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
									elif differenz[i+2] == 0:
										perf_pos[0][0][k][schritte2+1] = perf_pos[0][0][k][schritte2+1] + 1
									else:
										schwelle5 = 10000
										schwelle6 = + schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+2] <= schwelle5 and differenz[i+2] > schwelle6:
												perf_pos[0][0][k][(schritte2+1)*2-l] = perf_pos[0][0][k][(schritte2+1)*2-l] + 1
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2
											else:
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2
								else:
									schwelle1 = schwelle2
									schwelle2 = schwelle2-schrittlänge
					elif rand >= low[i+j]:
						ab = 1
						pos_kl_li = pos_kl_li + [j-1]
						if j == 1:
							gro = (ope[i+1]-close[i])/ope[i]*100
							schwelle1 = 10000
							schwelle2 = schritte * schrittlänge
							for k in range(schritte+1):
								if gro <= schwelle1 and gro > schwelle2:
									anz_pos[1][k] = anz_pos[1][k] + 1
									schwelle1 = schwelle2
									schwelle2 = schwelle2-schrittlänge
									if differenz[i+2] < 0:
										schwelle3 = - 10000
										schwelle4 = - schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+2] < schwelle4 and differenz[i+2] >= schwelle3:
												perf_pos[0][1][k][l] = perf_pos[0][1][k][l] + 1
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
											else:
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
									elif differenz[i+2] == 0:
										perf_pos[0][1][k][schritte2+1] = perf_pos[0][1][k][schritte2+1] + 1
									else:
										schwelle5 = 10000
										schwelle6 = + schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+2] <= schwelle5 and differenz[i+2] > schwelle6:
												perf_pos[0][1][k][(schritte2+1)*2-l] = perf_pos[0][1][k][(schritte2+1)*2-l] + 1
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2
											else:
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2
								else:
									schwelle1 = schwelle2
									schwelle2 = schwelle2-schrittlänge
				else:
					ab = 1
					pos_kl_li = pos_kl_li + [j-1]
					pos_kl_open = pos_kl_open + 1	
					if j == 2:
						gro = (ope[i+1]-close[i])/ope[i]*100
						schwelle1 = 10000
						schwelle2 = + schritte * schrittlänge
						for k in range(schritte+1):
							if gro <= schwelle1 and gro > schwelle2:
								anz_pos[1][k] = anz_pos[1][k] + 1
								schwelle1 = schwelle2
								schwelle2 = schwelle2-schrittlänge
								if differenz[i+2] < 0:
									schwelle3 = - 10000
									schwelle4 = - schritte2 * schrittlänge2
									for l in range(schritte2+1):
										if differenz[i+2] < schwelle4 and differenz[i+2] >= schwelle3:
											perf_pos[0][0][k][l] = perf_pos[0][0][k][l] + 1
											schwelle3 = schwelle4
											schwelle4 = schwelle4 + schrittlänge2
										else:
											schwelle3 = schwelle4
											schwelle4 = schwelle4 + schrittlänge2
								elif differenz[i+2] == 0:
									perf_pos[0][0][k][schritte2+1] = perf_pos[0][0][k][schritte2+1] + 1
								else:
									schwelle5 = 10000
									schwelle6 = + schritte2 * schrittlänge2
									for l in range(schritte2+1):
										if differenz[i+2] <= schwelle5 and differenz[i+2] > schwelle6:
											perf_pos[0][0][k][(schritte2+1)*2-l] = perf_pos[0][0][k][(schritte2+1)*2-l] + 1
											schwelle5 = schwelle6
											schwelle6 = schwelle6-schrittlänge2
										else:
											schwelle5 = schwelle6
											schwelle6 = schwelle6-schrittlänge2
							else:
								schwelle1 = schwelle2
								schwelle2 = schwelle2-schrittlänge

		elif ope[i+1] < close[i]:
			if high[i+1] > close[i]:
				gro = (close[i+1]-close[i])/low[i]*100
				if gro < 0:
					schwelle3 = - 10000
					schwelle4 = - schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro < schwelle4 and gro >= schwelle3:
							nb_ks[1][l] = nb_ks[1][l] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
				elif gro == 0:
					nb_ks[1][schritte2+1] = nb_ks[1][schritte2+1] + 1
				else:
					schwelle5 = 10000
					schwelle6 = + schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro <= schwelle5 and gro > schwelle6:
							nb_ks[1][(schritte2+1)*2-l] = nb_ks[1][(schritte2+1)*2-l] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2

			neg_kur = neg_kur + 1
			rand = close[i]
			ab = 0
			j = 1
			while ab == 0:
				if i + j < len(ope):
					if rand > high[i+j]:
						j = j + 1

						if j == 2:
							große_ab = (close[i] - ope[i+1])
							rücklauf_ab = (high[i+1] - ope[i+1])
							verh_ks = rücklauf_ab/große_ab
							sch1_ks = 0
							sch2_ks = 0.2
							for k in range(5):
								if sch1_ks <= verh_ks and sch2_ks > verh_ks:
									verh_ks_gesch[1][k] += 1
									sch1_ks = sch2_ks
									sch2_ks = sch2_ks + 0.2
								sch1_ks = sch2_ks
								sch2_ks = sch2_ks + 0.2

						if j == 2:
							gro = (ope[i+1]-close[i])/ope[i]*100
							schwelle1 = -10000
							schwelle2 = -schritte * schrittlänge
							for k in range(schritte+1):
								if gro < schwelle2 and gro >= schwelle1:
									print(i)
									anz_neg[0][k] = anz_neg[0][k] + 1
									schwelle1 = schwelle2
									schwelle2 = schwelle2+schrittlänge
									if differenz[i+2] < 0:
										schwelle3 = - 10000
										schwelle4 = - schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+2] < schwelle4 and differenz[i+2] >= schwelle3:
												perf_neg[0][0][k][l] = perf_neg[0][0][k][l] + 1
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
											else:
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
									elif differenz[i+2] == 0:
										perf_neg[0][0][k][schritte2+1] = perf_neg[0][0][k][schritte2+1] + 1
									else:
										schwelle5 = 10000
										schwelle6 = + schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+2] <= schwelle5 and differenz[i+2] > schwelle6:
												perf_neg[0][0][k][(schritte2+1)*2-l] = perf_neg[0][0][k][(schritte2+1)*2-l] + 1
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2
											else:
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2
								else:
									schwelle1 = schwelle2
									schwelle2 = schwelle2+schrittlänge
					elif rand <= high[i+j]:
						ab = 1
						neg_kl_li = neg_kl_li + [j-1]
						if j == 1:
							gro = (-close[i] + ope[i+1])/ope[i]*100
							schwelle1 = -10000
							schwelle2 = -schritte * schrittlänge
							for k in range(schritte+1):
								if gro < schwelle2 and gro >= schwelle1:
									anz_neg[1][k] = anz_neg[1][k] + 1
									schwelle1 = schwelle2
									schwelle2 = schwelle2+schrittlänge
									if differenz[i+2] < 0:
										schwelle3 = - 10000
										schwelle4 = - schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+2] < schwelle4 and differenz[i+2] >= schwelle3:
												perf_neg[0][1][k][l] = perf_neg[0][1][k][l] + 1
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
											else:
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
									elif differenz[i+2] == 0:
										perf_neg[0][1][k][schritte2+1] = perf_neg[0][1][k][schritte2+1] + 1
									else:
										schwelle5 = 10000
										schwelle6 = + schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+2] <= schwelle5 and differenz[i+2] > schwelle6:
												perf_neg[0][1][k][(schritte2+1)*2-l] = perf_neg[0][1][k][(schritte2+1)*2-l] + 1
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2
											else:
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2
								else:
									schwelle1 = schwelle2
									schwelle2 = schwelle2+schrittlänge
				else:
					ab = 1
					neg_kl_li = neg_kl_li + [j-1]
					neg_kl_open = neg_kl_open + 1
					if j == 2:
						gro = (-close[i] + ope[i+1])/ope[i]*100
						schwelle1 = -10000
						schwelle2 = -schritte * schrittlänge
						for k in range(schritte+1):
							if gro < schwelle2 and gro >= schwelle1:
								anz_neg[0][k] = anz_neg[0][k] + 1
								schwelle1 = schwelle2
								schwelle2 = schwelle2+schrittlänge
								if differenz[i+2] < 0:
									schwelle3 = - 10000
									schwelle4 = - schritte2 * schrittlänge2
									for l in range(schritte2+1):
										if differenz[i+2] < schwelle4 and differenz[i+2] >= schwelle3:
											perf_neg[0][0][k][l] = perf_neg[0][0][k][l] + 1
											schwelle3 = schwelle4
											schwelle4 = schwelle4 + schrittlänge2
										else:
											schwelle3 = schwelle4
											schwelle4 = schwelle4 + schrittlänge2
								elif differenz[i+2] == 0:
									perf_neg[0][0][k][schritte2+1] = perf_neg[0][0][k][schritte2+1] + 1
								else:
									schwelle5 = 10000
									schwelle6 = + schritte2 * schrittlänge2
									for l in range(schritte2+1):
										if differenz[i+2] <= schwelle5 and differenz[i+2] > schwelle6:
											perf_neg[0][0][k][(schritte2+1)*2-l] = perf_neg[0][0][k][(schritte2+1)*2-l] + 1
											schwelle5 = schwelle6
											schwelle6 = schwelle6-schrittlänge2
										else:
											schwelle5 = schwelle6
											schwelle6 = schwelle6-schrittlänge2
							else:
								schwelle1 = schwelle2
								schwelle2 = schwelle2+schrittlänge

	pos_kl_lä = []
	pos_kl_anz = []
	neg_kl_lä = []
	neg_kl_anz = []

	for i in range(len(ope)):
		pos_kl_lä = pos_kl_lä + [i]
		pos_kl_anz = pos_kl_anz + [pos_kl_li.count(i)]
	
	for i in range(len(ope)):
		neg_kl_lä = neg_kl_lä + [i]
		neg_kl_anz = neg_kl_anz + [neg_kl_li.count(i)]

	pos_kl_min_open = pos_kur - pos_kl_li.count(0)
	neg_kl_min_open = neg_kur - neg_kl_li.count(0)

	return [[pos_kur, pos_kl_min_open, pos_kl_open, pos_kl_lä, pos_kl_anz], [neg_kur, neg_kl_min_open, neg_kl_open, neg_kl_lä, neg_kl_anz], [anz_pos, perf_pos], [anz_neg, perf_neg], verh_ks_gesch, nb_ks]
