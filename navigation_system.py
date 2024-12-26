import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import folium
import webbrowser

def compute_jacobian(joint_angles):
    """Compute the Jacobian matrix and end-effector position."""
    x1 = np.cos(joint_angles[0])
    y1 = np.sin(joint_angles[0])
    x2 = x1 + np.cos(joint_angles[0] + joint_angles[1])
    y2 = y1 + np.sin(joint_angles[0] + joint_angles[1])
    
    J = np.array([[-np.sin(joint_angles[0]), -np.sin(joint_angles[0] + joint_angles[1])],
                  [np.cos(joint_angles[0]), np.cos(joint_angles[0] + joint_angles[1])]])
    
    return J, np.array([x2, y2])

def get_current_location():
    """Simulate getting the current GPS location."""
    return (34.0522, -118.2437)  # Example: Los Angeles coordinates

def validate_input(angle1, angle2, target_lat, target_lon):
    """Validate joint angles and GPS coordinates."""
    if not (-180 <= angle1 <= 180) or not (-180 <= angle2 <= 180):
        raise ValueError("Joint angles must be between -180 and 180 degrees.")
    if not (-90 <= target_lat <= 90) or not (-180 <= target_lon <= 180):
        raise ValueError("GPS coordinates are out of bounds.")

def display_results(current_location, target_location, distance, J, end_effector_position):
    """Display results in a message box."""
    result_text = (
        "Current Position: {}\n"
        "Target Position: {}\n"
        "Distance: {:.2f} meters\n"
        "Jacobian Matrix:\n{}\n"
        "End Effector Position: {}".format(
            current_location,
            target_location,
            distance,
            J,
            end_effector_position
        )
    )
    messagebox.showinfo("Navigation Results", result_text)

def navigate_to_target():
    """Handle navigation and display results."""
    try:
        angle1 = float(entry_angle1.get())
        angle2 = float(entry_angle2.get())
        target_lat = float(entry_lat.get())
        target_lon = float(entry_lon.get())
        
        # Validate inputs
        validate_input(angle1, angle2, target_lat, target_lon)

        target_location = (target_lat, target_lon)
        joint_angles = [np.radians(angle1), np.radians(angle2)]
        J, end_effector_position = compute_jacobian(joint_angles)
        
        current_location = get_current_location()
        distance = geodesic(current_location, target_location).meters
        
        display_results(current_location, target_location, distance, J, end_effector_position)

        plot_navigation_path([current_location, target_location])
        show_map(current_location, target_location)

    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))

def plot_navigation_path(path):
    """Plot the navigation path using Matplotlib."""
    latitudes, longitudes = zip(*path)
    plt.figure()
    plt.plot(longitudes, latitudes, marker='o', color='b', label='Path')
    plt.title('Navigation Path')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid()
    plt.legend()
    plt.axis('equal')
    plt.show()

def show_map(current_location, target_location):
    """Create and display a map with the current and target locations."""
    map_center = [(current_location[0] + target_location[0]) / 2, (current_location[1] + target_location[1]) / 2]
    folium_map = folium.Map(location=map_center, zoom_start=13)

    folium.Marker(location=current_location, popup='Current Location', icon=folium.Icon(color='blue')).add_to(folium_map)
    folium.Marker(location=target_location, popup='Target Location', icon= folium.Icon(color='red')).add_to(folium_map)

    folium_map.save("navigation_map.html")

    webbrowser.open("navigation_map.html")

def create_background_image():
    """Create a Tkinter label with a background image."""
    img = Image.open("back.jpg")  # Ensure you have a background image file
    img = img.resize((800, 600), Image.LANCZOS)  # Resize to fit your GUI
    background_image = ImageTk.PhotoImage(img)
    
    background_label = tk.Label(app, image=background_image)
    background_label.image = background_image  # Keep a reference to avoid garbage collection
    background_label.place(x=0, y=0, relwidth=1, relheight=1)


def display_logo():
    """Display the logo at the top of the window."""
    logo = Image.open("ki.png")  # Replace with your logo file path
    logo = logo.resize((200, 100), Image.LANCZOS)  # Resize logo to fit the GUI
    logo_image = ImageTk.PhotoImage(logo)
    
    logo_label = tk.Label(app, image=logo_image)
    logo_label.image = logo_image  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=10)  # Add some space around the logo

def fill_example_values():
    """Fill the input fields with example values."""
    entry_angle1.delete(0, tk.END)
    entry_angle1.insert(0, "45")  # Example joint angle 1

    entry_angle2.delete(0, tk.END)
    entry_angle2.insert(0, "30")  # Example joint angle 2

    entry_lat.delete(0, tk.END)
    entry_lat.insert(0, "18.054431")  # Example latitude (Los Angeles)

    entry_lon.delete(0, tk.END)
    entry_lon.insert(0, "79.537703")  # Example longitude (Los Angeles)

app = tk.Tk()
app.title("Navigation System")
app.geometry("800x600") 
app.resizable(False, False)
display_logo()
create_background_image()
tk.Label(app, text="Current Location is Los Angeles(Default)").pack()
tk.Label(app, text="Joint Angle 1 (degrees):").pack()
entry_angle1 = tk.Entry(app)
entry_angle1.pack()

tk.Label(app, text="Joint Angle 2 (degrees):").pack()
entry_angle2 = tk.Entry(app)
entry_angle2.pack()

tk.Label(app, text="Target Latitude:").pack()
entry_lat = tk.Entry(app)
entry_lat.pack()

tk.Label(app, text="Target Longitude:").pack()
entry_lon = tk.Entry(app)
entry_lon.pack()
btn_navigate = tk.Button(app, text="Navigate", command=navigate_to_target)
btn_navigate.pack()
btn_example = tk.Button(app, text="Fill Kitsw Ece block location Values", command=fill_example_values)
btn_example.pack()
app.mainloop()