import pandas as pd

def recommend_products(salary, loan_term_years, coverage_type, ncd, filters, df, max_percentage=0.3, down_payment_percentage=0.1, interest_rate=0.035):
    # Data Cleaning
    df['Price'] = df['Price'].astype(str)
    df['Price'] = df['Price'].str.replace(r'[^\d.]', '', regex=True)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df = df.dropna(subset=['Price'])

    # Calculate maximum monthly spend on car based on salary
    max_monthly_spend = salary * max_percentage

    # Calculate the maximum car price based on loan terms
    r = float(interest_rate) / 12  # Monthly interest rate
    n = int(loan_term_years * 12)  # Total number of payments

    # Calculate the maximum car price (P)
    car_affordability = max_monthly_spend * ((1 + r)**n - 1) / (r * (1 + r)**n)
    
    # Calculate down payment
    down_payment = car_affordability * down_payment_percentage

    # Estimate insurance cost (based on user inputs)
    print(f"Coverage Type: {coverage_type}")  # Debugging
    insurance_cost_yearly = calculate_insurance_cost(car_affordability, coverage_type, ncd)
    insurance_cost_monthly = insurance_cost_yearly / 12

    # Calculate total monthly cost including insurance
    total_monthly_cost = max_monthly_spend - insurance_cost_monthly

    # Filter products based on affordability
    affordable_products = df[df['Price'] <= car_affordability]

    # Apply additional filters
    if filters.get('brand'):
        affordable_products = affordable_products[affordable_products['Brand'].str.contains(filters['brand'], case=False, na=False)]
    if filters.get('price_range'):
        try:
            min_price, max_price = map(float, filters['price_range'].split('-'))
            affordable_products = affordable_products[(affordable_products['Price'] >= min_price) & (affordable_products['Price'] <= max_price)]
        except ValueError:
            pass  # If the price range filter is not a valid range, skip this filter
    if filters.get('condition'):
        affordable_products = affordable_products[affordable_products['Condition'].str.contains(filters['condition'], case=False, na=False)]
    if filters.get('transmission'):
        affordable_products = affordable_products[affordable_products['Transmission'].str.contains(filters['transmission'], case=False, na=False)]
    if filters.get('body_type'):
        affordable_products = affordable_products[affordable_products['Body Type'].str.contains(filters['body_type'], case=False, na=False)]

    # Sort affordable products by price
    sorted_products = affordable_products.sort_values(by=['Price'], ascending=True)

    # Create details dictionary
    details = {
        'max_monthly_spend': max_monthly_spend,
        'car_affordability': car_affordability,
        'down_payment': down_payment,
        'insurance_cost_yearly': insurance_cost_yearly,
        'insurance_cost_monthly': insurance_cost_monthly,
        'total_monthly_cost': total_monthly_cost,
        'num_affordable_products': sorted_products.shape[0]
    }

    return sorted_products, details


def calculate_insurance_cost(market_price, coverage_type, ncd):
    # Assumptions for insurance calculation
    valid_coverage_types = ['comprehensive', 'third party']
    print(f"Coverage Type received: {coverage_type}")  # Debugging

    if coverage_type not in valid_coverage_types:
        print(f"Invalid coverage type: {coverage_type}")  # Debugging
        raise ValueError("Invalid coverage type")

    if coverage_type == 'comprehensive':
        base_rate = 0.05  # 5% for comprehensive coverage
    elif coverage_type == 'third party':
        base_rate = 0.03  # 3% for third party coverage

    # No Claims Discount rates
    ncd_rates = {
        'None': 0,
        '1 year': 0.25,
        '2 years': 0.30,
        '3 years': 0.3833,
        '4 years': 0.45,
        '5 years': 0.55
    }

    # Basic insurance cost calculation
    basic_insurance = market_price * base_rate
    discount = basic_insurance * ncd_rates.get(ncd, 0)  # Default to 0 if ncd is not found
    total_insurance_cost = basic_insurance - discount
    
    return total_insurance_cost


