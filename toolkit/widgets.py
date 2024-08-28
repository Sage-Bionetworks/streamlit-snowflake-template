import plotly.express as px
import plotly.graph_objects as go

def scatter_plot_yearly_unique_users(df):
    """
    Plots a line plot with dots for yearly unique users using Plotly.

    Parameters:
    df (pandas.DataFrame): DataFrame containing 'QUERY_YEAR' and 'CUMULATIVE_USERS' columns.
    """
    fig = px.line(df, 
                  x='QUERY_YEAR', 
                  y='CUMULATIVE_USERS', 
                  markers=True, 
                  title='Yearly Unique Users Over Time')
    
    fig.update_traces(line=dict(shape='linear'), mode='lines+markers')
    fig.update_layout(xaxis_title='Year', yaxis_title='Cumulative Unique Users')

    return fig

def bar_plot_yearly_unique_users(df):
    """
    Plots a bar plot with a line fit over each year and a secondary y-axis for the percentage of total unique users.

    Parameters:
    df (pandas.DataFrame): DataFrame containing 'QUERY_YEAR' and 'CUMULATIVE_USERS' columns.
    """
    # Calculate the percentage of total for each year
    total_users = df['CUMULATIVE_USERS'].max()
    df['PERCENT_OF_TOTAL'] = (df['CUMULATIVE_USERS'] / total_users) * 100

    # Create the bar plot
    fig = go.Figure()

    # Add bar trace
    fig.add_trace(
        go.Bar(
            x=df['QUERY_YEAR'],
            y=df['CUMULATIVE_USERS'],
            name='Cumulative Unique Users',
            yaxis='y1'
        )
    )

    # Add percentage line trace
    fig.add_trace(
        go.Scatter(
            x=df['QUERY_YEAR'],
            y=df['PERCENT_OF_TOTAL'],
            mode='lines+markers',
            name='Percentage of Total',
            yaxis='y2',
        )
    )

    # Update layout for dual y-axes
    fig.update_layout(
        title='Yearly Unique Users with Percentage of Total',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Cumulative Unique Users', side='left', range=[0, total_users], anchor='x'),
        yaxis2=dict(
            title='Percentage of Total (%)',
            overlaying='y',
            side='right',
            showgrid=False,
            range=[0, 100],
            anchor='x'
        ),
        legend=dict(x=0.1, y=1.1, orientation='h')
    )

    return fig
