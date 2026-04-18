# KPI Framework — Amman Digital Market

Define 5 KPIs for the Amman Digital Market. At least 2 must be time-based and 1 must be cohort-based.

---

## KPI 1 (Time-Based)

- **Name:** Monthly Revenue Growth
- **Definition:** Total revenue generated from completed orders grouped by month.
- **Formula:** `SUM(order_items.quantity * products.unit_price)` grouped by `orders.order_date` (Month).
- **Data Source (tables/columns):** `orders.order_date`, `order_items.quantity`, `products.unit_price`.
- **Baseline Value:** 56,261.50 JOD (Total accumulated).
- **Interpretation:** Tracks the market's financial growth over time. An upward trend indicates successful scaling.

---

## KPI 2 (Time-Based)

- **Name:** Weekly Order Volume
- **Definition:** The total count of unique orders processed per week.
- **Formula:** `COUNT(DISTINCT order_id)` grouped by week.
- **Data Source (tables/columns):** `orders.order_id`, `orders.order_date`.
- **Baseline Value:** 443 total clean orders.
- **Interpretation:** Helps manage logistics and delivery capacity. Sudden spikes might require more courier/tow-truck resources.

---

## KPI 3 (Cohort/Category-Based)

- **Name:** Revenue by Product Category
- **Definition:** Total sales value distributed across different product categories.
- **Formula:** `SUM(quantity * unit_price)` grouped by `products.category`.
- **Data Source (tables/columns):** `products.category`, `order_items.quantity`, `products.unit_price`.
- **Baseline Value:** (Varies by category, e.g., Electronics, Groceries).
- **Interpretation:** Identifies which categories are driving the most profit and which are underperforming.

---

## KPI 4

- **Name:** Average Order Value (AOV)
- **Definition:** The average amount of money spent by a customer per transaction.
- **Formula:** `Total Revenue / Total Number of Orders`.
- **Data Source (tables/columns):** `order_items`, `products`, `orders`.
- **Baseline Value:** 127.00 JOD (Calculated: 56,261.50 / 443).
- **Interpretation:** High AOV suggests customers are buying expensive items or many items at once.

---

## KPI 5

- **Name:** Top 5 Best-Selling Products
- **Definition:** The items with the highest total quantity sold.
- **Formula:** `SUM(quantity)` grouped by `product_name` (Top 5).
- **Data Source (tables/columns):** `order_items.quantity`, `products.product_name`.
- **Baseline Value:** Top products listed in Task 2 output.
- **Interpretation:** Guides inventory management. Ensuring these 5 items never go out of stock is critical for revenue.