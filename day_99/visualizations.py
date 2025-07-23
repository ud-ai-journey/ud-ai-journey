import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_energy_chart(energy_data):
    """
    Create a comprehensive energy visualization chart
    """
    if energy_data.empty:
        # Return empty chart
        fig = go.Figure()
        fig.add_annotation(
            text="No data available yet. Start tracking your energy!",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title="Energy Patterns",
            xaxis_title="Time",
            yaxis_title="Energy Level",
            height=400
        )
        return fig
    
    # Prepare data
    energy_data = energy_data.sort_values('timestamp')
    
    # Create energy score mapping
    energy_scores = energy_data['energy_level'].map({'High': 3, 'Medium': 2, 'Low': 1})
    
    # Create the main chart
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Energy Timeline', 'Energy Distribution', 'Hourly Patterns', 'Daily Patterns'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # 1. Energy Timeline
    fig.add_trace(
        go.Scatter(
            x=energy_data['timestamp'],
            y=energy_scores,
            mode='lines+markers',
            name='Energy Level',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=8, color=energy_scores, colorscale='RdYlGn')
        ),
        row=1, col=1
    )
    
    # 2. Energy Distribution
    energy_dist = energy_data['energy_level'].value_counts()
    colors = {'High': '#2ecc71', 'Medium': '#f39c12', 'Low': '#e74c3c'}
    
    fig.add_trace(
        go.Bar(
            x=energy_dist.index,
            y=energy_dist.values,
            name='Energy Distribution',
            marker_color=[colors.get(level, '#95a5a6') for level in energy_dist.index]
        ),
        row=1, col=2
    )
    
    # 3. Hourly Patterns
    if 'hour' in energy_data.columns:
        hourly_data = energy_data.groupby(['hour', 'energy_level']).size().unstack(fill_value=0)
        
        for energy_level in ['High', 'Medium', 'Low']:
            if energy_level in hourly_data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=hourly_data.index,
                        y=hourly_data[energy_level],
                        mode='lines+markers',
                        name=f'{energy_level} Energy',
                        line=dict(color=colors.get(energy_level, '#95a5a6')),
                        marker=dict(size=6)
                    ),
                    row=2, col=1
                )
    
    # 4. Daily Patterns
    if 'day_of_week' in energy_data.columns:
        daily_data = energy_data.groupby(['day_of_week', 'energy_level']).size().unstack(fill_value=0)
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_data = daily_data.reindex([day for day in day_order if day in daily_data.index])
        
        for energy_level in ['High', 'Medium', 'Low']:
            if energy_level in daily_data.columns:
                fig.add_trace(
                    go.Bar(
                        x=daily_data.index,
                        y=daily_data[energy_level],
                        name=f'{energy_level} Energy',
                        marker_color=colors.get(energy_level, '#95a5a6')
                    ),
                    row=2, col=2
                )
    
    # Update layout
    fig.update_layout(
        title="⚡ Energy Lens - Pattern Analysis",
        height=600,
        showlegend=True,
        template="plotly_white"
    )
    
    # Update axes
    fig.update_xaxes(title_text="Time", row=1, col=1)
    fig.update_yaxes(title_text="Energy Level (1=Low, 2=Medium, 3=High)", row=1, col=1)
    fig.update_xaxes(title_text="Energy Level", row=1, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=2)
    fig.update_xaxes(title_text="Hour of Day", row=2, col=1)
    fig.update_yaxes(title_text="Count", row=2, col=1)
    fig.update_xaxes(title_text="Day of Week", row=2, col=2)
    fig.update_yaxes(title_text="Count", row=2, col=2)
    
    return fig

def create_pattern_insights(energy_data):
    """
    Create insights visualization
    """
    if energy_data.empty:
        return None
    
    # Calculate insights
    total_records = len(energy_data)
    avg_confidence = energy_data['confidence'].mean()
    energy_dist = energy_data['energy_level'].value_counts(normalize=True)
    
    # Create insights figure
    fig = go.Figure()
    
    # Add gauge charts for key metrics
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=avg_confidence,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Detection Confidence"},
        delta={'reference': 70},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        title="📊 Energy Detection Insights",
        height=300
    )
    
    return fig

def create_weekly_summary(energy_data):
    """
    Create a weekly summary visualization
    """
    if energy_data.empty:
        return None
    
    # Filter for last 7 days
    # Ensure 'timestamp' is timezone-naive for comparison
    ts = energy_data['timestamp']
    if hasattr(ts.dt, 'tz') and ts.dt.tz is not None:
        ts = ts.dt.tz_localize(None)
    week_ago = datetime.now()
    weekly_data = energy_data[ts >= week_ago - timedelta(days=7)]
    
    if weekly_data.empty:
        return None
    
    # Create weekly heatmap
    if 'hour' in weekly_data.columns and 'day_of_week' in weekly_data.columns:
        # Create pivot table for heatmap
        energy_scores = weekly_data['energy_level'].map({'High': 3, 'Medium': 2, 'Low': 1})
        weekly_data['energy_score'] = energy_scores
        
        pivot_data = weekly_data.pivot_table(
            values='energy_score',
            index='day_of_week',
            columns='hour',
            aggfunc='mean',
            fill_value=0
        )
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot_data = pivot_data.reindex([day for day in day_order if day in pivot_data.index])
        
        fig = px.imshow(
            pivot_data,
            title="📅 Weekly Energy Heatmap",
            color_continuous_scale='RdYlGn',
            aspect="auto"
        )
        
        fig.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Day of Week",
            height=400
        )
        
        return fig
    
    return None

def create_productivity_chart(energy_data):
    """
    Create productivity-focused visualization
    """
    if energy_data.empty:
        return None
    
    # Calculate productivity metrics
    high_energy_pct = (energy_data['energy_level'] == 'High').mean() * 100
    low_energy_pct = (energy_data['energy_level'] == 'Low').mean() * 100
    
    # Create productivity gauge
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=high_energy_pct,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "High Energy Time (%)"},
        delta={'reference': 40},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, 30], 'color': "lightgray"},
                {'range': [30, 50], 'color': "yellow"},
                {'range': [50, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    
    fig.update_layout(
        title="🎯 Productivity Score",
        height=300
    )
    
    return fig

def create_energy_trend(energy_data):
    """
    Create energy trend analysis
    """
    if energy_data.empty or len(energy_data) < 3:
        return None
    
    # Sort by timestamp
    sorted_data = energy_data.sort_values('timestamp')
    
    # Calculate moving average
    energy_scores = sorted_data['energy_level'].map({'High': 3, 'Medium': 2, 'Low': 1})
    moving_avg = energy_scores.rolling(window=3, min_periods=1).mean()
    
    fig = go.Figure()
    
    # Add actual energy levels
    fig.add_trace(go.Scatter(
        x=sorted_data['timestamp'],
        y=energy_scores,
        mode='markers',
        name='Actual Energy',
        marker=dict(size=8, color=energy_scores, colorscale='RdYlGn')
    ))
    
    # Add trend line
    fig.add_trace(go.Scatter(
        x=sorted_data['timestamp'],
        y=moving_avg,
        mode='lines',
        name='Trend (3-day avg)',
        line=dict(color='blue', width=3)
    ))
    
    fig.update_layout(
        title="📈 Energy Trend Analysis",
        xaxis_title="Time",
        yaxis_title="Energy Level (1=Low, 2=Medium, 3=High)",
        height=400
    )
    
    return fig 