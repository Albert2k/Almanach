import openpyxl
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import collections
import matplotlib.mlab as mlab
import e_book_def_export


def excel_export(daten, basiswert):

	quan = quantile(daten[5])
	lagepar = lageparameter(daten[5])
	streupar = streuparameter(daten[5])
	verh = verh_pos_neg(daten[5])
	pos_cl = verh_pos(daten[5])
	neg_cl = verh_neg(daten[5])
	folg_pos = folge_pos(daten[5])
	folg_neg = folge_neg(daten[5])
	kl = kurslücken(daten[1], daten[3], daten[2], daten[4])
	strver_pos = strverh(pos_cl[1])
	strver_neg = strverh(neg_cl[1])
	strver_span = strverh(daten[6])
	wp = was_passiert_danach(daten[5])
	wpd = was_passiert_schleife(daten[5], 30, 0.1)
	e_book_def_export.excel_ausgabe(daten, basiswert, quan, lagepar, streupar, verh, pos_cl[0], neg_cl[0], folg_pos, folg_neg, kl, strver_pos, strver_neg, strver_span, wp, wpd)


def aus_grund(daten, basiswert):
	ver_pos_neg = verh_pos_neg(daten[5])
	verh_ri_wr_dia(ver_pos_neg, basiswert)

	ver_pos=verh_pos(daten[5])
	verh_dia(ver_pos[0], 'pos', basiswert)

	ver_neg = verh_neg(daten[5])
	verh_dia(ver_neg[0], 'neg', basiswert)
	performance_his(daten[5], 'beide', basiswert)

	folg_pos = folge_pos(daten[5])
	folge_dia(folg_pos[0], folg_pos[1], folg_pos[3], 'pos', basiswert)
	folg_neg = folge_neg(daten[5])
	folge_dia(folg_neg[0], folg_neg[1], folg_neg[3], 'neg', basiswert)


# ---------------------------------------------------------------------------------
# Zählt wie viele positive, negative und neutrale Tage es gibt
# Returnwert: [Anzahl positiver Tage, Anzahl negativer Tage, Anzahl neutraler Tage]

def verh_pos_neg(differenz):
	pos = 0
	neu = 0
	neg = 0

	for i in range(len(differenz)):
		if differenz[i] > 0:
			pos = pos + 1
		elif differenz[i] == 0:
			neu = neu +1
		elif differenz[i] < 0:
			neg = neg + 1

	return [pos, neg, neu]


# ---------------------------------------------------------------------------------
# Unterteilt die positiven Tage in Cluster, 0%-0,5%, 0,5%-1%, usw. alle Werte größer
# zwei Prozent im letzten Cluster
# Returnwert: [[Anzahl in Cluster], Liste positiver Werte]

def verh_pos(differenz):
	cl1 = 0
	cl2 = 0
	cl3 = 0
	cl4 = 0
	cl5 = 0
	al = []

	for i in range(len(differenz)):
		if differenz[i] > 0:
			al = al + [differenz[i]]
			if differenz[i] <= 0.5:
				cl1 = cl1 + 1
			elif differenz[i] > 0.5 and differenz[i] <= 1:
				cl2 = cl2 + 1
			elif differenz[i] > 1 and differenz[i] <= 1.5:
				cl3 = cl3 + 1
			elif differenz[i] > 1.5 and differenz[i] <= 2:
				cl4 = cl4 + 1
			elif differenz[i] > 2:
				cl5 = cl5 + 1

	return [[cl1, cl2, cl3, cl4, cl5], al]


# ---------------------------------------------------------------------------------
# Unterteilt die negativen Tage in Cluster, 0%-0,5%, 0,5%-1%, usw. alle Werte größer
# zwei Prozent im letzten Cluster
# Returnwert: [[Anzahl in Cluster], Liste negativer Werte]

def verh_neg(differenz):
	cl1 = 0
	cl2 = 0
	cl3 = 0
	cl4 = 0
	cl5 = 0
	al = []

	for i in range(len(differenz)):
		if differenz[i] < 0:
			al = al + [differenz[i]]
			if abs(differenz[i]) <= 0.5:
				cl1 = cl1 + 1
			elif abs(differenz[i]) > 0.5 and abs(differenz[i]) <= 1:
				cl2 = cl2 + 1
			elif abs(differenz[i]) > 1 and abs(differenz[i]) <= 1.5:
				cl3 = cl3 + 1
			elif abs(differenz[i]) > 1.5 and abs(differenz[i]) <= 2:
				cl4 = cl4 + 1
			elif abs(differenz[i]) > 2:
				cl5 = cl5 + 1

	return [[cl1, cl2, cl3, cl4, cl5], al]


# Funktions die auswertet was nach einem bestimmten Prozentsatz-Tag passiert

def was_passiert_schleife(differenz, schritte, schrittlänge):

	list_p = []
	anz_list = []
	wpd_ber = []
	wpd = []
	for i in range(2*(schritte+1)+1):
		anz_list = anz_list + [0]

	for i in range(3):
		wpd += [[]]
		for j in range(2*(schritte+1)+1):
			wpd[i] += [[]]
			for k in range(2*(schritte+1)+1):
				wpd[i][j] += [0]

	for i in range(len(differenz)-30):
		zugeord1 = 0
		while zugeord1 == 0:
			print(i)
			if differenz[i] < 0:
				schwelle1 = - 10000
				schwelle2 = - schritte * schrittlänge
				for j in range(schritte+1):
					if differenz[i] < schwelle2 and differenz[i] >= schwelle1:
						anz_list[j] = anz_list[j] + 1
						print(sum(anz_list))
						zugeord2 = 0
						while zugeord2 == 0:
							if differenz[i+1] < 0:
								schwelle3 = - 10000
								schwelle4 = - schritte * schrittlänge
								for k in range(schritte+1):
									if differenz[i+1] < schwelle4 and differenz[i+1] >= schwelle3:
										wpd[0][j][k] = wpd[0][j][k] + 1
										zugeord1 = 1
										zugeord2 = 1
										schwelle3 = schwelle4
										schwelle4 = schwelle4 + schrittlänge
									else:
										schwelle3 = schwelle4
										schwelle4 = schwelle4 + schrittlänge
							elif differenz[i+1] == 0:
								wpd[0][j][schritte+1] = wpd[0][j][schritte+1] + 1
								zugeord1 = 1
								zugeord2 = 1
							else:
								schwelle5 = 10000
								schwelle6 = + schritte * schrittlänge
								for k in range(schritte+1):
									if differenz[i+1] <= schwelle5 and differenz[i+1] > schwelle6:
										wpd[0][j][(schritte+1)*2-k] = wpd[0][j][(schritte+1)*2-k] + 1
										zugeord1 = 1
										zugeord2 = 1
										schwelle5 = schwelle6
										schwelle6 = schwelle6-schrittlänge
									else:
										schwelle5 = schwelle6
										schwelle6 = schwelle6-schrittlänge
							
							sum5 = sum(differenz[i+1:i+6])
							if sum5 < 0:
								schwelle3 = - 10000
								schwelle4 = - schritte * schrittlänge
								for k in range(schritte+1):
									if sum5 < schwelle4 and sum5 >= schwelle3:
										wpd[1][j][k] = wpd[1][j][k] + 1
										zugeord1 = 1
										zugeord2 = 1
										schwelle3 = schwelle4
										schwelle4 = schwelle4 + schrittlänge
									else:
										schwelle3 = schwelle4
										schwelle4 = schwelle4 + schrittlänge
							elif sum5 == 0:
								wpd[1][j][schritte+1] = wpd[1][j][schritte+1] + 1
								zugeord1 = 1
								zugeord2 = 1
							else:
								schwelle5 = 10000
								schwelle6 = + schritte * schrittlänge
								for k in range(schritte+1):
									if sum5 <= schwelle5 and sum5 > schwelle6:
										wpd[1][j][(schritte+1)*2-k] = wpd[1][j][(schritte+1)*2-k] + 1
										zugeord1 = 1
										zugeord2 = 1
										schwelle5 = schwelle6
										schwelle6 = schwelle6-schrittlänge
									else:
										schwelle5 = schwelle6
										schwelle6 = schwelle6 - schrittlänge

							sum30 = sum(differenz[i+1:i+31])
							if sum30 < 0:
								schwelle3 = - 10000
								schwelle4 = - schritte * schrittlänge
								for k in range(schritte+1):
									if sum30 < schwelle4 and sum30 >= schwelle3:
										wpd[2][j][k] = wpd[2][j][k] + 1
										zugeord1 = 1
										zugeord2 = 1
										schwelle3 = schwelle4
										schwelle4 = schwelle4 + schrittlänge
									else:
										schwelle3 = schwelle4
										schwelle4 = schwelle4 + schrittlänge

							elif sum30 == 0:
								wpd[2][j][schritte+1] = wpd[2][j][schritte+1] + 1
								zugeord1 = 1
								zugeord2 = 1
							else:
								schwelle5 = 10000
								schwelle6 = + schritte * schrittlänge
								for k in range(schritte+1):
									if sum30 <= schwelle5 and sum30 > schwelle6:
										wpd[2][j][(schritte+1)*2-k] = wpd[2][j][(schritte+1)*2-k] + 1
										zugeord1 = 1
										zugeord2 = 1
										schwelle5 = schwelle6
										schwelle6 = schwelle6-schrittlänge
									else:
										schwelle5 = schwelle6
										schwelle6 = schwelle6 - schrittlänge
						schwelle1 = schwelle2
						schwelle2 = schwelle2 + schrittlänge				
					else:
						schwelle1 = schwelle2
						schwelle2 = schwelle2 + schrittlänge

			elif differenz[i] == 0:
				anz_list[schritte+1] = anz_list[schritte+1] + 1
				zugeord2 = 0
				while zugeord2 == 0:
					if differenz[i+1] < 0:
						schwelle3 = - 10000
						schwelle4 = - schritte * schrittlänge
						for k in range(schritte+1):
							if differenz[i+1] < schwelle4 and differenz[i+1] >= schwelle3:
								wpd[0][schritte+1][k] = wpd[0][schritte+1][k] + 1
								zugeord1 = 1
								zugeord2 = 1
								schwelle3 = schwelle4
								schwelle4 = schwelle4 + schrittlänge
							else:
								schwelle3 = schwelle4
								schwelle4 = schwelle4 + schrittlänge
					elif differenz[i+1] == 0:
						wpd[0][schritte+1][schritte+1] = wpd[0][schritte+1][schritte+1] + 1
						zugeord1 = 1
						zugeord2 = 1
					else:
						schwelle5 = 10000
						schwelle6 = + schritte * schrittlänge
						for k in range(schritte+1):
							if differenz[i+1] <= schwelle5 and differenz[i+1] > schwelle6:
								wpd[0][schritte+1][(schritte+1)*2-k] = wpd[0][schritte+1][(schritte+1)*2-k] + 1
								zugeord1 = 1
								zugeord2 = 1
								schwelle5 = schwelle6
								schwelle6 = schwelle6-schrittlänge
							else:
								schwelle5 = schwelle6
								schwelle6 = schwelle6 - schrittlänge

					sum5 = sum(differenz[i+1:i+6])
					if sum5 < 0:
						schwelle3 = - 10000
						schwelle4 = - schritte * schrittlänge
						for k in range(schritte+1):
							if sum5 < schwelle4 and sum5 >= schwelle3:
								wpd[1][schritte+1][k] = wpd[1][schritte+1][k] + 1
								zugeord1 = 1
								zugeord2 = 1
								schwelle3 = schwelle4
								schwelle4 = schwelle4 + schrittlänge
							else:
								schwelle3 = schwelle4
								schwelle4 = schwelle4 + schrittlänge

					elif sum5 == 0:
						wpd[1][schritte+1][schritte+1] = wpd[1][schritte+1][schritte+1] + 1
						zugeord1 = 1
						zugeord2 = 1
					else:
						schwelle5 = 10000
						schwelle6 = + schritte * schrittlänge
						for k in range(schritte+1):
							if sum5 <= schwelle5 and sum5 > schwelle6:
								wpd[1][schritte+1][(schritte+1)*2-k] = wpd[1][schritte+1][(schritte+1)*2-k] + 1
								zugeord1 = 1
								zugeord2 = 1
								schwelle5 = schwelle6
								schwelle6 = schwelle6-schrittlänge
							else:
								schwelle5 = schwelle6
								schwelle6 = schwelle6 - schrittlänge

					sum30 = sum(differenz[i+1:i+31])
					if sum30 < 0:
						schwelle3 = - 10000
						schwelle4 = - schritte * schrittlänge
						for k in range(schritte+1):
							if sum30 < schwelle4 and sum30 >= schwelle3:
								wpd[2][schritte+1][k] = wpd[2][schritte+1][k] + 1
								zugeord1 = 1
								zugeord2 = 1
								schwelle3 = schwelle4
								schwelle4 = schwelle4 + schrittlänge
							else:
								schwelle3 = schwelle4
								schwelle4 = schwelle4 + schrittlänge

					elif sum30 == 0:
						wpd[2][schritte+1][schritte+1] = wpd[2][schritte+1][schritte+1] + 1
						zugeord1 = 1
						zugeord2 = 1
					else:
						schwelle5 = 10000
						schwelle6 = schritte * schrittlänge
						for k in range(schritte+1):
							if sum30 <= schwelle5 and sum30 > schwelle6:
								wpd[2][schritte+1][(schritte+1)*2-k] = wpd[2][schritte+1][(schritte+1)*2-k] + 1
								zugeord1 = 1
								zugeord2 = 1
								schwelle5 = schwelle6
								schwelle6 = schwelle6-schrittlänge
							else:
								schwelle5 = schwelle6
								schwelle6 = schwelle6 - schrittlänge
			else:
				schwelle1 = 10000
				schwelle2 = schritte * schrittlänge
				for j in range(schritte+1):
					if differenz[i] <= schwelle1 and differenz[i] > schwelle2:
						anz_list[(schritte+1)*2-j] = anz_list[(schritte+1)*2-j] + 1
						zugeord2 = 0
						while zugeord2 == 0:
							if differenz[i+1] < 0:
								schwelle3 = - 10000
								schwelle4 = - schritte * schrittlänge
								for k in range(schritte+1):
									if differenz[i+1] < schwelle4 and differenz[i+1] >= schwelle3:
										wpd[0][(schritte+1)*2-j][k] = wpd[0][(schritte+1)*2-j][k] + 1
										zugeord1 = 1
										zugeord2 = 1
										schwelle3 = schwelle4
										schwelle4 = schwelle4 + schrittlänge
									else:
										schwelle3 = schwelle4
										schwelle4 = schwelle4 + schrittlänge

							elif differenz[i+1] == 0:
								wpd[0][(schritte+1)*2-j][schritte+1] = wpd[0][(schritte+1)*2-j][schritte+1] + 1
								zugeord1 = 1
								zugeord2 = 1
							else:
								schwelle5 = 10000
								schwelle6 = + schritte * schrittlänge
								for k in range(schritte+1):
									if differenz[i+1] <= schwelle5 and differenz[i+1] > schwelle6:
										wpd[0][(schritte+1)*2-j][(schritte+1)*2-k] = wpd[0][(schritte+1)*2-j][(schritte+1)*2-k] + 1
										zugeord1 = 1
										zugeord2 = 1
										schwelle5 = schwelle6
										schwelle6 = schwelle6-schrittlänge
									else:
										schwelle5 = schwelle6
										schwelle6 = schwelle6 - schrittlänge

							sum5 = sum(differenz[i+1:i+6])
							if sum5 < 0:
								schwelle3 = - 10000
								schwelle4 = - schritte * schrittlänge
								for k in range(schritte+1):
									if sum5 < schwelle4 and sum5 >= schwelle3:
										wpd[1][(schritte+1)*2-j][k] = wpd[1][(schritte+1)*2-j][k] + 1
										zugeord1 = 1
										zugeord2 = 1
										schwelle3 = schwelle4
										schwelle4 = schwelle4 + schrittlänge
									else:
										schwelle3 = schwelle4
										schwelle4 = schwelle4 + schrittlänge

							elif sum5 == 0:
								wpd[1][(schritte+1)*2-j][schritte+1] = wpd[1][(schritte+1)*2-j][schritte+1] + 1
								zugeord1 = 1
								zugeord2 = 1
							else:
								schwelle5 = 10000
								schwelle6 = + schritte * schrittlänge
								for k in range(schritte+1):
									if sum5 <= schwelle5 and sum5 > schwelle6:
										wpd[1][(schritte+1)*2-j][(schritte+1)*2-k] = wpd[1][(schritte+1)*2-j][(schritte+1)*2-k] + 1
										zugeord1 = 1
										zugeord2 = 1
										schwelle5 = schwelle6
										schwelle6 = schwelle6-schrittlänge
									else:
										schwelle5 = schwelle6
										schwelle6 = schwelle6 - schrittlänge

							sum30 = sum(differenz[i+1:i+31])
							if sum30 < 0:
								schwelle3 = - 10000
								schwelle4 = - schritte * schrittlänge
								for k in range(schritte+1):
									if sum30 < schwelle4 and sum30 >= schwelle3:
										wpd[2][(schritte+1)*2-j][k] = wpd[2][(schritte+1)*2-j][k] + 1
										zugeord1 = 1
										zugeord2 = 1
										schwelle3 = schwelle4
										schwelle4 = schwelle4 + schrittlänge
									else:
										schwelle3 = schwelle4
										schwelle4 = schwelle4 + schrittlänge

							elif sum30 == 0:
								wpd[2][(schritte+1)*2-j][schritte+1] = wpd[2][(schritte+1)*2-j][schritte+1] + 1
								zugeord1 = 1
								zugeord2 = 1
							else:
								schwelle5 = 10000
								schwelle6 = + schritte * schrittlänge
								for k in range(schritte+1):
									if sum30 <= schwelle5 and sum30 > schwelle6:
										wpd[2][(schritte+1)*2-j][(schritte+1)*2-k] = wpd[2][(schritte+1)*2-j][(schritte+1)*2-k] + 1
										zugeord1 = 1
										zugeord2 = 1
										schwelle5 = schwelle6
										schwelle6 = schwelle6-schrittlänge
									else:
										schwelle5 = schwelle6
										schwelle6 = schwelle6 - schrittlänge
						schwelle1 = schwelle2
						schwelle2 = schwelle2 - schrittlänge

					else:
						schwelle1 = schwelle2
						schwelle2 = schwelle2 - schrittlänge

	print(wpd, anz_list)
	return [anz_list, wpd, schritte, schrittlänge]


def was_passiert_danach(differenz,):

	anz_list = [0,0,0,0,0]
	wp1_list_9_17 = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]]
	wp5_list_9_17 = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]]
	wp30_list_9_17 = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]]
	wp1_list_9_9 = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]]
	wp5_list_9_9 = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]]
	wp30_list_9_9 = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]]

	for i in range(len(differenz)-30):
		if differenz[i] > 0:

			if differenz[i] <= 0.5:
				anz_list[0] = anz_list[0] + 1

				if differenz[i+1] < -2:
					wp1_list_9_17[0][0] = wp1_list_9_17[0][0] + 1
				elif differenz[i+1] < -1.50:
					wp1_list_9_17[0][1] = wp1_list_9_17[0][1] + 1
				elif differenz[i+1] < -1:
					wp1_list_9_17[0][2] = wp1_list_9_17[0][2] + 1
				elif differenz[i+1] < -0.5:
					wp1_list_9_17[0][3] = wp1_list_9_17[0][3] + 1
				elif differenz[i+1] < 0:
					wp1_list_9_17[0][4] = wp1_list_9_17[0][4] + 1
				elif differenz[i+1] == 0:
					wp1_list_9_17[0][5] = wp1_list_9_17[0][5] + 1
				elif differenz[i+1] <= 0.5:
					wp1_list_9_17[0][6] = wp1_list_9_17[0][6] + 1
				elif differenz[i+1] <= 1:
					wp1_list_9_17[0][7] = wp1_list_9_17[0][7] + 1
				elif differenz[i+1] <= 1.5:
					wp1_list_9_17[0][8] = wp1_list_9_17[0][8] + 1
				elif differenz[i+1] <= 2:
					wp1_list_9_17[0][9] = wp1_list_9_17[0][9] + 1
				else:
					wp1_list_9_17[0][10] = wp1_list_9_17[0][10] + 1

				if sum(differenz[i+1:i+6]) < -2:
					wp5_list_9_17[0][0] = wp5_list_9_17[0][0] + 1
				elif sum(differenz[i+1:i+6]) < -1.50:
					wp5_list_9_17[0][1] = wp5_list_9_17[0][1] + 1
				elif sum(differenz[i+1:i+6]) < -1:
					wp5_list_9_17[0][2] = wp5_list_9_17[0][2] + 1
				elif sum(differenz[i+1:i+6]) < -0.5:
					wp5_list_9_17[0][3] = wp5_list_9_17[0][3] + 1
				elif sum(differenz[i+1:i+6]) < 0:
					wp5_list_9_17[0][4] = wp5_list_9_17[0][4] + 1
				elif sum(differenz[i+1:i+6]) == 0:
					wp5_list_9_17[0][5] = wp5_list_9_17[0][5] + 1
				elif sum(differenz[i+1:i+6]) <= 0.5:
					wp5_list_9_17[0][6] = wp5_list_9_17[0][6] + 1
				elif sum(differenz[i+1:i+6]) <= 1:
					wp5_list_9_17[0][7] = wp5_list_9_17[0][7] + 1
				elif sum(differenz[i+1:i+6]) <= 1.5:
					wp5_list_9_17[0][8] = wp5_list_9_17[0][8] + 1
				elif sum(differenz[i+1:i+6]) <= 2:
					wp5_list_9_17[0][9] = wp5_list_9_17[0][9] + 1
				else:
					wp5_list_9_17[0][10] = wp5_list_9_17[0][10] + 1

				if sum(differenz[i+1:i+31]) < -2:
					wp30_list_9_17[0][0] = wp30_list_9_17[0][0] + 1
				elif sum(differenz[i+1:i+31]) < -1.50:
					wp30_list_9_17[0][1] = wp30_list_9_17[0][1] + 1
				elif sum(differenz[i+1:i+31]) < -1:
					wp30_list_9_17[0][2] = wp30_list_9_17[0][2] + 1
				elif sum(differenz[i+1:i+31]) < -0.5:
					wp30_list_9_17[0][3] = wp30_list_9_17[0][3] + 1
				elif sum(differenz[i+1:i+31]) < 0:
					wp30_list_9_17[0][4] = wp30_list_9_17[0][4] + 1
				elif sum(differenz[i+1:i+31]) == 0:
					wp30_list_9_17[0][5] = wp30_list_9_17[0][5] + 1
				elif sum(differenz[i+1:i+31]) <= 0.5:
					wp30_list_9_17[0][6] = wp30_list_9_17[0][6] + 1
				elif sum(differenz[i+1:i+31]) <= 1:
					wp30_list_9_17[0][7] = wp30_list_9_17[0][7] + 1
				elif sum(differenz[i+1:i+31]) <= 1.5:
					wp30_list_9_17[0][8] = wp30_list_9_17[0][8] + 1
				elif sum(differenz[i+1:i+31]) <= 2:
					wp30_list_9_17[0][9] = wp30_list_9_17[0][9] + 1
				else:
					wp30_list_9_17[0][10] = wp30_list_9_17[0][10] + 1

			elif differenz[i] > 0.5 and differenz[i] <= 1:
				anz_list[1] = anz_list[1] + 1

				if differenz[i+1] < -2:
					wp1_list_9_17[1][0] = wp1_list_9_17[1][0] + 1
				elif differenz[i+1] < -1.50:
					wp1_list_9_17[1][1] = wp1_list_9_17[1][1] + 1
				elif differenz[i+1] < -1:
					wp1_list_9_17[1][2] = wp1_list_9_17[1][2] + 1
				elif differenz[i+1] < -0.5:
					wp1_list_9_17[1][3] = wp1_list_9_17[1][3] + 1
				elif differenz[i+1] < 0:
					wp1_list_9_17[1][4] = wp1_list_9_17[1][4] + 1
				elif differenz[i+1] == 0:
					wp1_list_9_17[1][5] = wp1_list_9_17[1][5] + 1
				elif differenz[i+1] <= 0.5:
					wp1_list_9_17[1][6] = wp1_list_9_17[1][6] + 1
				elif differenz[i+1] <= 1:
					wp1_list_9_17[1][7] = wp1_list_9_17[1][7] + 1
				elif differenz[i+1] <= 1.5:
					wp1_list_9_17[1][8] = wp1_list_9_17[1][8] + 1
				elif differenz[i+1] <= 2:
					wp1_list_9_17[1][9] = wp1_list_9_17[1][9] + 1
				else:
					wp1_list_9_17[1][10] = wp1_list_9_17[1][10] + 1

				if sum(differenz[i+1:i+6]) < -2:
					wp5_list_9_17[1][0] = wp5_list_9_17[1][0] + 1
				elif sum(differenz[i+1:i+6]) < -1.50:
					wp5_list_9_17[1][1] = wp5_list_9_17[1][1] + 1
				elif sum(differenz[i+1:i+6]) < -1:
					wp5_list_9_17[1][2] = wp5_list_9_17[1][2] + 1
				elif sum(differenz[i+1:i+6]) < -0.5:
					wp5_list_9_17[1][3] = wp5_list_9_17[1][3] + 1
				elif sum(differenz[i+1:i+6]) < 0:
					wp5_list_9_17[1][4] = wp5_list_9_17[1][4] + 1
				elif sum(differenz[i+1:i+6]) == 0:
					wp5_list_9_17[1][5] = wp5_list_9_17[1][5] + 1
				elif sum(differenz[i+1:i+6]) <= 0.5:
					wp5_list_9_17[1][6] = wp5_list_9_17[1][6] + 1
				elif sum(differenz[i+1:i+6]) <= 1:
					wp5_list_9_17[1][7] = wp5_list_9_17[1][7] + 1
				elif sum(differenz[i+1:i+6]) <= 1.5:
					wp5_list_9_17[1][8] = wp5_list_9_17[1][8] + 1
				elif sum(differenz[i+1:i+6]) <= 2:
					wp5_list_9_17[1][9] = wp5_list_9_17[1][9] + 1
				else:
					wp5_list_9_17[1][10] = wp5_list_9_17[1][10] + 1

				if sum(differenz[i+1:i+31]) < -2:
					wp30_list_9_17[1][0] = wp30_list_9_17[1][0] + 1
				elif sum(differenz[i+1:i+31]) < -1.50:
					wp30_list_9_17[1][1] = wp30_list_9_17[1][1] + 1
				elif sum(differenz[i+1:i+31]) < -1:
					wp30_list_9_17[1][2] = wp30_list_9_17[1][2] + 1
				elif sum(differenz[i+1:i+31]) < -0.5:
					wp30_list_9_17[1][3] = wp30_list_9_17[1][3] + 1
				elif sum(differenz[i+1:i+31]) < 0:
					wp30_list_9_17[1][4] = wp30_list_9_17[1][4] + 1
				elif sum(differenz[i+1:i+31]) == 0:
					wp30_list_9_17[1][5] = wp30_list_9_17[1][5] + 1
				elif sum(differenz[i+1:i+31]) <= 0.5:
					wp30_list_9_17[1][6] = wp30_list_9_17[1][6] + 1
				elif sum(differenz[i+1:i+31]) <= 1:
					wp30_list_9_17[1][7] = wp30_list_9_17[1][7] + 1
				elif sum(differenz[i+1:i+31]) <= 1.5:
					wp30_list_9_17[1][8] = wp30_list_9_17[1][8] + 1
				elif sum(differenz[i+1:i+31]) <= 2:
					wp30_list_9_17[1][9] = wp30_list_9_17[1][9] + 1
				else:
					wp30_list_9_17[1][10] = wp30_list_9_17[1][10] + 1

			elif differenz[i] > 1 and differenz[i] <= 1.5:
				anz_list[2] = anz_list[2] + 1

				if differenz[i+1] < -2:
					wp1_list_9_17[2][0] = wp1_list_9_17[2][0] + 1
				elif differenz[i+1] < -1.50:
					wp1_list_9_17[2][1] = wp1_list_9_17[2][1] + 1
				elif differenz[i+1] < -1:
					wp1_list_9_17[2][2] = wp1_list_9_17[2][2] + 1
				elif differenz[i+1] < -0.5:
					wp1_list_9_17[2][3] = wp1_list_9_17[2][3] + 1
				elif differenz[i+1] < 0:
					wp1_list_9_17[2][4] = wp1_list_9_17[2][4] + 1
				elif differenz[i+1] == 0:
					wp1_list_9_17[2][5] = wp1_list_9_17[2][5] + 1
				elif differenz[i+1] <= 0.5:
					wp1_list_9_17[2][6] = wp1_list_9_17[2][6] + 1
				elif differenz[i+1] <= 1:
					wp1_list_9_17[2][7] = wp1_list_9_17[2][7] + 1
				elif differenz[i+1] <= 1.5:
					wp1_list_9_17[2][8] = wp1_list_9_17[2][8] + 1
				elif differenz[i+1] <= 2:
					wp1_list_9_17[2][9] = wp1_list_9_17[2][9] + 1
				else:
					wp1_list_9_17[2][10] = wp1_list_9_17[2][10] + 1

				if sum(differenz[i+1:i+6]) < -2:
					wp5_list_9_17[2][0] = wp5_list_9_17[2][0] + 1
				elif sum(differenz[i+1:i+6]) < -1.50:
					wp5_list_9_17[2][1] = wp5_list_9_17[2][1] + 1
				elif sum(differenz[i+1:i+6]) < -1:
					wp5_list_9_17[2][2] = wp5_list_9_17[2][2] + 1
				elif sum(differenz[i+1:i+6]) < -0.5:
					wp5_list_9_17[2][3] = wp5_list_9_17[2][3] + 1
				elif sum(differenz[i+1:i+6]) < 0:
					wp5_list_9_17[2][4] = wp5_list_9_17[2][4] + 1
				elif sum(differenz[i+1:i+6]) == 0:
					wp5_list_9_17[2][5] = wp5_list_9_17[2][5] + 1
				elif sum(differenz[i+1:i+6]) <= 0.5:
					wp5_list_9_17[2][6] = wp5_list_9_17[2][6] + 1
				elif sum(differenz[i+1:i+6]) <= 1:
					wp5_list_9_17[2][7] = wp5_list_9_17[2][7] + 1
				elif sum(differenz[i+1:i+6]) <= 1.5:
					wp5_list_9_17[2][8] = wp5_list_9_17[2][8] + 1
				elif sum(differenz[i+1:i+6]) <= 2:
					wp5_list_9_17[2][9] = wp5_list_9_17[2][9] + 1
				else:
					wp5_list_9_17[2][10] = wp5_list_9_17[2][10] + 1

				if sum(differenz[i+1:i+31]) < -2:
					wp30_list_9_17[2][0] = wp30_list_9_17[2][0] + 1
				elif sum(differenz[i+1:i+31]) < -1.50:
					wp30_list_9_17[2][1] = wp30_list_9_17[2][1] + 1
				elif sum(differenz[i+1:i+31]) < -1:
					wp30_list_9_17[2][2] = wp30_list_9_17[2][2] + 1
				elif sum(differenz[i+1:i+31]) < -0.5:
					wp30_list_9_17[2][3] = wp30_list_9_17[2][3] + 1
				elif sum(differenz[i+1:i+31]) < 0:
					wp30_list_9_17[2][4] = wp30_list_9_17[2][4] + 1
				elif sum(differenz[i+1:i+31]) == 0:
					wp30_list_9_17[2][5] = wp30_list_9_17[2][5] + 1
				elif sum(differenz[i+1:i+31]) <= 0.5:
					wp30_list_9_17[2][6] = wp30_list_9_17[2][6] + 1
				elif sum(differenz[i+1:i+31]) <= 1:
					wp30_list_9_17[2][7] = wp30_list_9_17[2][7] + 1
				elif sum(differenz[i+1:i+31]) <= 1.5:
					wp30_list_9_17[2][8] = wp30_list_9_17[2][8] + 1
				elif sum(differenz[i+1:i+31]) <= 2:
					wp30_list_9_17[2][9] = wp30_list_9_17[2][9] + 1
				else:
					wp30_list_9_17[2][10] = wp30_list_9_17[2][10] + 1

			elif differenz[i] > 1.5 and differenz[i] <= 2:
				anz_list[3] = anz_list[3] + 1

				if differenz[i+1] < -2:
					wp1_list_9_17[3][0] = wp1_list_9_17[3][0] + 1
				elif differenz[i+1] < -1.50:
					wp1_list_9_17[3][1] = wp1_list_9_17[3][1] + 1
				elif differenz[i+1] < -1:
					wp1_list_9_17[3][2] = wp1_list_9_17[3][2] + 1
				elif differenz[i+1] < -0.5:
					wp1_list_9_17[3][3] = wp1_list_9_17[3][3] + 1
				elif differenz[i+1] < 0:
					wp1_list_9_17[3][4] = wp1_list_9_17[3][4] + 1
				elif differenz[i+1] == 0:
					wp1_list_9_17[3][5] = wp1_list_9_17[3][5] + 1
				elif differenz[i+1] <= 0.5:
					wp1_list_9_17[3][6] = wp1_list_9_17[3][6] + 1
				elif differenz[i+1] <= 1:
					wp1_list_9_17[3][7] = wp1_list_9_17[3][7] + 1
				elif differenz[i+1] <= 1.5:
					wp1_list_9_17[3][8] = wp1_list_9_17[3][8] + 1
				elif differenz[i+1] <= 2:
					wp1_list_9_17[3][9] = wp1_list_9_17[3][9] + 1
				else:
					wp1_list_9_17[3][10] = wp1_list_9_17[3][10] + 1

				if sum(differenz[i+1:i+6]) < -2:
					wp5_list_9_17[3][0] = wp5_list_9_17[3][0] + 1
				elif sum(differenz[i+1:i+6]) < -1.50:
					wp5_list_9_17[3][1] = wp5_list_9_17[3][1] + 1
				elif sum(differenz[i+1:i+6]) < -1:
					wp5_list_9_17[3][2] = wp5_list_9_17[3][2] + 1
				elif sum(differenz[i+1:i+6]) < -0.5:
					wp5_list_9_17[3][3] = wp5_list_9_17[3][3] + 1
				elif sum(differenz[i+1:i+6]) < 0:
					wp5_list_9_17[3][4] = wp5_list_9_17[3][4] + 1
				elif sum(differenz[i+1:i+6]) == 0:
					wp5_list_9_17[3][5] = wp5_list_9_17[3][5] + 1
				elif sum(differenz[i+1:i+6]) <= 0.5:
					wp5_list_9_17[3][6] = wp5_list_9_17[3][6] + 1
				elif sum(differenz[i+1:i+6]) <= 1:
					wp5_list_9_17[3][7] = wp5_list_9_17[3][7] + 1
				elif sum(differenz[i+1:i+6]) <= 1.5:
					wp5_list_9_17[3][8] = wp5_list_9_17[3][8] + 1
				elif sum(differenz[i+1:i+6]) <= 2:
					wp5_list_9_17[3][9] = wp5_list_9_17[3][9] + 1
				else:
					wp5_list_9_17[3][10] = wp5_list_9_17[3][10] + 1

				if sum(differenz[i+1:i+31]) < -2:
					wp30_list_9_17[3][0] = wp30_list_9_17[3][0] + 1
				elif sum(differenz[i+1:i+31]) < -1.50:
					wp30_list_9_17[3][1] = wp30_list_9_17[3][1] + 1
				elif sum(differenz[i+1:i+31]) < -1:
					wp30_list_9_17[3][2] = wp30_list_9_17[3][2] + 1
				elif sum(differenz[i+1:i+31]) < -0.5:
					wp30_list_9_17[3][3] = wp30_list_9_17[3][3] + 1
				elif sum(differenz[i+1:i+31]) < 0:
					wp30_list_9_17[3][4] = wp30_list_9_17[3][4] + 1
				elif sum(differenz[i+1:i+31]) == 0:
					wp30_list_9_17[3][5] = wp30_list_9_17[3][5] + 1
				elif sum(differenz[i+1:i+31]) <= 0.5:
					wp30_list_9_17[3][6] = wp30_list_9_17[3][6] + 1
				elif sum(differenz[i+1:i+31]) <= 1:
					wp30_list_9_17[3][7] = wp30_list_9_17[3][7] + 1
				elif sum(differenz[i+1:i+31]) <= 1.5:
					wp30_list_9_17[3][8] = wp30_list_9_17[3][8] + 1
				elif sum(differenz[i+1:i+31]) <= 2:
					wp30_list_9_17[3][9] = wp30_list_9_17[3][9] + 1
				else:
					wp30_list_9_17[3][10] = wp30_list_9_17[3][10] + 1

			elif differenz[i] > 2:
				anz_list[4] = anz_list[4] + 1

				if differenz[i+1] < -2:
					wp1_list_9_17[4][0] = wp1_list_9_17[4][0] + 1
				elif differenz[i+1] < -1.50:
					wp1_list_9_17[4][1] = wp1_list_9_17[4][1] + 1
				elif differenz[i+1] < -1:
					wp1_list_9_17[4][2] = wp1_list_9_17[4][2] + 1
				elif differenz[i+1] < -0.5:
					wp1_list_9_17[4][3] = wp1_list_9_17[4][3] + 1
				elif differenz[i+1] < 0:
					wp1_list_9_17[4][4] = wp1_list_9_17[4][4] + 1
				elif differenz[i+1] == 0:
					wp1_list_9_17[4][5] = wp1_list_9_17[4][5] + 1
				elif differenz[i+1] <= 0.5:
					wp1_list_9_17[4][6] = wp1_list_9_17[4][6] + 1
				elif differenz[i+1] <= 1:
					wp1_list_9_17[4][7] = wp1_list_9_17[4][7] + 1
				elif differenz[i+1] <= 1.5:
					wp1_list_9_17[4][8] = wp1_list_9_17[4][8] + 1
				elif differenz[i+1] <= 2:
					wp1_list_9_17[4][9] = wp1_list_9_17[4][9] + 1
				else:
					wp1_list_9_17[4][10] = wp1_list_9_17[4][10] + 1

				if sum(differenz[i+1:i+6]) < -2:
					wp5_list_9_17[4][0] = wp5_list_9_17[4][0] + 1
				elif sum(differenz[i+1:i+6]) < -1.50:
					wp5_list_9_17[4][1] = wp5_list_9_17[4][1] + 1
				elif sum(differenz[i+1:i+6]) < -1:
					wp5_list_9_17[4][2] = wp5_list_9_17[4][2] + 1
				elif sum(differenz[i+1:i+6]) < -0.5:
					wp5_list_9_17[4][3] = wp5_list_9_17[4][3] + 1
				elif sum(differenz[i+1:i+6]) < 0:
					wp5_list_9_17[4][4] = wp5_list_9_17[4][4] + 1
				elif sum(differenz[i+1:i+6]) == 0:
					wp5_list_9_17[4][5] = wp5_list_9_17[4][5] + 1
				elif sum(differenz[i+1:i+6]) <= 0.5:
					wp5_list_9_17[4][6] = wp5_list_9_17[4][6] + 1
				elif sum(differenz[i+1:i+6]) <= 1:
					wp5_list_9_17[4][7] = wp5_list_9_17[4][7] + 1
				elif sum(differenz[i+1:i+6]) <= 1.5:
					wp5_list_9_17[4][8] = wp5_list_9_17[4][8] + 1
				elif sum(differenz[i+1:i+6]) <= 2:
					wp5_list_9_17[4][9] = wp5_list_9_17[4][9] + 1
				else:
					wp5_list_9_17[4][10] = wp5_list_9_17[4][10] + 1

				if sum(differenz[i+1:i+31]) < -2:
					wp30_list_9_17[4][0] = wp30_list_9_17[4][0] + 1
				elif sum(differenz[i+1:i+31]) < -1.50:
					wp30_list_9_17[4][1] = wp30_list_9_17[4][1] + 1
				elif sum(differenz[i+1:i+31]) < -1:
					wp30_list_9_17[4][2] = wp30_list_9_17[4][2] + 1
				elif sum(differenz[i+1:i+31]) < -0.5:
					wp30_list_9_17[4][3] = wp30_list_9_17[4][3] + 1
				elif sum(differenz[i+1:i+31]) < 0:
					wp30_list_9_17[4][4] = wp30_list_9_17[4][4] + 1
				elif sum(differenz[i+1:i+31]) == 0:
					wp30_list_9_17[4][5] = wp30_list_9_17[4][5] + 1
				elif sum(differenz[i+1:i+31]) <= 0.5:
					wp30_list_9_17[4][6] = wp30_list_9_17[4][6] + 1
				elif sum(differenz[i+1:i+31]) <= 1:
					wp30_list_9_17[4][7] = wp30_list_9_17[4][7] + 1
				elif sum(differenz[i+1:i+31]) <= 1.5:
					wp30_list_9_17[4][8] = wp30_list_9_17[4][8] + 1
				elif sum(differenz[i+1:i+31]) <= 2:
					wp30_list_9_17[4][9] = wp30_list_9_17[4][9] + 1
				else:
					wp30_list_9_17[4][10] = wp30_list_9_17[4][10] + 1

	return [anz_list, wp1_list_9_17, wp5_list_9_17, wp30_list_9_17]


# ---------------------------------------------------------------------------------
# Erstellt Angaben über Länge und Häufigkeit von positiven Folgen
# Returnwert: [Anzahl aller Tage, Anzahl aller Tage in Folgen(min 2 Tage), max Folgelänge, Liste der Häufigkeiten von Folgen]

def folge_pos(differenz):
	folge = []
	i = 0

	while i <= len(differenz)-1:
		if differenz[i] > 0:
			ab = 0
			j = 0
			while ab == 0:
				if differenz[i+j] > 0 and len(differenz)-1 > i+j:
					j = j + 1
				elif differenz[i+j] > 0 and len(differenz)-1 == i+j:
					j = j + 1
					ab = 1
					folge = folge + [j]
				elif differenz[i+j] <= 0 and len(differenz)-1 >= i+j:
					ab = 1
					folge = folge + [j]
					i = i + j
				elif len(differenz)-1 < i+j:
					ab = 1
					if j > 0:
						folge = folge + [j]
					i = i + j + 1
		else:
			i = i + 1

	anz = sum(folge)

	max_fol = max(folge)
	anzahl_folge = []

	for i in range(1, max_fol + 1):
		anzahl_folge = anzahl_folge + [folge.count(i)]

	folg_tage = anz - anzahl_folge[0]
	
	return [anz, folg_tage, max_fol, anzahl_folge]


# ---------------------------------------------------------------------------------
# Erstellt Angaben über Länge und Häufigkeit von negativen Folgen
# Returnwert: [Anzahl aller Tage, Anzahl aller Tage in Folgen(min 2 Tage), max Folgelänge, Liste der Häufigkeiten von Folgen]

def folge_neg(differenz):
	folge = []
	i = 0

	while i <= len(differenz)-1:
		if differenz[i] < 0:
			ab = 0
			j = 0
			while ab == 0:
				if differenz[i+j] < 0 and len(differenz)-1 > i+j:
					j = j + 1
				elif differenz[i+j] < 0 and len(differenz)-1 == i+j:
					j = j + 1
					ab = 1
					folge = folge + [j]
					i = i + j
				elif differenz[i+j] >= 0 and len(differenz)-1 >= i+j:
					ab = 1
					folge = folge + [j]
					i = i + j
				elif len(differenz)-1 < i+j+1:
					ab = 1
					if j > 0:
						folge = folge + [j]
					i = i + j + 1
		else:
			i = i + 1

	anz = sum(folge)

	max_fol = max(folge)
	anzahl_folge = []

	for i in range(1, max_fol + 1):
		anzahl_folge = anzahl_folge + [folge.count(i)]

	folg_tage = anz - anzahl_folge[0]
	
	return [anz, folg_tage, max_fol, anzahl_folge]


# ---------------------------------------------------------------------------------
# Berechnet den maximalen und minimalen Wert sowie das 25%-, 50%- und 75%-Quantil
# Returnwert: [min, 25%, 50%, 75%, max]

def quantile(daten):

	quan_min = daten[np.argmin(daten)]
	quan25 = np.percentile(daten,25)
	quan50 = np.percentile(daten,50)
	quan75 = np.percentile(daten,75)
	quan_max = daten[np.argmax(daten)]

	return [quan_min, quan25, quan50, quan75, quan_max]


# ---------------------------------------------------------------------------------
# Berechnet die Lageparameter der Performance-Verteilung
# Returnwert: [modus, median, aritmetisches Mittel]

def lageparameter(daten):

	data_modu = collections.Counter(daten)
	modu = data_modu.most_common(1)
	modu = list(modu[0])
	modu = modu[0]
	medi = np.median(daten)
	armi = np.mean(daten)

	return [modu, medi, armi]

def streuparameter(daten):

	varianz = np.var(daten)
	strab = np.std(daten)
	
	semi_daten = []
	for i in range(len(daten)):
		if daten[i] < 0:
			semi_daten = semi_daten + [daten[i]]

	semi_strab = np.std(semi_daten)

	var = []
	var = var + [np.percentile(daten,5)]
	var = var + [np.percentile(daten,1)]
	var = var + [np.percentile(daten,0.1)]

	cvar_li = []
	for j in range(3):
		cvar_dat = []
		for i in range(len(daten)):
			if daten[i] < var[j]:
				cvar_dat = cvar_dat + [daten[i]]
		cvar_li = cvar_li + [cvar_dat]

	cvar = []
	cvar = cvar + [np.mean(cvar_li[0])]
	cvar = cvar + [np.mean(cvar_li[1])]
	cvar = cvar + [np.mean(cvar_li[2])]


	armi = np.mean(daten)
	daten_wöl = []
	for i in range(len(daten)):
		daten_wöl = daten_wöl + [(daten[i]-armi)/strab]
	daten_wöl = np.power(daten_wöl, 4)

	wölbung = sum(daten_wöl)/len(daten_wöl)

	daten_sch = []
	for i in range(len(daten)):
		daten_sch = daten_sch + [(daten[i]-armi)/strab]
	daten_sch = np.power(daten_sch, 3)
	schiefe = sum(daten_sch)/len(daten_sch)


	return[schiefe, wölbung, varianz, strab, semi_strab, var, cvar]


# ---------------------------------------------------------------------------------
# Berechnet Anzahl und Eigenschaften von Kurslüken
# Returnwert: [[Anzahl Kurslücken, Anzahl bestätigter Kurslücken(min am entstehungstag offen),
#               Anzahl offener Kurslüken, Öffnungdauer, Häufigkeit][negativ]]

def kurslücken(ope, low, high, close):
	
	print('start')
	pos_kur = 0
	neg_kur = 0
	pos_kl_li = []
	neg_kl_li = []
	pos_kl_open = 0
	neg_kl_open = 0
	for i in range(len(ope)-1):
		if ope[i+1] > high[i]:
			pos_kur = pos_kur + 1
			rand = high[i]			
			ab = 0
			j = 1
			while ab == 0:
				if i + j < len(ope):
					if rand < low[i+j]:
						j = j + 1
					elif rand >= low[i+j]:
						ab = 1
						pos_kl_li = pos_kl_li + [j-1]
				else:
					ab = 1
					pos_kl_li = pos_kl_li + [j-1]
					pos_kl_open = pos_kl_open + 1		
		elif ope[i+1] < low[i]:
			neg_kur = neg_kur + 1
			rand = low[i]
			ab = 0
			j = 1
			while ab == 0:
				if i + j < len(ope):
					if rand > high[i+j]:
						j = j + 1
					elif rand <= high[i+j]:
						ab = 1
						neg_kl_li = neg_kl_li + [j-1]
				else:
					ab = 1
					neg_kl_li = neg_kl_li + [j-1]
					neg_kl_open = neg_kl_open + 1


	pos_kl_lä = []
	pos_kl_anz = []
	neg_kl_lä = []
	neg_kl_anz = []

	for i in range(len(ope)):
		if pos_kl_li.count(i) > 0:
			pos_kl_lä = pos_kl_lä + [i]
			pos_kl_anz = pos_kl_anz + [pos_kl_li.count(i)]
	
	for i in range(len(ope)):
		if neg_kl_li.count(i) > 0:
			neg_kl_lä = neg_kl_lä + [i]
			neg_kl_anz = neg_kl_anz + [neg_kl_li.count(i)]

	pos_kl_min_open = pos_kur - pos_kl_li.count(0)
	neg_kl_min_open = neg_kur - neg_kl_li.count(0)

	return [[pos_kur, pos_kl_min_open, pos_kl_open, pos_kl_lä, pos_kl_anz],[neg_kur, neg_kl_min_open, neg_kl_open, neg_kl_lä, neg_kl_anz]]


def strverh(daten):

	mi = daten[np.argmin(daten)]
	durch = np.mean(daten)
	ma = daten[np.argmax(daten)]

	return [mi, durch, ma]

# ---------------------------------------------------------------------------------------
# Pie-Diagram, Edi und Tesla, Trefferverhältnis
def verh_ri_wr_dia(inp, bas):
	labels = 'Positiv', 'Negativ', 'Neutral'
	colour = '#FFD900', '#FFE761', '#E6FF05'
	#explode = (0.05, 0.05, 0.05)  

	font = {'fontname':'Calibri'}

	fig, ax = plt.subplots()
	ax.pie(inp, labels=labels, autopct='%1.1f%%', startangle=90, colors = colour, textprops = font)
	ax.axis('equal')
	bas = 'Vehältnis_Positiv_Negativ.png'
	plt.legend()
	plt.savefig(bas, dpi = 900)


	

def performance_his(daten, wahl, bas):

	fig, ax = plt.subplots()
	n, bins, patches = plt.hist(daten, range = (-20,20), bins = 400, facecolor = '#408000', edgecolor = 'black')

	# add a 'best fit' line
	#y = mlab.normpdf( bins, mu, sigma)
	#l = plt.plot(bins, y, 'r--', linewidth=1)

	plt.xlabel('Prozent')
	plt.ylabel('Tage')
	if wahl == 'pos':
		plt.title('positive Performance')
		ax.set_xlim(0,4)
	elif wahl == 'neg':
		plt.title('negative Performance')
		ax.set_xlim(-4,0)
	elif wahl == 'beide':
		ax.set_xlim(-4,4)

	plt.grid(True)

	bas = 'Histo_Performance.png'
	plt.legend()
	plt.savefig(bas, dpi = 900)


# ---------------------------------------------------------------------------------------
# Pie-Diagram, Edi und Tesla, Trefferverhältnis
def verh_dia(inp, wahl, bas):
	labels = '0,01-0,50', '0,51-1,00', '1,01-1.50', '1,51-2,00', '< 2,00'
	colour = '#FFD900', '#FFE761', '#E6FF05', '#F1FF70', '#AEFF0D'
	#explode = (0.05, 0.05, 0.05)  

	font = {'fontname':'Calibri'}

	if wahl == 'pos':
		tit = 'positive Performance'
		bas = 'Positive_Performance.png'
	elif wahl == 'neg':
		tit = 'negative Performance'
		bas = 'Negative_Performance.png'

	fig, ax = plt.subplots()
	ax.pie(inp, labels=labels, autopct='%1.1f%%', startangle=90, colors = colour, textprops = font)
	ax.axis('equal')

	plt.savefig(bas, dpi = 900)


def folge_dia(anz, folge_tage, folg, ausri, bas):
	
	if ausri == 'pos':
		tit = 'positive Folgentage'
		tit2 = 'positive Folgen'
		datei_name1 = 'positive_Folgentage.png'
		datei_name2 = 'positive_Folgen.png'
	elif ausri == 'neg':
		tit = 'negative Folgentage'
		tit2 = 'negative Folgen'
		datei_name1 = 'negative_Folgentage.png'
		datei_name2 = 'negative_Folgen.png'

	labels = 'nicht in Folge', 'in Folge'
	colour = '#FFD900', '#FFE761'
	
	font = {'fontname':'Calibri'}

	fig, ax = plt.subplots()
	ax.pie([folg[0], folge_tage], labels=labels, autopct='%1.1f%%', startangle=90, colors = colour, textprops = font)
	ax.axis('equal')

	plt.savefig(datei_name1, dpi = 900)

	plot_folge = folg[1:7] + [sum(folg[7:len(folg)])]
	gesamt_folge = sum(plot_folge)

	labels = '2', '3', '4', '5', '6', '7', '≥8'
	colour = '#FFD900', '#FFE761', '#E6FF05', '#F1FF70', '#AEFF0D', '#C2E876', '#97E876'

	fig2, ax2 = plt.subplots()
	patches, texts, autotexts = ax2.pie(plot_folge, labels=labels, autopct='%1.1f%%', startangle=90, colors = colour, textprops = font)
	
	j = 0
	for i in range(len(autotexts)-1):
		j = j + 1
		if plot_folge[i]/gesamt_folge <= 0.1 and plot_folge[i+1]/gesamt_folge <= 0.1 and j > 0:
			pos = autotexts[i+1].get_position()
			pos = list(pos)
			pos[0] = pos[0] * 1.2
			pos[1] = pos[1] * 1.2
			pos = tuple(pos)
			autotexts[i+1].set_position(pos)
			j = - 1

	ax2.axis('equal')

	plt.savefig(datei_name2, dpi = 900)