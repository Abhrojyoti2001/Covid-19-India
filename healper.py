import numpy as np


def return_total_cases(df, start, end, state, col):
    if state != 'All India':
        filter_df = df[(df['Date'] >= str(start)) & (df['Date'] <= str(end))]
        return filter_df[filter_df['State/UnionTerritory'] == state][col].max() - filter_df[filter_df['State/UnionTerritory'] == state][col].min()
    else:
        filter_df = df[(df['Date'] >= str(start)) & (df['Date'] <= str(end))]
        max_values = filter_df.groupby('State/UnionTerritory')[col].max()
        min_values = filter_df.groupby('State/UnionTerritory')[col].min()
        return (max_values - min_values).sum()


def return_daily_cases(df, start, end, state, col, new_col):
    filter_df = df[(df['Date'] >= str(start)) & (df['Date'] <= str(end))]
    if state != 'All India':
        filter_df = filter_df[filter_df['State/UnionTerritory'] == state]
    new_df = filter_df.groupby('Date').sum()[col].reset_index()
    cases = new_df[col].values.tolist()
    cases.insert(0, 0)
    cases = cases[0:-1]
    new_df[new_col] = new_df[col] - cases
    return new_df


def return_cases_chart(df, start, end, col):
    filter_df = df[(df['Date'] >= str(start)) & (df['Date'] <= str(end))]
    total = filter_df.groupby('State/UnionTerritory')[col].max() - filter_df.groupby('State/UnionTerritory')[col].min()
    total = total.reset_index()
    return total
