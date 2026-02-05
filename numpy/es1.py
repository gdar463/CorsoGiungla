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

import numpy as np

np.random.seed(42)
data_array = np.random.randint(1, 100, size=(4, 5))
print("data_array:")
print(data_array)
sub_array = data_array[:2, :]
print("sub_array:")
print(sub_array)
total_mean = np.mean(data_array)
print("total_mean:", total_mean)
columns_mean = np.mean(data_array, axis=0)
print("columns_mean:")
print(columns_mean)
max_value = np.max(data_array)
print("max_value:", max_value)
