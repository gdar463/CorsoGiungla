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

#
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

import pprint

print("Question 2:")
fibonacci: dict[int, int] = {1: 0, 2: 1}
for i in range(3, 13):
    fibonacci[i] = fibonacci[i - 1] + fibonacci[i - 2]
pprint.pprint(fibonacci)

print()

print("Question 3:")
companyNames = ["Python DS", "PythonSoft", "Pythazon", "Pybook"]
prices = [
    [12.87, 13.23, 11.42, 13.10],
    [23.54, 25.76, 21.87, 22.33],
    [98.99, 102.34, 97.21, 100.065],
    [203.63, 207.54, 202.43, 205.24],
]

companies: dict[str, dict[str, float]] = {
    companyNames[i]: {
        "open": prices[i][0],
        "high": prices[i][1],
        "low": prices[i][2],
        "close": prices[i][3],
    }
    for i in range(len(companyNames))
}
pprint.pprint(companies)

print()

print("Question 6:")
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
cards = {suits[i]: values.copy() for i in range(len(suits))}
pprint.pprint(cards, width=120)
