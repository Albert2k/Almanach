import openpyxl
import numpy as np
import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import collections
import matplotlib.mlab as mlab
import e_book_def_export

def excel_export2(daten, basiswert):
	wochentag_perf(daten[0], daten[5])


def excel_export(daten, basiswert):

	quan = quantile(daten[5])
	lagepar = lageparameter(daten[5])
	streupar = streuparameter(daten[5])
	verh = verh_pos_neg(daten[5])
	pos_cl = verh_pos(daten[5])
	neg_cl = verh_neg(daten[5])
	folg_pos = folge_pos(daten[5])
	folg_neg = folge_neg(daten[5])
	kl = kurslücken(daten[1], daten[3], daten[2], daten[4], daten[5])
	strver_pos = strverh(pos_cl[1])
	strver_neg = strverh(neg_cl[1])
	strver_span = strverh(daten[6])
	wpd = was_passiert_schleife(daten[5], 4, 0.5)
	wa = wochentag_perf(daten[0], daten[5], daten[6])
	ma = monate_perf(daten[0], daten[5], daten[6])
	e_book_def_export.excel_ausgabe(daten, basiswert, quan, lagepar, streupar, verh, pos_cl[0], neg_cl[0], folg_pos, folg_neg, kl, strver_pos, strver_neg, strver_span, wpd, wa, ma)


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
			if differenz[i] < 0:
				schwelle1 = - 10000
				schwelle2 = - schritte * schrittlänge
				for j in range(schritte+1):
					if differenz[i] < schwelle2 and differenz[i] >= schwelle1:
						anz_list[j] = anz_list[j] + 1
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
								schwelle6 = schwelle6 - schrittlänge
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
										schwelle6 = schwelle6 - schrittlänge
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

	return [anz_list, wpd, schritte, schrittlänge]


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
					i = i + j
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

	# [Perf_KsSchluss_close, Perf_Open_close, Perf_open_high, Perf_open_low]
	nb_ks = []
	
	for l in range(4):
		nb_ks += [[]]
		for i in range(2):
			nb_ks[l] += [[]]
			for j in range((schritte2+1)*2+1):
				nb_ks[l][i] += [0]

	b_ks = []
	
	for l in range(3):
		b_ks += [[]]
		for i in range(2):
			b_ks[l] += [[]]
			for j in range((schritte2+1)*2+1):
				b_ks[l][i] += [0]


	for i in range(len(ope)-2):
		# positive Kurslücken
		if ope[i+1] > high[i]:
			pos_kur = pos_kur + 1
			rand = high[i]

			# bestätigte Ks; Performance von Open bis Close
			if low[i+1] > rand:
				gro = (close[i+1]-ope[i+1])/ope[i+1]*100
				if gro < 0:
					schwelle3 = - 10000
					schwelle4 = - schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro < schwelle4 and gro >= schwelle3:
							b_ks[0][0][l] = b_ks[0][0][l] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
				elif gro == 0:
					b_ks[0][0][schritte2+1] = b_ks[0][0][schritte2+1] + 1
				else:
					schwelle5 = 10000
					schwelle6 = + schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro <= schwelle5 and gro > schwelle6:
							b_ks[0][0][(schritte2+1)*2-l] = b_ks[0][0][(schritte2+1)*2-l] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2

			# bestätigte Ks; Performance von Open bis High
			if low[i+1] > rand:
				gro = (high[i+1]-ope[i+1])/ope[i+1]*100
				if gro < 0:
					schwelle3 = - 10000
					schwelle4 = - schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro < schwelle4 and gro >= schwelle3:
							b_ks[1][0][l] = b_ks[1][0][l] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
				elif gro == 0:
					b_ks[1][0][schritte2+1] = b_ks[1][0][schritte2+1] + 1
				else:
					schwelle5 = 10000
					schwelle6 = + schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro <= schwelle5 and gro > schwelle6:
							b_ks[1][0][(schritte2+1)*2-l] = b_ks[1][0][(schritte2+1)*2-l] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2

			# bestätigte Ks; Performance von Open bis low
			if low[i+1] > rand:
				gro = (low[i+1]-ope[i+1])/ope[i+1]*100
				if gro < 0:
					schwelle3 = - 10000
					schwelle4 = - schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro < schwelle4 and gro >= schwelle3:
							b_ks[2][0][l] = b_ks[2][0][l] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
				elif gro == 0:
					b_ks[2][0][schritte2+1] = b_ks[2][0][schritte2+1] + 1
				else:
					schwelle5 = 10000
					schwelle6 = + schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro <= schwelle5 and gro > schwelle6:
							b_ks[2][0][(schritte2+1)*2-l] = b_ks[2][0][(schritte2+1)*2-l] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2

			# am selben tag geschlossene Ks; Performance von Ksschluss bis Close
			if low[i+1] < rand:
				gro = (close[i+1]-rand)/ope[i+1]*100
				if gro < 0:
					schwelle3 = - 10000
					schwelle4 = - schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro < schwelle4 and gro >= schwelle3:
							nb_ks[0][0][l] = nb_ks[0][0][l] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
				elif gro == 0:
					nb_ks[0][0][schritte2+1] = nb_ks[0][0][schritte2+1] + 1
				else:
					schwelle5 = 10000
					schwelle6 = + schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro <= schwelle5 and gro > schwelle6:
							nb_ks[0][0][(schritte2+1)*2-l] = nb_ks[0][0][(schritte2+1)*2-l] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2

			# am selben tag geschlossene Ks; Performance von Open bis Close
			if low[i+1] < rand:
				gro = (close[i+1]-ope[i+1])/ope[i+1]*100
				if gro < 0:
					schwelle3 = - 10000
					schwelle4 = - schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro < schwelle4 and gro >= schwelle3:
							nb_ks[1][0][l] = nb_ks[1][0][l] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
				elif gro == 0:
					nb_ks[1][0][schritte2+1] = nb_ks[1][0][schritte2+1] + 1
				else:
					schwelle5 = 10000
					schwelle6 = + schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro <= schwelle5 and gro > schwelle6:
							nb_ks[1][0][(schritte2+1)*2-l] = nb_ks[1][0][(schritte2+1)*2-l] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2

			# am selben tag geschlossene Ks; Performance von Open bis High
			if low[i+1] < rand:
				gro = (high[i+1]-ope[i+1])/ope[i+1]*100
				if gro < 0:
					schwelle3 = - 10000
					schwelle4 = - schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro < schwelle4 and gro >= schwelle3:
							nb_ks[2][0][l] = nb_ks[2][0][l] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
				elif gro == 0:
					nb_ks[2][0][schritte2+1] = nb_ks[2][0][schritte2+1] + 1
				else:
					schwelle5 = 10000
					schwelle6 = + schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro <= schwelle5 and gro > schwelle6:
							nb_ks[2][0][(schritte2+1)*2-l] = nb_ks[2][0][(schritte2+1)*2-l] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2

			# am selben tag geschlossene Ks; Performance von Open bis Low
			if low[i+1] < rand:
				gro = (low[i+1]-ope[i+1])/ope[i+1]*100
				if gro < 0:
					schwelle3 = - 10000
					schwelle4 = - schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro < schwelle4 and gro >= schwelle3:
							nb_ks[3][0][l] = nb_ks[3][0][l] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
				elif gro == 0:
					nb_ks[3][0][schritte2+1] = nb_ks[3][0][schritte2+1] + 1
				else:
					schwelle5 = 10000
					schwelle6 = + schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro <= schwelle5 and gro > schwelle6:
							nb_ks[3][0][(schritte2+1)*2-l] = nb_ks[3][0][(schritte2+1)*2-l] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
			
			ab = 0
			j = 1
			while ab == 0:
				if i + j < len(ope):
					if rand < low[i+j]:
						j = j + 1

						# offene Ks; Teilschluss
						if j == 2:
							große_ab = (ope[i+1]-high[i])
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

						# offene Ks; Performancebereich
						if j == 2:
							gro = (ope[i+1]-high[i])/ope[i]*100
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

									if differenz[i+1] < 0:
										schwelle3 = - 10000
										schwelle4 = - schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+1] < schwelle4 and differenz[i+1] >= schwelle3:
												perf_pos[1][0][k][l] = perf_pos[1][0][k][l] + 1
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
											else:
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
									elif differenz[i+1] == 0:
										perf_pos[1][0][k][schritte2+1] = perf_pos[1][0][k][schritte2+1] + 1
									else:
										schwelle5 = 10000
										schwelle6 = + schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+1] <= schwelle5 and differenz[i+1] > schwelle6:
												perf_pos[1][0][k][(schritte2+1)*2-l] = perf_pos[1][0][k][(schritte2+1)*2-l] + 1
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2
											else:
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2

									if differenz[i] < 0:
										schwelle3 = - 10000
										schwelle4 = - schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i] < schwelle4 and differenz[i] >= schwelle3:
												perf_pos[2][0][k][l] = perf_pos[2][0][k][l] + 1
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
											else:
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
									elif differenz[i] == 0:
										perf_pos[2][0][k][schritte2+1] = perf_pos[2][0][k][schritte2+1] + 1
									else:
										schwelle5 = 10000
										schwelle6 = + schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i] <= schwelle5 and differenz[i] > schwelle6:
												perf_pos[2][0][k][(schritte2+1)*2-l] = perf_pos[2][0][k][(schritte2+1)*2-l] + 1
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
							gro = (ope[i+1]-high[i])/ope[i]*100
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

									if differenz[i+1] < 0:
										schwelle3 = - 10000
										schwelle4 = - schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+1] < schwelle4 and differenz[i+1] >= schwelle3:
												perf_pos[1][1][k][l] = perf_pos[1][1][k][l] + 1
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
											else:
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
									elif differenz[i+1] == 0:
										perf_pos[1][1][k][schritte2+1] = perf_pos[1][1][k][schritte2+1] + 1
									else:
										schwelle5 = 10000
										schwelle6 = + schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+1] <= schwelle5 and differenz[i+1] > schwelle6:
												perf_pos[1][1][k][(schritte2+1)*2-l] = perf_pos[1][1][k][(schritte2+1)*2-l] + 1
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2
											else:
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2

									if differenz[i] < 0:
										schwelle3 = - 10000
										schwelle4 = - schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i] < schwelle4 and differenz[i] >= schwelle3:
												perf_pos[2][1][k][l] = perf_pos[2][1][k][l] + 1
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
											else:
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
									elif differenz[i] == 0:
										perf_pos[2][1][k][schritte2+1] = perf_pos[2][1][k][schritte2+1] + 1
									else:
										schwelle5 = 10000
										schwelle6 = + schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i] <= schwelle5 and differenz[i] > schwelle6:
												perf_pos[2][1][k][(schritte2+1)*2-l] = perf_pos[2][1][k][(schritte2+1)*2-l] + 1
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
						gro = (ope[i+1]-high[i])/ope[i]*100
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

								if differenz[i+1] < 0:
									schwelle3 = - 10000
									schwelle4 = - schritte2 * schrittlänge2
									for l in range(schritte2+1):
										if differenz[i+1] < schwelle4 and differenz[i+1] >= schwelle3:
											perf_pos[1][0][k][l] = perf_pos[1][0][k][l] + 1
											schwelle3 = schwelle4
											schwelle4 = schwelle4 + schrittlänge2
										else:
											schwelle3 = schwelle4
											schwelle4 = schwelle4 + schrittlänge2
								elif differenz[i+1] == 0:
									perf_pos[1][0][k][schritte2+1] = perf_pos[1][0][k][schritte2+1] + 1
								else:
									schwelle5 = 10000
									schwelle6 = + schritte2 * schrittlänge2
									for l in range(schritte2+1):
										if differenz[i+1] <= schwelle5 and differenz[i+1] > schwelle6:
											perf_pos[1][0][k][(schritte2+1)*2-l] = perf_pos[1][0][k][(schritte2+1)*2-l] + 1
											schwelle5 = schwelle6
											schwelle6 = schwelle6-schrittlänge2
										else:
											schwelle5 = schwelle6
											schwelle6 = schwelle6-schrittlänge2

								if differenz[i] < 0:
									schwelle3 = - 10000
									schwelle4 = - schritte2 * schrittlänge2
									for l in range(schritte2+1):
										if differenz[i] < schwelle4 and differenz[i] >= schwelle3:
											perf_pos[2][0][k][l] = perf_pos[2][0][k][l] + 1
											schwelle3 = schwelle4
											schwelle4 = schwelle4 + schrittlänge2
										else:
											schwelle3 = schwelle4
											schwelle4 = schwelle4 + schrittlänge2
								elif differenz[i] == 0:
									perf_pos[2][0][k][schritte2+1] = perf_pos[2][0][k][schritte2+1] + 1
								else:
									schwelle5 = 10000
									schwelle6 = + schritte2 * schrittlänge2
									for l in range(schritte2+1):
										if differenz[i] <= schwelle5 and differenz[i] > schwelle6:
											perf_pos[2][0][k][(schritte2+1)*2-l] = perf_pos[2][0][k][(schritte2+1)*2-l] + 1
											schwelle5 = schwelle6
											schwelle6 = schwelle6-schrittlänge2
										else:
											schwelle5 = schwelle6
											schwelle6 = schwelle6-schrittlänge2
							else:
								schwelle1 = schwelle2
								schwelle2 = schwelle2-schrittlänge

		elif ope[i+1] < low[i]:
			neg_kur = neg_kur + 1
			rand = low[i]

			if high[i+1] > rand:
				gro = (close[i+1]-rand)/ope[i+1]*100
				if gro < 0:
					schwelle3 = - 10000
					schwelle4 = - schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro < schwelle4 and gro >= schwelle3:
							nb_ks[0][1][l] = nb_ks[0][1][l] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
				elif gro == 0:
					nb_ks[0][1][schritte2+1] = nb_ks[0][1][schritte2+1] + 1
				else:
					schwelle5 = 10000
					schwelle6 = + schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro <= schwelle5 and gro > schwelle6:
							nb_ks[0][1][(schritte2+1)*2-l] = nb_ks[0][1][(schritte2+1)*2-l] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2

			if high[i+1] > rand:
				gro = (close[i+1]-ope[i+1])/ope[i+1]*100
				if gro < 0:
					schwelle3 = - 10000
					schwelle4 = - schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro < schwelle4 and gro >= schwelle3:
							nb_ks[1][1][l] = nb_ks[1][1][l] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
				elif gro == 0:
					nb_ks[1][1][schritte2+1] = nb_ks[1][1][schritte2+1] + 1
				else:
					schwelle5 = 10000
					schwelle6 = + schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro <= schwelle5 and gro > schwelle6:
							nb_ks[1][1][(schritte2+1)*2-l] = nb_ks[1][1][(schritte2+1)*2-l] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2

			if high[i+1] > rand:
				gro = (high[i+1]-ope[i+1])/ope[i+1]*100
				if gro < 0:
					schwelle3 = - 10000
					schwelle4 = - schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro < schwelle4 and gro >= schwelle3:
							nb_ks[2][1][l] = nb_ks[2][1][l] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
				elif gro == 0:
					nb_ks[2][1][schritte2+1] = nb_ks[2][1][schritte2+1] + 1
				else:
					schwelle5 = 10000
					schwelle6 = + schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro <= schwelle5 and gro > schwelle6:
							nb_ks[2][1][(schritte2+1)*2-l] = nb_ks[2][1][(schritte2+1)*2-l] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2

			if high[i+1] > rand:
				gro = (low[i+1]-ope[i+1])/ope[i+1]*100
				if gro < 0:
					schwelle3 = - 10000
					schwelle4 = - schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro < schwelle4 and gro >= schwelle3:
							nb_ks[3][1][l] = nb_ks[3][1][l] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge2
				elif gro == 0:
					nb_ks[3][1][schritte2+1] = nb_ks[3][1][schritte2+1] + 1
				else:
					schwelle5 = 10000
					schwelle6 = + schritte2 * schrittlänge2
					for l in range(schritte2+1):
						if gro <= schwelle5 and gro > schwelle6:
							nb_ks[3][1][(schritte2+1)*2-l] = nb_ks[3][1][(schritte2+1)*2-l] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge2

			ab = 0
			j = 1
			while ab == 0:
				if i + j < len(ope):
					if rand > high[i+j]:
						j = j + 1

						if j == 2:
							große_ab = (low[i] - ope[i+1])
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
							gro = (ope[i+1]-low[i])/ope[i]*100
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

									if differenz[i+1] < 0:
										schwelle3 = - 10000
										schwelle4 = - schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+1] < schwelle4 and differenz[i+1] >= schwelle3:
												perf_neg[1][0][k][l] = perf_neg[1][0][k][l] + 1
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
											else:
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
									elif differenz[i+1] == 0:
										perf_neg[1][0][k][schritte2+1] = perf_neg[1][0][k][schritte2+1] + 1
									else:
										schwelle5 = 10000
										schwelle6 = + schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+1] <= schwelle5 and differenz[i+1] > schwelle6:
												perf_neg[1][0][k][(schritte2+1)*2-l] = perf_neg[1][0][k][(schritte2+1)*2-l] + 1
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2
											else:
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2

									if differenz[i] < 0:
										schwelle3 = - 10000
										schwelle4 = - schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i] < schwelle4 and differenz[i] >= schwelle3:
												perf_neg[2][0][k][l] = perf_neg[2][0][k][l] + 1
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
											else:
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
									elif differenz[i] == 0:
										perf_neg[2][0][k][schritte2+1] = perf_neg[2][0][k][schritte2+1] + 1
									else:
										schwelle5 = 10000
										schwelle6 = + schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i] <= schwelle5 and differenz[i] > schwelle6:
												perf_neg[2][0][k][(schritte2+1)*2-l] = perf_neg[2][0][k][(schritte2+1)*2-l] + 1
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
							gro = (-low[i] + ope[i+1])/ope[i]*100
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

									if differenz[i+1] < 0:
										schwelle3 = - 10000
										schwelle4 = - schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+1] < schwelle4 and differenz[i+1] >= schwelle3:
												perf_neg[1][1][k][l] = perf_neg[1][1][k][l] + 1
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
											else:
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
									elif differenz[i+1] == 0:
										perf_neg[1][1][k][schritte2+1] = perf_neg[1][1][k][schritte2+1] + 1
									else:
										schwelle5 = 10000
										schwelle6 = + schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i+1] <= schwelle5 and differenz[i+1] > schwelle6:
												perf_neg[1][1][k][(schritte2+1)*2-l] = perf_neg[1][1][k][(schritte2+1)*2-l] + 1
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2
											else:
												schwelle5 = schwelle6
												schwelle6 = schwelle6-schrittlänge2

									if differenz[i] < 0:
										schwelle3 = - 10000
										schwelle4 = - schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i] < schwelle4 and differenz[i] >= schwelle3:
												perf_neg[2][1][k][l] = perf_neg[2][1][k][l] + 1
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
											else:
												schwelle3 = schwelle4
												schwelle4 = schwelle4 + schrittlänge2
									elif differenz[i] == 0:
										perf_neg[2][1][k][schritte2+1] = perf_neg[2][1][k][schritte2+1] + 1
									else:
										schwelle5 = 10000
										schwelle6 = + schritte2 * schrittlänge2
										for l in range(schritte2+1):
											if differenz[i] <= schwelle5 and differenz[i] > schwelle6:
												perf_neg[2][1][k][(schritte2+1)*2-l] = perf_neg[2][1][k][(schritte2+1)*2-l] + 1
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
						gro = (-low[i] + ope[i+1])/ope[i]*100
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

								if differenz[i+1] < 0:
									schwelle3 = - 10000
									schwelle4 = - schritte2 * schrittlänge2
									for l in range(schritte2+1):
										if differenz[i+1] < schwelle4 and differenz[i+1] >= schwelle3:
											perf_neg[1][0][k][l] = perf_neg[1][0][k][l] + 1
											schwelle3 = schwelle4
											schwelle4 = schwelle4 + schrittlänge2
										else:
											schwelle3 = schwelle4
											schwelle4 = schwelle4 + schrittlänge2
								elif differenz[i+1] == 0:
									perf_neg[1][0][k][schritte2+1] = perf_neg[1][0][k][schritte2+1] + 1
								else:
									schwelle5 = 10000
									schwelle6 = + schritte2 * schrittlänge2
									for l in range(schritte2+1):
										if differenz[i+1] <= schwelle5 and differenz[i+1] > schwelle6:
											perf_neg[1][0][k][(schritte2+1)*2-l] = perf_neg[1][0][k][(schritte2+1)*2-l] + 1
											schwelle5 = schwelle6
											schwelle6 = schwelle6-schrittlänge2
										else:
											schwelle5 = schwelle6
											schwelle6 = schwelle6-schrittlänge2

								if differenz[i] < 0:
									schwelle3 = - 10000
									schwelle4 = - schritte2 * schrittlänge2
									for l in range(schritte2+1):
										if differenz[i] < schwelle4 and differenz[i] >= schwelle3:
											perf_neg[2][0][k][l] = perf_neg[2][0][k][l] + 1
											schwelle3 = schwelle4
											schwelle4 = schwelle4 + schrittlänge2
										else:
											schwelle3 = schwelle4
											schwelle4 = schwelle4 + schrittlänge2
								elif differenz[i] == 0:
									perf_neg[2][0][k][schritte2+1] = perf_neg[2][0][k][schritte2+1] + 1
								else:
									schwelle5 = 10000
									schwelle6 = + schritte2 * schrittlänge2
									for l in range(schritte2+1):
										if differenz[i] <= schwelle5 and differenz[i] > schwelle6:
											perf_neg[2][0][k][(schritte2+1)*2-l] = perf_neg[2][0][k][(schritte2+1)*2-l] + 1
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

	return [[pos_kur, pos_kl_min_open, pos_kl_open, pos_kl_lä, pos_kl_anz], [neg_kur, neg_kl_min_open, neg_kl_open, neg_kl_lä, neg_kl_anz], [anz_pos, perf_pos], [anz_neg, perf_neg], verh_ks_gesch, nb_ks, b_ks]


def strverh(daten):

	mi = daten[np.argmin(daten)]
	durch = np.mean(daten)
	ma = daten[np.argmax(daten)]

	return [mi, durch, ma]

# ---------------------------------------------------------------------------------------
# Pie-Diagram, Edi und Tesla, Trefferverhältnis
def verh_ri_wr_dia(inp, bas):
	labels = 'Positiv', 'Negativ', 'Neutral'
	colour = '#FF7700', '#D68640', '#FAC596'
	#explode = (0.05, 0.05, 0.05)  

	font = {'fontname':'Calibri'}

	fig, ax = plt.subplots()
	explode = (0, 0.01 ,0.2)
	ax.pie(inp, autopct='%1.1f%%', colors = colour, textprops = font, explode = explode)
	
	patch = []
	for i in range(len(labels)):
		patch = patch + [mpatches.Patch(color=colour[i], label=labels[i])]
	
	plt.legend(handles=patch)

	ax.axis('equal')
	bas = 'Vehältnis_Positiv_Negativ.png'
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
	colour = '#FF7700', '#D68640', '#FAC596', '#967251', '#C7B3A1'
	#explode = (0.05, 0.05, 0.05)  

	font = {'fontname':'Calibri'}

	if wahl == 'pos':
		tit = 'positive Performance'
		bas = 'Positive_Performance.png'
	elif wahl == 'neg':
		tit = 'negative Performance'
		bas = 'Negative_Performance.png'

	fig, ax = plt.subplots()
	explode = (0, 0.1, 0.2, 0.3, 0.4)
	ax.pie(inp, autopct='%1.1f%%', explode = explode, colors = colour, textprops = font)
	
	patch = []
	for i in range(len(labels)):
		patch = patch + [mpatches.Patch(color=colour[i], label=labels[i])]
	
	plt.legend(handles=patch)

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
	colour = '#FF7700', '#D68640'
	
	font = {'fontname':'Calibri'}

	fig, ax = plt.subplots()
	explode = (0, 0.01)
	ax.pie([folg[0], folge_tage], explode = explode, autopct='%1.1f%%', colors = colour, textprops = font)
	
	patch = []
	for i in range(len(labels)):
		patch = patch + [mpatches.Patch(color=colour[i], label=labels[i])]
	
	plt.legend(handles=patch)

	ax.axis('equal')
	plt.savefig(datei_name1, dpi = 900)

	plot_folge = folg[1:7] + [sum(folg[7:len(folg)])]
	gesamt_folge = sum(plot_folge)

	labels = '2', '3', '4', '5', '6', '7', '≥8'
	colour = '#FF7700', '#D68640', '#FAC596', '#967251', '#C7B3A1', '#FFA305', '#FFE085', '#FFBF00'

	fig2, ax2 = plt.subplots()
	explode = (0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5)
	ax2.pie(plot_folge, autopct='%1.1f%%', explode = explode, colors = colour, textprops = font)
	
	patch = []
	for i in range(len(labels)):
		patch = patch + [mpatches.Patch(color=colour[i], label=labels[i])]
	
	plt.legend(handles=patch)

	ax2.axis('equal')
	plt.savefig(datei_name2, dpi = 900)


def label(autotexts, plot_folge, gesamt_folge, pos):
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

def wochentag_perf(datum, differenz, spanne):
	schritte = 4
	schrittlänge = 0.5
	mon = []
	dien = []
	mit = []
	don = []
	frei = []

	mon_sp = []
	dien_sp = []
	mit_sp = []
	don_sp = []
	frei_sp = []

	for i in range(len(datum)):
		dat = datum[i]
		nr = dat.weekday()
		if nr == 0:
			mon += [differenz[i]]
			mon_sp += [spanne[i]]
		elif nr == 1:
			dien += [differenz[i]]
			dien_sp += [spanne[i]]
		elif nr == 2:
			mit += [differenz[i]]
			mit_sp += [spanne[i]]
		elif nr == 3:
			don += [differenz[i]]
			don_sp += [spanne[i]]
		elif nr == 4:
			frei += [differenz[i]]
			frei_sp += [spanne[i]]

	week = []
	week += [mon]
	week += [dien]
	week += [mit]
	week += [don]
	week += [frei]

	week_sp = []
	week_sp += [mon_sp]
	week_sp += [dien_sp]
	week_sp += [mit_sp]
	week_sp += [don_sp]
	week_sp += [frei_sp]

	durch = []

	for i in range(5):
		durch += [[]]
		for j in range(3):
			durch[i] += [0]

	for i in range(5):
		day = week[i]	
		durch[i][0] = day[np.argmin(day)]
		durch[i][1] = np.mean(day)
		durch[i][2] = day[np.argmax(day)]

	durch_sp = []

	for i in range(5):
		durch_sp += [[]]
		for j in range(3):
			durch_sp[i] += [0]

	for i in range(5):
		day = week_sp[i]	
		durch_sp[i][0] = day[np.argmin(day)]
		durch_sp[i][1] = np.mean(day)
		durch_sp[i][2] = day[np.argmax(day)]

	wdp = []
	wo = []

	for i in range(5):
		wdp += [[]]
		for j in range(2*(schritte+1)+1):
			wdp[i] += [0]

	for i in range(5):
		wo += [[]]
		for j in range(3):
			wo[i] += [0]

	for i in range(5):
		day = week[i]
		for j in range(len(day)):
				if day[j] < 0:
					wo[i][0] = wo[i][0] + 1
					schwelle3 = - 10000
					schwelle4 = - schritte * schrittlänge
					for k in range(schritte+1):
						if day[j] < schwelle4 and day[j] >= schwelle3:
							wdp[i][k] = wdp[i][k] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge
				elif day[j] == 0:
					wo[i][1] = wo[i][1] + 1
					wdp[i][schritte+1] = wdp[i][schritte+1] + 1

				else:
					wo[i][2] = wo[i][2] + 1
					schwelle5 = 10000
					schwelle6 = + schritte * schrittlänge
					for k in range(schritte+1):
						if day[j] <= schwelle5 and day[j] > schwelle6:
							wdp[i][(schritte+1)*2-k] = wdp[i][(schritte+1)*2-k] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6 - schrittlänge

	
	return [wdp, durch, wo, durch_sp]


def kerzen_pop_gun(ope, close, low, high, differenz):

	anz_pg = 0
	ab_long = 0
	ab_long_dauer = []
	ab_short = 0
	ab_short_dauer = []

	for i in range(len(spanne)-2):
		if differenz[i] > 0:
			if close[i] > close[i+1] and high[i] > high[i+1] and ope[i] < ope[i+1] and low[i] < low[i+1] and close[i+1] > close[i+2] and high[i+1] > high[i+2] and ope[i+1] < ope[i+2] and low[i+1] < low[i+2]:
				tricker_high = high[i+2]
				tricker_low = low[i+2]
				anz_pg += 1
				j = 0
				k = 1
				while j == 0:
					if i+2+k < len(spanne)-2:
						if close[i+2+k] > tricker_high:
							ab_long += 1
							ab_long_dauer += [k]
							j += 1
						elif close[i+2+k] < tricker_low:
							ab_short += 1
							ab_short_dauer += [k]
							j += 1
						else:
							k += 1
					else:
						ab_long_dauer += [-1]
						j += 1


		if differenz[i] < 0:
			if close[i] > close[i+1] and high[i] > high[i+1] and ope[i] > ope[i+1] and low[i] < low[i+1] and close[i+1] < close[i+2] and high[i+1] > high[i+2] and ope[i+1] > ope[i+2] and low[i+1] < low[i+2]:
				tricker_high = high[i+2]
				tricker_low = low[i+2]
				anz_pg += 1 
				j = 0
				k = 1
				while j == 0:
					if i+2+k < len(spanne)-2:
						if close[i+2+k] > tricker_high:
							ab_long += 1
							ab_long_dauer += [k]
							j += 1
						elif close[i+2+k] < tricker_low:
							ab_short += 1
							ab_short_dauer += [k]
							j += 1
						else:
							k += 1
					else:
						ab_short_dauer += [-1]
						j += 1


def monate_perf(datum, differenz, spanne):
	schritte = 4
	schrittlänge = 0.5
	monate = []
	
	for i in range(12):
			monate += [[]]

	for i in range(len(datum)):
		dat = datum[i]
		nr = dat.month
		monate[nr-1] += [differenz[i]]

	monate_sp = []
	
	for i in range(12):
			monate_sp += [[]]

	for i in range(len(datum)):
		dat = datum[i]
		nr = dat.month
		monate_sp[nr-1] += [spanne[i]]

	durch = []

	for i in range(12):
		durch += [[]]
		for j in range(3):
			durch[i] += [0]

	for i in range(12):
		day = monate[i]	
		durch[i][0] = day[np.argmin(day)]
		durch[i][1] = np.mean(day)
		durch[i][2] = day[np.argmax(day)]

	durch_sp = []

	for i in range(12):
		durch_sp += [[]]
		for j in range(3):
			durch_sp[i] += [0]

	for i in range(12):
		day = monate_sp[i]	
		durch_sp[i][0] = day[np.argmin(day)]
		durch_sp[i][1] = np.mean(day)
		durch_sp[i][2] = day[np.argmax(day)]

	wdp = []
	wo = []

	for i in range(12):
		wdp += [[]]
		for j in range(2*(schritte+1)+1):
			wdp[i] += [0]

	for i in range(12):
		wo += [[]]
		for j in range(3):
			wo[i] += [0]

	for i in range(12):
		day = monate[i]
		for j in range(len(day)):
				if day[j] < 0:
					wo[i][0] = wo[i][0] + 1
					schwelle3 = - 10000
					schwelle4 = - schritte * schrittlänge
					for k in range(schritte+1):
						if day[j] < schwelle4 and day[j] >= schwelle3:
							wdp[i][k] = wdp[i][k] + 1
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge
						else:
							schwelle3 = schwelle4
							schwelle4 = schwelle4 + schrittlänge
				elif day[j] == 0:
					wo[i][1] = wo[i][1] + 1
					wdp[i][schritte+1] = wdp[i][schritte+1] + 1

				else:
					wo[i][2] = wo[i][2] + 1
					schwelle5 = 10000
					schwelle6 = + schritte * schrittlänge
					for k in range(schritte+1):
						if day[j] <= schwelle5 and day[j] > schwelle6:
							wdp[i][(schritte+1)*2-k] = wdp[i][(schritte+1)*2-k] + 1
							schwelle5 = schwelle6
							schwelle6 = schwelle6-schrittlänge
						else:
							schwelle5 = schwelle6
							schwelle6 = schwelle6 - schrittlänge

	
	return [wdp, durch, wo, durch_sp]


def kurslücken2(ope, low, high, close, differenz):
	
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


def monat_neu(datum, ope, low, high, close):

	time_900_1730 = []
	
	for i in range(len(datum)):
		
		dat = datum[i]
		
		wochentag = dat.weekday
		tag = dat.day
		mon = dat.month
		yea = dat.year
		spanne = high[i]-low[i]
		spanne_proz = spanne/ope[i]
		diff = close[i]-ope[i]
		diff_proz = diff/ope[i]

		zwischen = [wochentag, tag, mon, yea, spanne, spanne_proz, diff, proz]
		 
		time_900_1730 =+ zwischen 

	print(time_900_1730)

	for i in range(12):
			time_900_1730 += [[]]

monat_neu(daten[0], daten[1], daten[3], daten[2], daten[4])
