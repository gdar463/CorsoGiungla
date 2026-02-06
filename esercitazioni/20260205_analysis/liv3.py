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

rng = np.random.default_rng(42)

n_orders = 150
n_order_items = 400
n_returns = 20

# region Task1
print("Task 1")

dates = np.ndarray(shape=(n_orders,), dtype="datetime64[D]")
dates.fill(np.datetime64("2020-01-01"))
dates = dates + rng.integers(-365 * 4, 365 * 4, size=(n_orders,))

orders = pd.DataFrame(
    {
        "order_id": rng.integers(low=0, high=600, size=(n_orders,)),
        "date": dates,
        "customer_id": rng.integers(low=0, high=200, size=(n_orders,)),
        "channel": rng.integers(low=0, high=3, size=(n_orders,)).choose(
            ["web", "app", "store"]
        ),
        "region": rng.integers(low=0, high=3, size=(n_orders,)).choose(
            ["Nord", "Centro", "Sud"]
        ),
        "shipping_cost": (12.5 - 1) * rng.random(size=(n_orders,)) - 1,
    },
)
# print("Orders")
# print(orders)
# print()

order_items = pd.DataFrame(
    {
        "order_id": orders["order_id"][
            rng.integers(low=0, high=n_orders, size=(n_order_items,))
        ].to_numpy(),
        "product_id": rng.integers(low=0, high=150, size=(n_order_items,)),
        "category": rng.integers(low=0, high=4, size=(n_order_items,)).choose(
            ["Electronics", "Home", "Fashion", "Grocery"]
        ),
        "unit_price": (20 + 1) * rng.random(size=(n_order_items,)) - 1,
        "quantity": rng.integers(low=0, high=10, size=(n_order_items,)),
    },
)
# print("Order Items")
# print(order_items)
# print()

return_items = rng.integers(low=0, high=n_order_items, size=(n_returns,))
returns = pd.DataFrame(
    {
        "order_id": order_items["order_id"][return_items].to_numpy(),
        "product_id": order_items["product_id"][return_items].to_numpy(),
        "return_reason": rng.integers(low=0, high=4, size=(n_returns,)).choose(
            ["damaged", "wrong_item", "late", "other"]
        ),
    }
)
# print("Returns")
# print(returns)
# print()

orders.loc[rng.integers(low=0, high=len(orders), size=(5,)), ["shipping_cost"]] = np.nan
orders.loc[rng.integers(low=0, high=len(orders), size=(5,)), ["region"]] = np.nan

old_orders_len = len(orders)
orders.drop_duplicates(subset=["order_id"], inplace=True)
dup_order_ids = old_orders_len - len(orders)

old_orders_len = len(orders)
orders.dropna(subset=["shipping_cost"], inplace=True)
nan_shipping = old_orders_len - len(orders)

orders.fillna({"region": "N/D"}, inplace=True)
nan_regions = orders["region"].value_counts().get("N/D", 0)

old_orders_len = len(orders)
orders = orders[orders["shipping_cost"] >= 0]
neg_shipping_costs = old_orders_len - len(orders)

old_orders_len = len(orders)
orders.dropna(inplace=True)
orders_nan = old_orders_len - len(orders)

old_order_items_len = len(order_items)
order_items.dropna(inplace=True)
order_items_nan = old_order_items_len - len(order_items)

old_order_items_len = len(order_items)
order_items = order_items[order_items["quantity"] > 0]
neg_quantities = old_order_items_len - len(order_items)

old_order_items_len = len(order_items)
order_items = order_items[order_items["unit_price"] >= 0]
neg_unit_prices = old_order_items_len - len(order_items)

old_returns_len = len(returns)
returns.dropna(inplace=True)
returns_nan = old_returns_len - len(returns)

errors = pd.DataFrame(
    {
        "Orders": {
            "Duplicated IDs": dup_order_ids,
            "NaN Shipping": nan_shipping,
            "NaN Regions": nan_regions,
            "Negative Shipping": neg_shipping_costs,
            "Other NaN Fields": orders_nan,
        },
        "Order Items": {
            "Non-positive Quantities": neg_quantities,
            "Negative Unit Prices": neg_unit_prices,
            "NaN Fields": order_items_nan,
        },
        "Return": {
            "NaN Fields": returns_nan,
        },
    }
)
for index in errors:
    items = errors[index].dropna().astype(dtype=np.uint64)
    if items.max() > 0:
        print(f"{index} Errors:")
        print(items.to_string(header=False))
        print()
    else:
        print(f"{index} has no Errors")
        print()
print()
# endregion

# region Task2
print("Task 2")

fact_sales = (
    order_items.set_index("order_id")
    .join(orders.set_index("order_id"), validate="m:1")
    .sort_index()
)

old_fact_sales_len = len(fact_sales)
fact_sales.dropna(inplace=True)
fact_sales_nan = old_fact_sales_len - len(fact_sales)
if fact_sales_nan > 0:
    print(f"Found {fact_sales_nan} orders with no Items. Dropping...")
else:
    print("All orders have items")
print()

# print("Proof of 1-to-many orders-to-order_items relationship (same last 4 columns)")
# print(
#     fact_sales[fact_sales.duplicated(subset=["shipping_cost"])]
#     .sort_values(by=["shipping_cost"])
#     .head()
#     .to_string(max_cols=len(fact_sales.columns))
# )
# print()

fact_sales["item_revenue"] = fact_sales["unit_price"] * fact_sales["quantity"]
fact_sales = fact_sales.merge(
    fact_sales.groupby(["order_id"])["item_revenue"].sum().rename("order_revenue"),
    on=["order_id"],
)
fact_sales["order_total"] = fact_sales["order_revenue"] + fact_sales["shipping_cost"]
print("Fact Sales: First 10 rows")
print(fact_sales.head(10).to_string(max_cols=len(fact_sales.columns)))
print("\n")
# endregion

# region Task3
print("Task 3")

channel_use = fact_sales["channel"].value_counts() / len(fact_sales) * 100
kpi = pd.DataFrame(
    {
        "Total Revenue": [fact_sales["order_total"].drop_duplicates().sum()],
        "Orders Count": [len(fact_sales.index.unique())],
        "Unique Customers": [len(fact_sales["customer_id"].unique())],
        "AOV": [fact_sales["order_total"].drop_duplicates().mean()],
        "Web Channel %": [channel_use["web"]],
        "App Channel %": [channel_use["app"]],
        "Store Channel %": [channel_use["store"]],
    }
)
print("KPI")
print(kpi.to_string(index=False, max_cols=len(kpi.columns)))
print("\n")
# endregion

# region Task4
print("Task 4")

pivot_table = fact_sales.pivot_table(
    index="region", columns="channel", values="order_total", aggfunc=np.sum
)
print("Pivot Table")
print(pivot_table)
print()

print("Top 3 Categories per Revenue")
print(
    fact_sales.groupby(["category"])["item_revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(3)
    .to_string(header=False)
)
print()

print("Top 5 Customers per Revenue")
print(
    fact_sales.reset_index()
    .astype({"customer_id": np.uint32})
    .drop_duplicates(subset=["order_id"])
    .groupby(["customer_id"])["order_revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .to_string(header=False)
)
print("\n")
# endregion

# region Task5
print("Task 5")

return_sales = fact_sales.merge(returns, on=["order_id", "product_id"])
print("Return Rate % per Category")
print(
    (
        return_sales["category"].value_counts()
        / fact_sales["category"].value_counts()
        * 100
    )
    .sort_values(ascending=False)
    .to_string(header=False)
)
print()

print(
    "Highest Return Reason:",
    return_sales["return_reason"].value_counts().sort_values(ascending=False).index[0],
)
print("Revenue at Risk:", return_sales["item_revenue"].sum())
# endregion

# region Task5
print("Task 5")

# noinspection PyTypeChecker
fact_sales["weekday"] = fact_sales["date"].dt.day_of_week
fact_sales["basket_size"] = fact_sales.index.value_counts()
fact_sales = fact_sales.merge(
    fact_sales.groupby(["order_id"])["quantity"].sum().rename("items_per_order"),
    on=["order_id"],
)
corr = fact_sales.loc[:, ["basket_size", "order_total"]].corr()
print("Fact Sales")
print(fact_sales.to_string(max_cols=len(fact_sales.columns)))
print()

print(
    "Correlation between basket_size and order_total",
    corr["basket_size"].get("order_total"),
)
# endregion
