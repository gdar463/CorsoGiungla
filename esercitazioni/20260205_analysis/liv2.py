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

rng = np.random.default_rng(546)

print("Parte 1")

voti_sem1 = rng.integers(15, 31, size=(6, 5, 4), dtype=np.uint8)
voti_sem2 = rng.integers(15, 31, size=(6, 5, 4), dtype=np.uint8)
voti = np.concatenate((voti_sem1, voti_sem2), axis=1)

print("Media per ogni studente:", voti.mean(axis=(1, 2)))
print("Media per ogni materia:", voti.mean(axis=(0, 1)))
print("Voto massimo per ogni studente:", voti.max(axis=(1, 2)))
print("Voto minimo per ogni materia:", voti.min(axis=(0, 1)))

diffMean = voti_sem2.mean() - voti_sem1.mean()
print("Differenza media:", diffMean)
print("Studenti migliorati:", voti_sem2.mean(axis=(1, 2)) > voti_sem1.mean(axis=(1, 2)))
print("\n")

print("Parte 2")

indices = pd.MultiIndex.from_product(
    [np.arange(1, 7), np.arange(1, 6), np.arange(1, 5)],
    names=["Studente", "Appello", "Materia"],
)
votiDf_sem1 = pd.DataFrame(voti_sem1.flatten(), index=indices, columns=["Voto"])
votiDf_sem1["Semestre"] = 1
votiDf_sem2 = pd.DataFrame(voti_sem2.flatten(), index=indices, columns=["Voto"])
votiDf_sem2["Semestre"] = 2
votiDf = pd.concat([votiDf_sem1, votiDf_sem2])
votiDf.reset_index(inplace=True)
votiDf = votiDf[["Studente", "Semestre", "Appello", "Materia", "Voto"]]
print("Voti Frame:")
print(votiDf)
print()

print("Media per ogni Studente e Semestre:")
print(votiDf.groupby(["Studente", "Semestre"])["Voto"].mean())
print()

materiaGroup = votiDf.groupby(["Materia"])
print("Media per ogni materia:")
print(materiaGroup["Voto"].mean())
print()

print("Materia più difficile:", materiaGroup["Voto"].mean().idxmin())
print("Studente più costante:", votiDf.groupby(["Studente"])["Voto"].std().idxmin())
print()

print("Studente-Semestre-Media Pivot Table:")
studMeanPivot = votiDf.pivot_table(
    index="Studente", columns="Semestre", values="Voto", aggfunc=np.mean
)
print(studMeanPivot)
print()

studMeanPivot["Delta"] = studMeanPivot[2] - studMeanPivot[1]
print("Pivot Table con il Delta:")
print(studMeanPivot)
print("\n")

print("Parte 3")

studMean = votiDf.groupby(["Studente"])["Voto"].mean()
votiDf["Media"] = votiDf["Studente"].map(studMean)
votiDf["Categoria"] = np.select(
    [votiDf["Media"] < 18, votiDf["Media"] < 23, votiDf["Media"] < 27],
    ["Insufficiente", "Sufficiente", "Buono"],
    "Eccelente",
)
votiDf.drop(["Media"], axis=1, inplace=True)
print("Voti Frame con Categoria:")
print(votiDf)
print()

print(
    "Studenti Migliorati:", studMeanPivot[studMeanPivot["Delta"] > 0].index.to_numpy()
)

studMate2SemMean = (
    votiDf[votiDf["Semestre"] == 2]
    .groupby(["Studente", "Materia"])["Voto"]
    .mean()
    .reset_index()
)
print(
    "Studenti in 2nd Semestre con una materia con media >= 28:",
    studMate2SemMean[studMate2SemMean["Voto"] >= 28]["Studente"].unique(),
)
