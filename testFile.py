import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
from tkintermapview import TkinterMapView
import numpy as np
import plotly.graph_objects as go


class CrimeAnalysisApp:
    def __init__(self, root, data_file):
        self.root = root
        self.root.title("Enhanced Crime Analysis")
        self.root.state("zoomed")  # Fullscreen mode

        # Load and preprocess the dataset
        self.data = self.load_data(data_file)

        # Set up the notebook tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # frame for displaying graphs
        self.graph_frame = tk.Frame(self.root, height=400)
        self.graph_frame.pack(fill="both", expand=True, pady=10)

        # Add tabs
        self.create_city_analysis_tab()
        self.create_heatmap_tab()
        self.create_comparison_tab()
        self.create_interactive_map_tab()
        self.create_prediction_tab()

    def load_data(self, file_path):
        data = pd.read_excel(file_path, skiprows=4)
        data.columns = [
            "City", "Population", "Violent Crime", "Murder and Non-Negligent Manslaughter",
            "Rape", "Robbery", "Aggravated Assault", "Property Crime",
            "Burglary", "Larceny-Theft", "Motor Vehicle Theft", "Arson",
            "Latitude", "Longitude"
        ]
        data.fillna(0, inplace=True)
        data["City"] = data["City"].str.strip()
        data["Violent Crime Rate"] = (data["Violent Crime"] / data["Population"]) * 1000
        data["Property Crime Rate"] = (data["Property Crime"] / data["Population"]) * 1000
        return data

    def create_city_analysis_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="City Analysis")

        # City dropdown
        city_dropdown = ttk.Combobox(tab, values=self.data["City"].unique().tolist(), width=30)
        city_dropdown.pack(pady=10)

        # View Data Button
        ttk.Button(tab, text="View City Data", command=lambda: self.view_city_data(tab, city_dropdown.get())).pack()

    def view_city_data(self, tab, city):
        """Display city-specific data in a tab"""
        # Clear any existing widgets in the tab
        for widget in tab.winfo_children():
            widget.destroy()

        # Get filtered data for the selected city
        filtered = self.data[self.data["City"] == city]

        if filtered.empty:
            tk.Label(tab, text="No data available for the selected city.", font=("Arial", 12)).pack()
            return

        # Use a frame for the grid layout
        table_frame = tk.Frame(tab)
        table_frame.pack(fill="both", expand=True)

        # Display column headers
        for i, col in enumerate(filtered.columns):
            tk.Label(table_frame, text=col, font=("Arial", 10, "bold"), borderwidth=1, relief="solid").grid(row=0,
                                                                                                            column=i)

        # Display rows of data
        for i, row in enumerate(filtered.itertuples(), start=1):
            for j, value in enumerate(row[1:]):
                tk.Label(table_frame, text=value, borderwidth=1, relief="solid").grid(row=i, column=j)

    def create_heatmap_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Heatmap")
        ttk.Button(tab, text="Generate Heatmap", command=lambda: self.plot_heatmap(tab)).pack(pady=10)

    def plot_heatmap(self, tab):
        """Display a heatmap of crime correlations in the graph_frame."""
        # Clear previous plots
        self.clear_graph_frames()

        # Plot the heatmap using matplotlib
        correlations = self.data[["Violent Crime", "Property Crime", "Burglary", "Larceny-Theft", "Arson"]].corr()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(correlations, annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Crime Category Correlations")

        # Embed the plot into the graph_frame
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_comparison_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="City Comparison")

        # Dropdowns for two cities
        city1_dropdown = ttk.Combobox(tab, values=self.data["City"].unique().tolist(), width=30)
        city1_dropdown.pack(side=tk.LEFT, padx=10, pady=10)
        city2_dropdown = ttk.Combobox(tab, values=self.data["City"].unique().tolist(), width=30)
        city2_dropdown.pack(side=tk.LEFT, padx=10, pady=10)

        # Compare Button
        ttk.Button(tab, text="Compare Cities",
                   command=lambda: self.compare_cities(tab, city1_dropdown.get(), city2_dropdown.get())).pack()

    def compare_cities(self, tab, city1, city2):
        """Compare two cities' crime statistics in the graph_frame."""
        # Clear previous plots
        self.clear_graph_frames()

        # Get filtered data for the selected cities
        filtered1 = self.data[self.data["City"] == city1]
        filtered2 = self.data[self.data["City"] == city2]

        if filtered1.empty or filtered2.empty:
            tk.Label(self.graph_frame, text="Data for one or both cities is unavailable.", font=("Arial", 12)).pack()
            return

        # Combine data for plotting
        combined = pd.concat([filtered1, filtered2])

        # Plot a grouped bar chart using matplotlib
        fig, ax = plt.subplots(figsize=(6, 4))
        combined.plot(kind="bar", x="City", y=["Violent Crime", "Property Crime"], ax=ax, color=["blue", "orange"])
        ax.set_title("City Comparison: Violent vs Property Crime")
        ax.set_xlabel("City")
        ax.set_ylabel("Number of Crimes")
        ax.legend()

        # Embed the plot into the graph_frame
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_interactive_map_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Interactive Map")

        # Map Frame
        map_view = TkinterMapView(tab, width=1200, height=800, corner_radius=0)
        map_view.pack(fill="both", expand=True)

        # set initial center of the map
        map_view.set_position(40.4406, -79.9959)
        map_view.set_zoom(7)

        # Add crime heat zones
        self.add_heat_zones(map_view)

    def add_heat_zones(self, map_view):
        """Add markers to the map based on Latitude and Longitude columns in the dataset."""
        for _, row in self.data.iterrows():
            try:
                # Use latitude and longitude columns for each city
                latitude = row["Latitude"]
                longitude = row["Longitude"]
                if not pd.isna(latitude) and not pd.isna(longitude):
                    # Add a marker to the map
                    map_view.set_marker(latitude, longitude,
                                        text=f"{row['City']}: {row['Violent Crime']} Violent Crimes")
            except Exception as e:
                print(f"Error adding marker for {row['City']}: {e}")


    def create_prediction_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Prediction & Analysis")

        ttk.Button(tab, text="Predict Future Crimes", command=lambda: self.predict_crimes(tab)).pack(pady=10)
        ttk.Button(tab, text="Cluster Cities", command=lambda: self.cluster_cities(tab)).pack(pady=10)

    def clear_graph_frames(self):
        """Clear the graph display area to avoid overlapping graphs."""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

    def predict_crimes(self, tab):
        """Predict future violent crime rates using a linear regression model."""
        # Clear previous plots
        self.clear_graph_frames()

        # Check for sufficient data
        if self.data["Population"].isna().any() or self.data["Property Crime Rate"].isna().any():
            tk.Label(self.graph_frame, text="Data contains missing values. Cannot predict.", font=("Arial", 12)).pack()
            return

        # Prepare data for prediction
        features = self.data[["Population", "Property Crime Rate"]].values
        target = self.data["Violent Crime Rate"].values

        # Check for sufficient data
        if len(features) < 2:
            tk.Label(self.graph_frame, text="Not enough data for predictions.", font=("Arial", 12)).pack()
            return

        # Train the linear regression model
        model = LinearRegression()
        model.fit(features, target)

        # Predict crime rates for a range of populations and property crime rates
        future_populations = np.linspace(self.data["Population"].min(), self.data["Population"].max(), 100)
        future_property_crime_rates = np.linspace(self.data["Property Crime Rate"].min(),
                                                  self.data["Property Crime Rate"].max(), 100)

        future_features = np.array(list(zip(future_populations, future_property_crime_rates)))
        predictions = model.predict(future_features)

        # Plot using matplotlib for Tkinter integration
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(future_populations, predictions, label="Predicted Violent Crime Rate", color="blue")
        ax.set_title("Predicted Violent Crime Rates")
        ax.set_xlabel("Population")
        ax.set_ylabel("Predicted Violent Crime Rate")
        ax.legend()

        # Embed the plot into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def cluster_cities(self, tab):
        """Perform KMeans clustering on cities based on crime statistics."""
        # Clear previous plots
        self.clear_graph_frames()

        # Check for sufficient data
        if self.data[["Violent Crime Rate", "Property Crime Rate"]].isna().any().any():
            tk.Label(self.graph_frame, text="Data contains missing values. Cannot cluster.", font=("Arial", 12)).pack()
            return

        # Select features for clustering
        features = self.data[["Violent Crime Rate", "Property Crime Rate"]].values

        # Scale the features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        # Perform KMeans clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(scaled_features)

        # Add cluster labels to the dataset
        self.data["Cluster"] = clusters

        # Plot using matplotlib for Tkinter integration
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = ['red', 'green', 'blue']

        for cluster_id in range(3):
            cluster_data = self.data[self.data["Cluster"] == cluster_id]
            ax.scatter(cluster_data["Violent Crime Rate"], cluster_data["Property Crime Rate"],
                       label=f"Cluster {cluster_id}", color=colors[cluster_id])

        ax.set_title("Clustering of Cities Based on Crime Rates")
        ax.set_xlabel("Violent Crime Rate")
        ax.set_ylabel("Property Crime Rate")
        ax.legend()

        # Embed the plot into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    file_path = "pa_crime_data.xls"  # Replace with your actual file path
    root = tk.Tk()
    app = CrimeAnalysisApp(root, file_path)
    root.mainloop()
