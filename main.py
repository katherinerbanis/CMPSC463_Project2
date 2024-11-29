import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns


class CrimeAnalysisApp:
    def __init__(self, root, data_file):
        self.root = root
        self.root.title("Crime Rate by PA City")
        self.root.state("zoomed")  # Fullscreen mode

        # Load and preprocess the dataset
        self.data = self.load_data(data_file)

        # Initialize variables
        self.graph_frame = None

        # Setup UI
        self.create_widgets()

    def load_data(self, file_path):
        # Load dataset
        data = pd.read_excel(file_path, skiprows=4)

        # Rename columns for convenience
        data.columns = [
            "City", "Population", "Violent Crime", "Murder and Non-Negligent Manslaughter",
            "Rape (Revised Definition)", "Rape (Legacy Definition)", "Robbery",
            "Aggravated Assault", "Property Crime", "Burglary",
            "Larceny-Theft", "Motor Vehicle Theft", "Arson"
        ]

        # Data cleaning
        data.fillna(0, inplace=True)
        data["City"] = data["City"].str.strip()  # Strip whitespace
        data["Violent Crime Rate"] = (data["Violent Crime"] / data["Population"]) * 1000
        data["Property Crime Rate"] = (data["Property Crime"] / data["Population"]) * 1000
        return data

    def create_widgets(self):
        # Dropdown for city selection
        tk.Label(self.root, text="Select a City:", font=("Arial", 12)).pack(pady=5)
        self.city_dropdown = ttk.Combobox(self.root, values=self.data["City"].unique().tolist(), width=30)
        self.city_dropdown.pack()

        # Button Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Buttons in a row
        tk.Button(button_frame, text="View Data", command=self.view_data, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Plot Side-by-Side", command=self.plot_side_by_side, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Show Top/Bottom Cities", command=self.show_top_bottom_cities, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Export Data", command=self.export_data, width=15).pack(side=tk.LEFT, padx=5)

        # Frame for data display
        self.data_frame = tk.Frame(self.root, height=150)
        self.data_frame.pack(fill="both", expand=False, pady=5)

        # Graph Frame
        self.graph_frame = tk.Frame(self.root)
        self.graph_frame.pack(fill="both", expand=True)

        # Configure resizing weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

    def clear_graph_frames(self):
        """Clear the graph display area to avoid overlapping graphs."""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

    def view_data(self):
        city = self.city_dropdown.get()
        filtered = self.filter_data(city=city)

        # Clear previous data display
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        if filtered.empty:
            tk.Label(self.data_frame, text="No data available for the selected city.", font=("Arial", 12)).pack()
            return

        # Display filtered data in a table
        for i, col in enumerate(filtered.columns):
            tk.Label(self.data_frame, text=col, font=("Arial", 10, "bold")).grid(row=0, column=i)
        for i, row in enumerate(filtered.itertuples()):
            for j, value in enumerate(row[1:]):
                tk.Label(self.data_frame, text=value).grid(row=i + 1, column=j)

    def filter_data(self, city=None):
        filtered = self.data
        if city:
            filtered = filtered[filtered["City"] == city]
        return filtered

    def plot_side_by_side(self):
        """Plot the crime trends on the left and the heatmap on the right."""
        self.clear_graph_frames()

        # Left Frame for Crime Trends
        left_frame = tk.Frame(self.graph_frame, width=300, height=200)
        left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)

        # Right Frame for Heatmap
        right_frame = tk.Frame(self.graph_frame, width=300, height=200)
        right_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=5, pady=5)

        # Plot Crime Trends on the Left
        crime_totals = self.data[["Violent Crime", "Property Crime", "Burglary", "Larceny-Theft", "Arson"]].sum()
        fig1, ax1 = plt.subplots(figsize=(4, 2))  # Smaller plot size
        crime_totals.plot(kind="bar", ax=ax1, color="skyblue")
        ax1.set_title("Total Crimes by Category in PA", fontsize=10)
        ax1.set_ylabel("Number of Crimes", fontsize=8)
        ax1.set_xticklabels(crime_totals.index, rotation=0, fontsize=8)

        canvas1 = FigureCanvasTkAgg(fig1, master=left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)

        # Plot Heatmap on the Right
        correlations = self.data[["Violent Crime", "Property Crime", "Burglary", "Larceny-Theft", "Arson"]].corr()
        fig2, ax2 = plt.subplots(figsize=(4, 2))  # Smaller plot size
        sns.heatmap(correlations, annot=True, cmap="coolwarm", ax=ax2, cbar=True, annot_kws={"size": 5})
        ax2.set_title("Crime Category Correlations", fontsize=10)
        ax2.set_xticklabels(correlations.index, rotation=0, fontsize=8)
        ax2.set_yticklabels(correlations.index, rotation=90, fontsize=8)

        canvas2 = FigureCanvasTkAgg(fig2, master=right_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)

    def show_top_bottom_cities(self):
        top_cities = self.data.nlargest(5, "Violent Crime Rate")
        bottom_cities = self.data.nsmallest(5, "Violent Crime Rate")

        # Clear previous data display
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        # Display Top and Bottom Cities
        tk.Label(self.data_frame, text="Top 5 Cities by Violent Crime Rate", font=("Arial", 12, "bold")).pack()
        for _, row in top_cities.iterrows():
            tk.Label(self.data_frame, text=f"{row['City']}: {row['Violent Crime Rate']:.2f} per 1,000 residents").pack()

        tk.Label(self.data_frame, text="Bottom 5 Cities by Violent Crime Rate", font=("Arial", 12, "bold")).pack()
        for _, row in bottom_cities.iterrows():
            tk.Label(self.data_frame, text=f"{row['City']}: {row['Violent Crime Rate']:.2f} per 1,000 residents").pack()

    def export_data(self):
        city = self.city_dropdown.get()
        filtered = self.filter_data(city=city)

        if filtered.empty:
            messagebox.showerror("Error", "No data available to export for the selected city.")
            return

        # Save to CSV
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            filtered.to_csv(file_path, index=False)
            messagebox.showinfo("Export Successful", f"Data for {city} exported successfully!")


if __name__ == "__main__":
    file_path = "pa_crime_data.xls"  # Replace with your actual file path
    root = tk.Tk()
    app = CrimeAnalysisApp(root, file_path)
    root.mainloop()
