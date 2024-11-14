# backtesting.py

def initialize_backtest(initial_balance=10000):
    # Initialize cumulative performance metrics
    metrics = {
        'balance': initial_balance,
        'initial_balance': initial_balance,
        'num_trades': 0,
        'wins': 0,
        'losses': 0,
        'total_return': 0,
        'win_rate': 0,
    }
    return metrics

def update_metrics(metrics, entry_price, exit_price):
    # Calculate profit for this trade
    profit = exit_price - entry_price
    metrics['balance'] += profit
    metrics['num_trades'] += 1

    # Track win or loss
    if profit > 0:
        metrics['wins'] += 1
    else:
        metrics['losses'] += 1

    # Update cumulative metrics
    metrics['total_return'] = ((metrics['balance'] - metrics['initial_balance']) / metrics['initial_balance']) * 100
    metrics['win_rate'] = metrics['wins'] / metrics['num_trades'] if metrics['num_trades'] > 0 else 0

    return metrics

def run_real_time_backtest(data, model, metrics):
    # Run the backtest on each new data point
    for i in range(1, len(data)):
        # Check if we have a "buy" signal
        if data['Prediction'].iloc[i] == 1 and data['Position'].iloc[i-1] == 0:
            # Record entry price and switch position to "bought"
            data.at[i, 'Entry Price'] = data['Close'].iloc[i]
            data.at[i, 'Position'] = 1  # Enter a trade

        # Check if we have a "sell" signal
        elif data['Prediction'].iloc[i] == 0 and data['Position'].iloc[i-1] == 1:
            # Record exit price and update metrics
            data.at[i, 'Exit Price'] = data['Close'].iloc[i]
            metrics = update_metrics(metrics, data.at[i-1, 'Entry Price'], data['Close'].iloc[i])
            data.at[i, 'Position'] = 0  # Exit the trade

    return metrics, data
