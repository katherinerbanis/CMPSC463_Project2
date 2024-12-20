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

        # frame for dropdown and button
        analysis_frame = tk.Frame(tab)
        analysis_frame.pack(fill="x", padx=10, pady=10)

        # City dropdown
        city_dropdown = ttk.Combobox(analysis_frame, values=self.data["City"].unique().tolist(), width=30)
        city_dropdown.pack(pady=5)

        # View Data Button
        ttk.Button(analysis_frame, text="View City Data", command=lambda: self.view_city_data(tab, city_dropdown.get())).pack()

        # frame for displaying data
        self.city_data_frame = tk.Frame(tab)
        self.city_data_frame.pack(fill="both", padx=10, pady=10)

    def view_city_data(self, tab, city):
        """Display city-specific data in a tab"""
        # Clear any existing widgets in the tab
        for widget in self.city_data_frame.winfo_children():
            widget.destroy()

        # Get filtered data for the selected city
        filtered = self.data[self.data["City"] == city]

        if filtered.empty:
            tk.Label(self.city_data_frame, text="No data available for the selected city.", font=("Arial", 12)).pack()
            return

        # Display data in vertical layout
        for i, (col, value) in enumerate(filtered.iloc[0].items()):
            label = tk.Label(self.city_data_frame, text=f"{col}: {value}", font=("Arial", 12), anchor="w")
            label.pack(fill="x", pady=5)

    def create_heatmap_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Heatmap")

        # create a frame inside the tab for the heatmap
        heatmap_frame = tk.Frame(tab)
        heatmap_frame.pack(fill="both", expand=True)

        # add a button to generate heatmap
        ttk.Button(tab, text="Generate Heatmap", command=lambda: self.plot_heatmap(heatmap_frame)).pack(pady=10)

    def plot_heatmap(self, frame):
        """Display a heatmap of crime correlations in the graph_frame."""
        # Clear previous plots
        for widget in frame.winfo_children():
            widget.destroy()

        # Plot the heatmap using matplotlib
        correlations = self.data[["Violent Crime", "Property Crime", "Burglary", "Larceny-Theft", "Arson"]].corr()
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.heatmap(correlations, annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Crime Category Correlations", fontsize=15)
        ax.set_xticklabels(correlations.index, rotation=0, fontsize=10)
        ax.set_yticklabels(correlations.index, rotation=90, fontsize=10)

        # Embed the plot into the graph_frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
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

        # create a frame inside the tab for the comparison
        comparison_frame = tk.Frame(tab)
        comparison_frame.pack(fill="both", expand=True)

        # Compare Button
        ttk.Button(tab, text="Compare Cities",
                   command=lambda: self.compare_cities(comparison_frame, city1_dropdown.get(), city2_dropdown.get())).pack()

    def compare_cities(self, frame, city1, city2):
        """Compare two cities' crime statistics in the graph_frame."""
        # Clear previous plots
        for widget in frame.winfo_children():
            widget.destroy()

        # Get filtered data for the selected cities
        filtered1 = self.data[self.data["City"] == city1]
        filtered2 = self.data[self.data["City"] == city2]

        if filtered1.empty or filtered2.empty:
            tk.Label(self.graph_frame, text="Data for one or both cities is unavailable.", font=("Arial", 12)).pack()
            return

        # Combine data for plotting
        combined = pd.concat([filtered1, filtered2])

        # Plot a grouped bar chart using matplotlib
        fig, ax = plt.subplots(figsize=(3, 2))
        combined.plot(kind="bar", x="City", y=["Violent Crime", "Property Crime"], ax=ax, color=["blue", "orange"])
        ax.set_title("City Comparison: Violent vs Property Crime")
        ax.set_xlabel("City")
        ax.set_ylabel("Number of Crimes")
        ax.set_xticklabels(combined.index, rotation=0, fontsize=10)
        ax.set_yticklabels(combined.index, rotation=90, fontsize=10)
        ax.legend()

        # Embed the plot into the graph_frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
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

    def clear_graph_frames(self):
        """Clear the graph display area to avoid overlapping graphs."""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

    def create_prediction_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Prediction & Analysis")

        # Create a parent frame to hold left and right frames
        prediction_frame = tk.Frame(tab)
        prediction_frame.pack(fill="both", expand=True)

        # Create left and right frames for buttons and plots
        left_frame = tk.Frame(prediction_frame, width=400, height=300, borderwidth=1, relief="solid")
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill="both", expand=True)

        right_frame = tk.Frame(prediction_frame, width=400, height=300, borderwidth=1, relief="solid")
        right_frame.pack(side=tk.LEFT, padx=10, pady=10, fill="both", expand=True)

        # Add buttons that call methods with the respective frames
        ttk.Button(left_frame, text="Predict Future Crimes", command=lambda: self.predict_crimes(left_frame)).pack(
            pady=10)
        ttk.Button(right_frame, text="Cluster Cities", command=lambda: self.cluster_cities(right_frame)).pack(pady=10)

    def predict_crimes(self, frame):
        """Predict future violent crime rates using a linear regression model."""
        # Clear previous plots
        for widget in frame.winfo_children():
            widget.destroy()

        # Prepare data for prediction
        features = self.data[["Population", "Property Crime Rate"]].values
        target = self.data["Violent Crime Rate"].values

        if len(features) < 2:
            tk.Label(frame, text="Not enough data for predictions.", font=("Arial", 12)).pack()
            return

        # Train the linear regression model
        model = LinearRegression()
        model.fit(features, target)
        future_populations = np.linspace(self.data["Population"].min(), self.data["Population"].max(), 100)
        future_property_crime_rates = np.linspace(self.data["Property Crime Rate"].min(),
                                                  self.data["Property Crime Rate"].max(), 100)
        future_features = np.array(list(zip(future_populations, future_property_crime_rates)))
        predictions = model.predict(future_features)

        # Plot the predictions
        fig, ax = plt.subplots(figsize=(4, 3))  # Smaller plot size
        ax.plot(future_populations, predictions, label="Predicted Violent Crime Rate", color="blue")
        ax.set_title("Predicted Violent Crime Rates", fontsize=12)
        ax.set_xlabel("Population", fontsize=10)
        ax.set_ylabel("Predicted Violent Crime Rate", fontsize=10)
        ax.legend()

        # Embed the plot in the passed frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def cluster_cities(self, frame):
        """Perform KMeans clustering on cities based on crime statistics."""
        # Clear previous plots
        for widget in frame.winfo_children():
            widget.destroy()

        # Prepare data for clustering
        features = self.data[["Violent Crime Rate", "Property Crime Rate"]].values
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(scaled_features)
        self.data["Cluster"] = clusters

        # Plot the clusters
        fig, ax = plt.subplots(figsize=(4, 3))  # Smaller plot size
        colors = ['red', 'green', 'blue']

        for cluster_id in range(3):
            cluster_data = self.data[self.data["Cluster"] == cluster_id]
            ax.scatter(cluster_data["Violent Crime Rate"], cluster_data["Property Crime Rate"],
                       label=f"Cluster {cluster_id}", color=colors[cluster_id])

        ax.set_title("Clustering of Cities Based on Crime Rates", fontsize=12)
        ax.set_xlabel("Violent Crime Rate", fontsize=10)
        ax.set_ylabel("Property Crime Rate", fontsize=10)
        ax.legend()

        # Embed the plot in the passed frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()


if __name__ == "__main__":
    file_path = "pa_crime_data.xls"  # Replace with your actual file path
    root = tk.Tk()
    app = CrimeAnalysisApp(root, file_path)
    root.mainloop()
