import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

class CrimeAnalysisApp:
    def __init__(self, root, data_file):
        self.root = root
        self.root.title("Crime Rate by PA City")
        self.root.geometry("900x700")

        # Load and preprocess the dataset
        self.data = self.load_data(data_file)

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
        tk.Label(self.root, text="Select a City:", font=("Arial", 12)).pack()
        self.city_dropdown = ttk.Combobox(self.root, values=self.data["City"].unique().tolist())
        self.city_dropdown.pack()

        # Buttons
        tk.Button(self.root, text="View Data", command=self.view_data).pack(pady=5)
        tk.Button(self.root, text="Plot Crime Trends", command=self.plot_crime_trends).pack(pady=5)
        tk.Button(self.root, text="Show Top/Bottom Cities", command=self.show_top_bottom_cities).pack(pady=5)
        tk.Button(self.root, text="Plot Heatmap", command=self.plot_heatmap).pack(pady=5)
        tk.Button(self.root, text="Export Data", command=self.export_data).pack(pady=5)

        # Frame for data display
        self.data_frame = tk.Frame(self.root)
        self.data_frame.pack(fill="both", expand=True, pady=10)

    def filter_data(self, city=None):
        filtered = self.data
        if city:
            filtered = filtered[filtered["City"] == city]
        return filtered

    def view_data(self):
        city = self.city_dropdown.get()
        filtered = self.filter_data(city=city)

        # Clear previous results
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

    def plot_crime_trends(self):
        crime_totals = self.data[["Violent Crime", "Property Crime", "Burglary", "Larceny-Theft", "Arson"]].sum()

        # Plot trends
        fig, ax = plt.subplots(figsize=(10, 6))
        crime_totals.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Total Crimes by Category in PA")
        ax.set_ylabel("Number of Crimes")
        ax.set_xticks(range(len(crime_totals.index)))
        ax.set_xticklabels(crime_totals.index, rotation=45)

        # Display chart in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_top_bottom_cities(self):
        top_cities = self.data.nlargest(5, "Violent Crime Rate")
        bottom_cities = self.data.nsmallest(5, "Violent Crime Rate")

        # Display in a new window
        top_bottom_window = tk.Toplevel(self.root)
        top_bottom_window.title("Top/Bottom Cities by Crime Rate")

        # Top cities
        tk.Label(top_bottom_window, text="Top 5 Cities by Violent Crime Rate", font=("Arial", 12, "bold")).pack()
        for _, row in top_cities.iterrows():
            tk.Label(top_bottom_window, text=f"{row['City']}: {row['Violent Crime Rate']:.2f} per 1,000 residents").pack()

        # Bottom cities
        tk.Label(top_bottom_window, text="Bottom 5 Cities by Violent Crime Rate", font=("Arial", 12, "bold")).pack()
        for _, row in bottom_cities.iterrows():
            tk.Label(top_bottom_window, text=f"{row['City']}: {row['Violent Crime Rate']:.2f} per 1,000 residents").pack()

    def plot_heatmap(self):
        correlations = self.data[["Violent Crime", "Property Crime", "Burglary", "Larceny-Theft", "Arson"]].corr()

        # Plot heatmap
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(correlations, annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Between Crime Categories")

        # Display chart in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

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
