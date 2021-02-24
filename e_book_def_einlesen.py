import openpyxl

def daten_einlesen(excel_datei):
	ws = excel_einlesen(excel_datei)
	rohdaten = rohdaten_einlesen_verarbeiten(ws)
	print('Daten eingelesen!')

	return rohdaten


def excel_einlesen(excel_datei):

	wb_daten = openpyxl.load_workbook(filename = excel_datei)
	ws_daten = wb_daten.active

	return [ws_daten]

# ---------------------------------------------------------------------------
# Retrun-Liste: [0] Datum; [1] Open; [2] High; [3] Low; [4] Close; [5] Differenz; [6] höchste Schwankung

def rohdaten_einlesen_verarbeiten(ws_rohdaten):

	daten_datum = spalte_einlesen(ws_rohdaten, 'A', 'Date')
	daten_open = spalte_einlesen(ws_rohdaten, 'B', 'Open')
	daten_high = spalte_einlesen(ws_rohdaten, 'C', 'High')
	daten_low = spalte_einlesen(ws_rohdaten, 'D', 'Low')
	daten_close = spalte_einlesen(ws_rohdaten, 'E', 'Close')

	daten_diff = []
	for i in range(len(daten_open)):
		daten_diff = daten_diff + [round((daten_close[i] - daten_open[i])/daten_open[i]*100,4)]

	daten_schw = []
	for i in range(len(daten_high)):
		daten_schw = daten_schw + [round((daten_high[i] - daten_low[i])/daten_open[i]*100,4)]



	return [daten_datum, daten_open, daten_high, daten_low, daten_close, daten_diff, daten_schw]


def spalte_einlesen(ws_rohdaten, spalte_name, name):
	ws = ws_rohdaten[0]
	spalten = ws[spalte_name]
	spalten_wert = []

	for i in range(len(spalten)):
		spalten_wert = spalten_wert + [spalten[i].value]

	spalten_wert.remove(name)

	return spalten_wert
	