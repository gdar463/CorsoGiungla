#
#  Copyright (c) 2026 gdar463 <dev@gdar463.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import pandas as pd

import numpy as np

rng = np.random.default_rng(30)

print("Parte 1")

voti = rng.integers(12, 31, size=(5, 4), dtype=np.uint8)
print("Voti:", voti)

# Shape: (5, 4) = 5 righe (studenti), 4 colonne (materie)
# dtype: uint8, siccome i voto sono solo interi fino a 31, un unsigned int a 8 bit è sufficiente

print("Media per studente:", voti.mean(axis=1))
print("Media per materia:", voti.mean(axis=0))
print("Voto Massimo:", voti.max(), "|", "Voto Minimo:", voti.min())

print("Voti Sufficienti:", voti[voti >= 18])
print("Numero Voti Insufficienti", np.sum(voti < 18))
print("\n")

print("Parte 2")

materie = pd.Series(["Matematica", "Informatica", "Fisica", "Inglese"])
votiDf = pd.DataFrame(
    voti,
    columns=materie,
    index=["Studente " + str(i) for i in range(1, 6)],
)
print("Voti Frame:")
print(votiDf)
print()

print("Voti Informatica:")
print(votiDf["Informatica"])
print()

print("Primi 3 Studenti:")
print(votiDf.head(3))
print()

print("Da Studente 2 a Studente 4:")
print(votiDf[1:4])
print()

print("Matematica e Inglese:")
print(votiDf[["Matematica", "Inglese"]])
print()

votiDf["media"] = votiDf.mean(axis=1)
print("Voti Frame con media:")
print(votiDf)
print()

votiDf["esito"] = votiDf["media"].map(lambda x: "Promosso" if x >= 18 else "Bocciato")
print("Voti Frame con esito:")
print(votiDf)
print("\n")

print("Parte 3")

print("Media Informatica:", np.mean(votiDf["Informatica"]))
print("Voto Massimo:", np.max(votiDf[materie]))
print()

mean = np.mean(votiDf[materie])
std = np.std(votiDf[materie])
print("Voti Normalizzati:")
print(votiDf[materie].map(lambda x: (x - mean) / std))
print()

votiDf.sort_values(by=["media"], ascending=False, inplace=True)
print("Voti Frame Ordinato:")
print(votiDf)
print()

print("Studenti Promossi:")
print(votiDf[votiDf["esito"] == "Promosso"])
print()

print("Studenti sopra la Media:")
print(votiDf[votiDf["media"] > mean])
