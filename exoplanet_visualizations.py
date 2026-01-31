"""
Exoplanet Data Visualization Module

Provides comprehensive visualization tools for exoplanet data including:
- 3D galaxy view of exoplanet positions
- Interactive scatter plots
- Discovery timeline
- Detection method analysis
- Habitable zone visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (12, 8)


class ExoplanetVisualizer:
    """Main class for creating exoplanet data visualizations."""
    
    def __init__(self, data):
        """
        Initialize visualizer with exoplanet data.
        
        Parameters:
        -----------
        data : pandas.DataFrame
            Combined exoplanet dataset
        """
        self.data = data
        
    def plot_3d_galaxy_view(self, save_html=True):
        """
        Create interactive 3D visualization of exoplanet positions in space.
        """
        print("Creating 3D galaxy view...")
        
        # Filter data with valid coordinates
        plot_data = self.data.dropna(subset=['x_pc', 'y_pc', 'z_pc'])
        
        # Color by planet type or discovery method
        color_column = 'planet_type' if 'planet_type' in plot_data.columns else 'discovery_method'
        
        # Create 3D scatter plot
        fig = go.Figure(data=[go.Scatter3d(
            x=plot_data['x_pc'],
            y=plot_data['y_pc'],
            z=plot_data['z_pc'],
            mode='markers',
            marker=dict(
                size=5,
                color=plot_data[color_column].astype('category').cat.codes,
                colorscale='Viridis',
                showscale=True,
                opacity=0.8,
                colorbar=dict(title=color_column)
            ),
            text=plot_data['planet_name'],
            hovertemplate='<b>%{text}</b><br>' +
                         'X: %{x:.1f} pc<br>' +
                         'Y: %{y:.1f} pc<br>' +
                         'Z: %{z:.1f} pc<br>' +
                         '<extra></extra>',
        )])
        
        # Add Sun at origin
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers',
            marker=dict(size=15, color='yellow', symbol='diamond'),
            name='Sun',
            hovertext='Solar System'
        ))
        
        fig.update_layout(
            title='3D Distribution of Exoplanets in Space',
            scene=dict(
                xaxis_title='X (parsecs)',
                yaxis_title='Y (parsecs)',
                zaxis_title='Z (parsecs)',
                bgcolor='rgb(10, 10, 30)',
            ),
            showlegend=True,
            height=800,
            paper_bgcolor='rgb(20, 20, 40)',
            font=dict(color='white')
        )
        
        if save_html:
            fig.write_html('exoplanet_3d_view.html')
            print("Saved to exoplanet_3d_view.html")
        
        return fig
    
    def plot_mass_radius_diagram(self, save_html=True):
        """
        Create mass-radius diagram with planet type classifications.
        """
        print("Creating mass-radius diagram...")
        
        plot_data = self.data.dropna(subset=['planet_mass_earth', 'planet_radius_earth'])
        
        fig = px.scatter(
            plot_data,
            x='planet_mass_earth',
            y='planet_radius_earth',
            color='planet_type',
            log_x=True,
            log_y=True,
            hover_data=['planet_name', 'host_star', 'discovery_method'],
            title='Exoplanet Mass-Radius Diagram',
            labels={
                'planet_mass_earth': 'Mass (Earth masses)',
                'planet_radius_earth': 'Radius (Earth radii)',
                'planet_type': 'Planet Type'
            },
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        # Add reference lines for Earth and Jupiter
        fig.add_hline(y=1, line_dash="dash", line_color="green", 
                     annotation_text="Earth radius")
        fig.add_vline(x=1, line_dash="dash", line_color="green",
                     annotation_text="Earth mass")
        fig.add_hline(y=11.2, line_dash="dash", line_color="orange",
                     annotation_text="Jupiter radius")
        fig.add_vline(x=317.8, line_dash="dash", line_color="orange",
                     annotation_text="Jupiter mass")
        
        fig.update_layout(
            height=700,
            hovermode='closest',
            template='plotly_dark'
        )
        
        if save_html:
            fig.write_html('exoplanet_mass_radius.html')
            print("Saved to exoplanet_mass_radius.html")
        
        return fig
    
    def plot_discovery_timeline(self, save_html=True):
        """
        Visualize exoplanet discoveries over time by method.
        """
        print("Creating discovery timeline...")
        
        plot_data = self.data.dropna(subset=['discovery_year'])
        
        # Count discoveries by year and method
        timeline = plot_data.groupby(['discovery_year', 'discovery_method']).size().reset_index(name='count')
        
        fig = px.area(
            timeline,
            x='discovery_year',
            y='count',
            color='discovery_method',
            title='Exoplanet Discoveries Over Time by Detection Method',
            labels={
                'discovery_year': 'Year',
                'count': 'Number of Discoveries',
                'discovery_method': 'Detection Method'
            },
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        
        fig.update_layout(
            height=600,
            hovermode='x unified',
            template='plotly_dark',
            xaxis=dict(range=[1990, 2025])
        )
        
        if save_html:
            fig.write_html('exoplanet_discovery_timeline.html')
            print("Saved to exoplanet_discovery_timeline.html")
        
        return fig
    
    def plot_detection_methods(self):
        """
        Create pie chart and bar chart of detection methods.
        """
        print("Creating detection method analysis...")
        
        method_counts = self.data['discovery_method'].value_counts()
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Pie chart
        colors = sns.color_palette("husl", len(method_counts))
        ax1.pie(method_counts.values, labels=method_counts.index, autopct='%1.1f%%',
               colors=colors, startangle=90)
        ax1.set_title('Exoplanet Detection Methods Distribution', fontsize=14, fontweight='bold')
        
        # Bar chart
        method_counts.plot(kind='barh', ax=ax2, color=colors)
        ax2.set_xlabel('Number of Planets', fontsize=12)
        ax2.set_title('Detection Methods (Count)', fontsize=14, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('detection_methods.png', dpi=300, bbox_inches='tight')
        print("Saved to detection_methods.png")
        
        return fig
    
    def plot_habitable_zone_analysis(self, save_html=True):
        """
        Visualize planets in the habitable zone.
        """
        print("Creating habitable zone analysis...")
        
        plot_data = self.data.dropna(subset=['orbital_distance_au', 'equilibrium_temp_k'])
        
        # Create scatter plot
        fig = px.scatter(
            plot_data,
            x='orbital_distance_au',
            y='equilibrium_temp_k',
            color='in_habitable_zone',
            size='planet_radius_earth',
            hover_data=['planet_name', 'host_star', 'planet_type'],
            log_x=True,
            title='Exoplanet Orbital Distance vs. Temperature (Habitable Zone)',
            labels={
                'orbital_distance_au': 'Orbital Distance (AU)',
                'equilibrium_temp_k': 'Equilibrium Temperature (K)',
                'in_habitable_zone': 'In Habitable Zone',
                'planet_radius_earth': 'Radius (Earth radii)'
            },
            color_discrete_map={True: 'green', False: 'gray'}
        )
        
        # Add habitable zone temperature range (roughly 273-373 K for liquid water)
        fig.add_hrect(y0=273, y1=373, fillcolor="green", opacity=0.2,
                     layer="below", line_width=0,
                     annotation_text="Habitable Zone (Water)", annotation_position="top left")
        
        fig.update_layout(
            height=700,
            hovermode='closest',
            template='plotly_dark'
        )
        
        if save_html:
            fig.write_html('exoplanet_habitable_zone.html')
            print("Saved to exoplanet_habitable_zone.html")
        
        return fig
    
    def plot_stellar_properties(self):
        """
        Analyze host star properties.
        """
        print("Creating stellar properties analysis...")
        
        plot_data = self.data.dropna(subset=['stellar_mass_solar', 'stellar_temp_k'])
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Stellar mass distribution
        axes[0, 0].hist(plot_data['stellar_mass_solar'], bins=50, 
                       color='orange', alpha=0.7, edgecolor='black')
        axes[0, 0].axvline(1.0, color='red', linestyle='--', linewidth=2, label='Sun')
        axes[0, 0].set_xlabel('Stellar Mass (Solar masses)', fontsize=11)
        axes[0, 0].set_ylabel('Count', fontsize=11)
        axes[0, 0].set_title('Distribution of Host Star Masses', fontsize=12, fontweight='bold')
        axes[0, 0].legend()
        axes[0, 0].grid(alpha=0.3)
        
        # Stellar temperature distribution
        axes[0, 1].hist(plot_data['stellar_temp_k'], bins=50,
                       color='skyblue', alpha=0.7, edgecolor='black')
        axes[0, 1].axvline(5778, color='red', linestyle='--', linewidth=2, label='Sun')
        axes[0, 1].set_xlabel('Stellar Temperature (K)', fontsize=11)
        axes[0, 1].set_ylabel('Count', fontsize=11)
        axes[0, 1].set_title('Distribution of Host Star Temperatures', fontsize=12, fontweight='bold')
        axes[0, 1].legend()
        axes[0, 1].grid(alpha=0.3)
        
        # HR Diagram
        axes[1, 0].scatter(plot_data['stellar_temp_k'], 
                          plot_data['stellar_mass_solar'],
                          alpha=0.5, s=20, c='purple')
        axes[1, 0].scatter(5778, 1.0, color='yellow', s=200, 
                          marker='*', edgecolors='red', linewidths=2, 
                          label='Sun', zorder=5)
        axes[1, 0].set_xlabel('Stellar Temperature (K)', fontsize=11)
        axes[1, 0].set_ylabel('Stellar Mass (Solar masses)', fontsize=11)
        axes[1, 0].set_title('Simplified HR Diagram of Host Stars', fontsize=12, fontweight='bold')
        axes[1, 0].invert_xaxis()
        axes[1, 0].legend()
        axes[1, 0].grid(alpha=0.3)
        
        # Distance distribution
        dist_data = self.data.dropna(subset=['stellar_distance_pc'])
        axes[1, 1].hist(dist_data['stellar_distance_pc'], bins=50,
                       color='green', alpha=0.7, edgecolor='black')
        axes[1, 1].set_xlabel('Distance (parsecs)', fontsize=11)
        axes[1, 1].set_ylabel('Count', fontsize=11)
        axes[1, 1].set_title('Distribution of Host Star Distances', fontsize=12, fontweight='bold')
        axes[1, 1].set_xlim(0, dist_data['stellar_distance_pc'].quantile(0.95))
        axes[1, 1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('stellar_properties.png', dpi=300, bbox_inches='tight')
        print("Saved to stellar_properties.png")
        
        return fig
    
    def create_dashboard(self, save_html=True):
        """
        Create a comprehensive interactive dashboard with multiple views.
        """
        print("Creating comprehensive dashboard...")
        
        # Create subplots
        from plotly.subplots import make_subplots
        
        # Prepare data
        method_counts = self.data['discovery_method'].value_counts().head(8)
        type_counts = self.data['planet_type'].value_counts()
        
        # Create figure with subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Detection Methods', 'Planet Types', 
                          'Discovery Timeline', 'Mass vs Radius'),
            specs=[[{"type": "pie"}, {"type": "pie"}],
                  [{"type": "scatter"}, {"type": "scatter"}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Detection methods pie
        fig.add_trace(
            go.Pie(labels=method_counts.index, values=method_counts.values,
                  name="Detection Methods"),
            row=1, col=1
        )
        
        # 2. Planet types pie
        fig.add_trace(
            go.Pie(labels=type_counts.index, values=type_counts.values,
                  name="Planet Types"),
            row=1, col=2
        )
        
        # 3. Discovery timeline
        timeline_data = self.data.dropna(subset=['discovery_year'])
        yearly_counts = timeline_data.groupby('discovery_year').size().reset_index(name='count')
        fig.add_trace(
            go.Scatter(x=yearly_counts['discovery_year'], 
                      y=yearly_counts['count'],
                      mode='lines+markers',
                      name='Discoveries',
                      line=dict(color='cyan', width=3)),
            row=2, col=1
        )
        
        # 4. Mass vs Radius
        mr_data = self.data.dropna(subset=['planet_mass_earth', 'planet_radius_earth'])
        fig.add_trace(
            go.Scatter(x=mr_data['planet_mass_earth'],
                      y=mr_data['planet_radius_earth'],
                      mode='markers',
                      name='Planets',
                      marker=dict(size=5, opacity=0.6, color='orange'),
                      text=mr_data['planet_name']),
            row=2, col=2
        )
        
        # Update layout
        fig.update_xaxes(title_text="Year", row=2, col=1)
        fig.update_yaxes(title_text="Count", row=2, col=1)
        fig.update_xaxes(title_text="Mass (Earth)", type="log", row=2, col=2)
        fig.update_yaxes(title_text="Radius (Earth)", type="log", row=2, col=2)
        
        fig.update_layout(
            title_text="Exoplanet Data Dashboard",
            showlegend=False,
            height=900,
            template='plotly_dark'
        )
        
        if save_html:
            fig.write_html('exoplanet_dashboard.html')
            print("Saved to exoplanet_dashboard.html")
        
        return fig
    
    def generate_all_visualizations(self):
        """
        Generate all available visualizations.
        """
        print("\n" + "="*60)
        print("GENERATING ALL VISUALIZATIONS")
        print("="*60 + "\n")
        
        self.plot_3d_galaxy_view()
        self.plot_mass_radius_diagram()
        self.plot_discovery_timeline()
        self.plot_detection_methods()
        self.plot_habitable_zone_analysis()
        self.plot_stellar_properties()
        self.create_dashboard()
        
        print("\n" + "="*60)
        print("ALL VISUALIZATIONS COMPLETE!")
        print("="*60 + "\n")


def main():
    """Main function to demonstrate visualization."""
    # Load data
    try:
        data = pd.read_csv('exoplanet_combined_data.csv')
        print(f"Loaded {len(data)} planets from exoplanet_combined_data.csv")
    except FileNotFoundError:
        print("Error: exoplanet_combined_data.csv not found.")
        print("Please run exoplanet_data_sources.py first to collect data.")
        return
    
    # Create visualizer
    viz = ExoplanetVisualizer(data)
    
    # Generate all visualizations
    viz.generate_all_visualizations()


if __name__ == "__main__":
    main()
