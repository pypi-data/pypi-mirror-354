import os
import tkinter as tk
from tkinter import ttk, messagebox

from .audio_recorder import AudioRecorder
from . import config

# --- Configuration Constants ---
INITIAL_WINDOW_GEOMETRY = config.INITIAL_WINDOW_GEOMETRY
RECORDING_WINDOW_GEOMETRY = config.RECORDING_WINDOW_GEOMETRY
IS_RESIZEABLE = config.RESIZABLE_WINDOW

class DubberUI:
    """Manages the Tkinter user interface."""
    def __init__(self, master, audio_recorder: AudioRecorder):
        self.master = master
        master.title("Dubber Device Selection & Recording")
        master.geometry(INITIAL_WINDOW_GEOMETRY)
        master.resizable(IS_RESIZEABLE, IS_RESIZEABLE) # Prevent resizing

        self.audio_recorder = audio_recorder

        # --- UI State Variables ---
        self.dropdown_var = tk.StringVar(master)

        # --- Page 1: Device Selection Frame ---
        self.page1_frame = ttk.Frame(master)
        self.create_page1_widgets()

        # --- Page 2: Recording Controls Frame ---
        self.page2_frame = ttk.Frame(master)
        self.create_page2_widgets()

        # Initial setup: Show page 1
        self.show_page1()

        # Set default device if available
        self.update_device_dropdown()
        if self.audio_recorder.get_input_devices():
            self.on_dropdown_select(None) # Select the first device by default

    def create_page1_widgets(self):
        """Creates widgets for the device selection page."""
        ttk.Label(self.page1_frame, text="Select a recording device:").pack(pady=10)

        self.device_dropdown = ttk.Combobox(
            self.page1_frame,
            textvariable=self.dropdown_var,
            state="readonly" # Prevent user from typing
        )
        self.device_dropdown.pack(pady=5)
        self.device_dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_select)

        button_frame = ttk.Frame(self.page1_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Cancel", command=self.on_cancel_click).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Next", command=self.on_next_click).pack(side=tk.RIGHT, padx=5)

    def create_page2_widgets(self):
        """Creates widgets for the recording controls page."""
        self.selected_device_label = ttk.Label(self.page2_frame, text="")
        self.selected_device_label.pack(pady=10)

        self.record_status_label = ttk.Label(self.page2_frame, text="Ready to record.", foreground="blue")
        self.record_status_label.pack(pady=5)

        self.start_button = ttk.Button(self.page2_frame, text="Start Recording", command=self.on_start_recording_click)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.page2_frame, text="Stop Recording", command=self.on_stop_recording_click, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        ttk.Button(self.page2_frame, text="Back", command=self.on_back_click).pack(side=tk.LEFT, padx=10, pady=20)


    def update_device_dropdown(self):
        """Populates the dropdown with available audio input devices."""
        input_devices = self.audio_recorder.get_input_devices()
        device_names = [dev['name'] for dev in input_devices]

        if not device_names:
            messagebox.showerror("Error", "No audio input devices found!")
            self.device_dropdown.config(values=[], state="disabled")
            self.dropdown_var.set("No devices found")
            return

        self.device_dropdown.config(values=device_names)
        self.dropdown_var.set(device_names[0]) # Set default selection
        self.audio_recorder.set_device(input_devices[0]['id']) # Set default device ID

    def show_page1(self):
        """Displays the device selection page."""
        self.page2_frame.pack_forget()
        self.page1_frame.pack(fill="both", expand=True)
        self.master.geometry(INITIAL_WINDOW_GEOMETRY)
        self.record_status_label.config(text="Ready to record.", foreground="blue") # Reset status

    def show_page2(self):
        """Displays the recording controls page."""
        self.page1_frame.pack_forget()
        self.page2_frame.pack(fill="both", expand=True)
        self.master.geometry(RECORDING_WINDOW_GEOMETRY) # Adjust size for page 2

    # --- Event Handlers ---

    def on_dropdown_select(self, event):
        """Handles selection from the device dropdown."""
        selected_name = self.dropdown_var.get()
        input_devices = self.audio_recorder.get_input_devices()
        selected_device = next((dev for dev in input_devices if dev['name'] == selected_name), None)

        if selected_device:
            self.audio_recorder.set_device(selected_device['id'])
            print(f"Selected device: {selected_name} (ID: {selected_device['id']})")
        else:
            messagebox.showwarning("Warning", "Selected device not found. Please refresh or check connections.")
            self.audio_recorder.set_device(None) # Unset device

    def on_next_click(self):
        """Handles 'Next' button click to transition to the recording page."""
        if self.audio_recorder._selected_device_id is None:
            messagebox.showwarning("Warning", "Please select an audio device first.")
            return

        selected_name = self.dropdown_var.get()
        self.selected_device_label.config(text=f"Selected Device: {selected_name}")
        self.show_page2()

    def on_cancel_click(self):
        """Handles 'Cancel' button click to exit the application."""
        if self.audio_recorder.is_recording:
            # Ask for confirmation if recording is active
            if not messagebox.askyesno("Confirm Exit", "A recording is in progress. Do you want to stop and exit?"):
                return
            self.audio_recorder.stop_recording() # Stop recording before exiting

        print("Cancel button clicked! Exiting.")
        self.master.destroy()

    def on_back_click(self):
        """Handles 'Back' button click to return to the device selection page."""
        if self.audio_recorder.is_recording:
            messagebox.showwarning("Warning", "Stop recording before going back.")
            return
        self.show_page1()

    def on_start_recording_click(self):
        """Handles 'Start Recording' button click."""
        if self.audio_recorder.start_recording(on_error_callback=self._update_ui_with_error):
            self.record_status_label.config(text="Recording...", foreground="red")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            print("UI: Recording started.")
        else:
            print("UI: Failed to start recording.")

    def on_stop_recording_click(self):
        """Handles 'Stop Recording' button click."""
        if self.audio_recorder.stop_recording(
            save_callback=self._update_ui_after_save,
            on_error_callback=self._update_ui_with_error
        ):
            print("UI: Recording stopped.")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.record_status_label.config(text="Processing recording...", foreground="orange")
        else:
            print("UI: Failed to stop recording or no data to save.")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.record_status_label.config(text="Ready to record.", foreground="blue")


    # --- Callbacks from AudioRecorder (executed on main thread) ---

    def _update_ui_with_error(self, message):
        """Updates UI with an error message from the audio thread."""
        self.master.after(0, lambda: messagebox.showerror("Recording Error", message))
        self.master.after(0, lambda: self.record_status_label.config(text=f"Error: {message}", foreground="red"))
        self.master.after(0, lambda: self.start_button.config(state=tk.NORMAL))
        self.master.after(0, lambda: self.stop_button.config(state=tk.DISABLED))


    def _update_ui_after_save(self, filename):
        """Updates UI after audio recording is saved (or not saved)."""
        if filename:
            self.master.after(0, lambda: self.record_status_label.config(text=f"Saved to: {os.path.basename(filename)}", foreground="green"))
        else:
            self.master.after(0, lambda: self.record_status_label.config(text="No audio recorded or failed to save.", foreground="red"))
        self.master.after(0, lambda: self.start_button.config(state=tk.NORMAL))
        self.master.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
