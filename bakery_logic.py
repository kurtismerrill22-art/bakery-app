def calculate_revenue(orders):
    return sum(num * price for num, price in orders)


def estimate_cost(total_cookies, base_cost, icing=False, icing_cost=0):
    cost_per_cookie = base_cost + (icing_cost if icing else 0)
    return total_cookies * cost_per_cookie


def calculate_results(orders, hours, base_cost, icing, icing_cost):
    total_cookies = sum(num for num, _ in orders)
    revenue = calculate_revenue(orders)
    total_cost = estimate_cost(total_cookies, base_cost, icing, icing_cost)
    profit = revenue - total_cost
    hourly_rate = profit / hours if hours > 0 else 0

    return {
        "cookies": total_cookies,
        "revenue": revenue,
        "cost": total_cost,
        "profit": profit,
        "hourly_rate": hourly_rate
    }