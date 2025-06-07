

import customtkinter as ctk
import tkinter as tk
import re
from tkinter import messagebox, ttk
import time

class inputclass:
    @staticmethod
    def create_input(parent, label_text, placeholder, row, column, colspan=1):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 14), text_color="black")
        label.grid(row=row, column=column, sticky="w", padx=20, pady=0.5)
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=250, height=30)
        entry.grid(row=row+1, column=column, columnspan=colspan, padx=20, pady=(5, 10))
        return entry

    def create_number_input(parent, label_text, placeholder, row, column):
        def validate_number(P):
            return P.isdigit() or P == ""

        vcmd = parent.register(validate_number)

        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 14), text_color="black")
        label.grid(row=row, column=column, sticky="w", padx=20, pady=(10, 2))

        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=250, height=35)
        entry.configure(validate="key", validatecommand=(vcmd, "%P"))
        entry.grid(row=row + 1, column=column, padx=20, pady=(0, 10))

        return entry

    def create_dropdown(parent, label_text, options, row, column,variable):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12), text_color="black")
        label.grid(row=row, column=column, sticky="w", padx=20, pady=(10, 2))

        dropdown = ctk.CTkOptionMenu(parent,variable=variable ,values=options, width=250, height=35)
        dropdown.grid(row=row + 1, column=column, padx=20, pady=(0, 10))

        return dropdown
    def create_dropdown(parent, label_text, options, row, column,variable):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12), text_color="black")
        label.grid(row=row, column=column, sticky="w", padx=20, pady=(10, 2))

        dropdown = ctk.CTkOptionMenu(parent,variable=variable ,values=options, width=250, height=35)
        dropdown.grid(row=row + 1, column=column, padx=20, pady=(0, 10))

        return dropdown

    def create_dropdown(parent, label_text, options, row, column, variable):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12), text_color="black")
        label.grid(row=row, column=column, sticky="w", padx=20, pady=(10, 2))

        dropdown = ctk.CTkOptionMenu(parent, variable=variable, values=options, width=250, height=35)
        dropdown.grid(row=row + 1, column=column, padx=20, pady=(0, 10))

        return dropdown

    @staticmethod
    def create_searchable_ttk_dropdown(parent, label_text, options, row, column, variable):
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=column, sticky="w", padx=20, pady=(10, 2))

        dropdown = ttk.Combobox(
            parent,
            textvariable=variable,
            values=options,
            state="normal",
            width=30
        )
        dropdown.grid(row=row + 1, column=column, padx=20, pady=(0, 10), sticky="ew")

        dropdown._original_options = options[:]
        dropdown._is_dropdown_open = False
        top_level_window = parent.winfo_toplevel()

        try:
            ttk.Style().configure("Combobox.TCombobox", fieldbackground="white")
            ttk.Style().map("Combobox.TCombobox",
                            fieldbackground=[('invalid', 'pink'), ('!invalid', 'white')])
            ttk.Style().configure("Combobox.Valid.TCombobox", fieldbackground="white")
        except tk.TclError:
            pass

        def get_current_focused_widget():
            try:
                focused_widget = top_level_window.focus_get()
                if focused_widget:
                    return f"Widget: {focused_widget._name} ({focused_widget.winfo_class()}), Path: {str(focused_widget)}"
                return "None"
            except Exception:
                return "Focus Error"

        def validate_and_filter(event=None):
            current_text = dropdown.get()
            lower_current_text = current_text.lower()
            original_options = dropdown._original_options

            filtered_list = [item for item in original_options if
                             lower_current_text in item.lower()] if lower_current_text else original_options
            dropdown["values"] = filtered_list

            is_exact_match = current_text in original_options
            is_partial_match = any(
                lower_current_text in item.lower() for item in original_options) if lower_current_text else False

            if is_exact_match or (not current_text and not event):
                dropdown.state(["!invalid"])
                dropdown.config(style="Combobox.TCombobox")
            elif is_partial_match:
                dropdown.state(["!invalid"])
                dropdown.config(style="Combobox.TCombobox")
            else:
                dropdown.state(["invalid"])
                dropdown.config(style="Combobox.TCombobox")

            # --- Optimized Logic to show/hide the dropdown menu ---
            # Event types: '4' for KeyRelease, '9' for FocusIn, '<<ComboboxSelected>>'
            is_key_release_event = (event and event.type == '4')
            is_combobox_selected_event = (event and event.type == '<<ComboboxSelected>>')

            # Condition to open the dropdown list:
            # 1. There are filtered items to show.
            # 2. Text is being typed OR it's a FocusIn event on an empty dropdown (handled by on_focus_in).
            should_open_dropdown_list = len(filtered_list) > 0 and (
                        len(current_text) > 0 or (event and event.type == '9' and not current_text))

            print(
                f"\n[{label_text}] validate_and_filter: Event Type={event.type if event else 'None'}, Text='{current_text}'")
            print(
                f"[{label_text}]   _is_dropdown_open: {dropdown._is_dropdown_open}, should_open_dropdown_list: {should_open_dropdown_list}")
            print(f"[{label_text}]   Current System Focus: {get_current_focused_widget()}")

            if should_open_dropdown_list:
                if not dropdown._is_dropdown_open:
                    print(f"[{label_text}]   ACTION: Opening dropdown via event_generate.")
                    dropdown.update_idletasks()
                    dropdown.event_generate('<Button-1>', x=dropdown.winfo_width() - 10, y=dropdown.winfo_height() // 2)
                    dropdown._is_dropdown_open = True
                    # Set focus back to the Combobox entry to ensure typing continues.
                    # Only do this if it's a KeyRelease and not after a selection or when just getting focus
                    # as on_focus_in will handle initial focus.
                    if is_key_release_event and not is_combobox_selected_event:
                        top_level_window.after(1, lambda: dropdown.focus_set())
                        print(f"[{label_text}]   After 1ms (KeyRelease): Focus set to dropdown.")
            else:  # Should not open / should close
                if dropdown._is_dropdown_open:
                    print(f"[{label_text}]   ACTION: Closing dropdown via event_generate.")
                    dropdown.event_generate('<Button-1>')  # Toggle to close
                    dropdown._is_dropdown_open = False

                # IMPORTANT: Aggressively transfer focus AWAY from the Combobox.
                # If an item was selected, or text is cleared, or if the dropdown just closed.
                # This is the most crucial part to stop focus hijacking.
                if is_combobox_selected_event or not current_text or (
                        not should_open_dropdown_list and dropdown._is_dropdown_open):
                    # Giving focus to the parent is safer than trying to predict where user wants to go.
                    # The user's next click will then properly take focus.
                    top_level_window.after(1, lambda: dropdown.master.focus_set())
                    print(
                        f"[{label_text}]   After 1ms (Selection/Clear/Close): Focus set to parent ({dropdown.master.winfo_class()}).")

        # Bind events
        # Pass the event object to validate_and_filter
        dropdown.bind("<KeyRelease>", validate_and_filter)
        dropdown.bind("<<ComboboxSelected>>", validate_and_filter)  # event object automatically passed

        # FocusOut is handled by _check_focus_and_close with a delay, which is generally good.
        dropdown.bind("<FocusOut>", lambda e: top_level_window.after(150, lambda: _check_focus_and_close(dropdown,
                                                                                                         top_level_window,
                                                                                                         validate_on_lost_focus=True)))

        # FocusIn should always ensure the dropdown is ready for input if it's not empty
        dropdown.bind("<FocusIn>", lambda e: on_focus_in(e, validate_and_filter))

        # --- Modified on_focus_in to pass validate_and_filter ---
        def on_focus_in(event, validate_func):
            print(f"\n[{label_text}] on_focus_in: Current Text='{dropdown.get()}'")
            print(f"[{label_text}]   _is_dropdown_open: {dropdown._is_dropdown_open}")
            print(f"[{label_text}]   Current System Focus: {get_current_focused_widget()}")

            if not dropdown.get():  # If field is empty when gaining focus
                dropdown["values"] = dropdown._original_options
                # No need to call validate_func here to open, let the logic below handle it more robustly.
                # Simply setting values is enough here for empty field.

            # Ensure dropdown is opened if not already, and there are options to show (or if it was previously invalid)
            # if not dropdown._is_dropdown_open and len(dropdown["values"]) > 0: # This was the old condition
            # New condition for opening on FocusIn:
            # 1. Not already open.
            # 2. Has options to show OR it was previously in an invalid state (user might want to correct it).
            should_open_on_focus_in = not dropdown._is_dropdown_open and (
                        len(dropdown["values"]) > 0 or "invalid" in dropdown.state())

            if should_open_on_focus_in:
                print(f"[{label_text}]   ACTION: Opening dropdown on FocusIn (if not already open).")
                dropdown.update_idletasks()
                dropdown.event_generate('<Button-1>', x=dropdown.winfo_width() - 10, y=dropdown.winfo_height() // 2)
                dropdown._is_dropdown_open = True
                # Always force focus back when the Combobox is brought into focus and opened.
                top_level_window.after(1, lambda: dropdown.focus_set())
                print(f"[{label_text}]   After 1ms (FocusIn): Focus set to dropdown.")
            else:
                print(f"[{label_text}]   No action on FocusIn (already open or no values).")

        # --- _check_focus_and_close remains largely the same ---
        def _check_focus_and_close(widget, root_window, validate_on_lost_focus=False):
            try:
                focused_widget = root_window.focus_get()
                focused_widget_path = str(focused_widget) if focused_widget else 'None'
            except Exception as e:
                focused_widget_path = f'FOCUS_ERROR_OR_LOST ({e})'

            widget_path = str(widget)

            print(
                f"\n[{label_text}] _check_focus_and_close (after 150ms): Current focused_widget='{focused_widget_path}'")
            print(f"[{label_text}]   Widget path='{widget_path}', _is_dropdown_open={widget._is_dropdown_open}")

            is_focus_truly_elsewhere = (
                    focused_widget_path != widget_path and
                    not focused_widget_path.startswith(widget_path + ".") and  # Not a child of the combobox
                    focused_widget_path != 'FOCUS_ERROR_OR_LOST' and
                    focused_widget_path != 'None'
            )

            if is_focus_truly_elsewhere or focused_widget_path == 'FOCUS_ERROR_OR_LOST':
                print(f"[{label_text}]   Focus truly elsewhere or error. Closing dropdown.")
                if widget._is_dropdown_open:
                    widget.event_generate('<Button-1>')
                    widget._is_dropdown_open = False

                if validate_on_lost_focus:
                    current_value = widget.get()
                    if current_value not in widget._original_options:
                        widget.state(["invalid"])
                        widget.config(style="Combobox.TCombobox")
                        print(f"[{label_text}]   Validation: Invalid value '{current_value}'.")
                    else:
                        widget.state(["!invalid"])
                        widget.config(style="Combobox.TCombobox")
                        print(f"[{label_text}]   Validation: Valid value '{current_value}'.")
            else:
                print(f"[{label_text}]   Focus is still on or within dropdown. Not closing.")

        # Initial validation state
        validate_and_filter()

        return dropdown
    @staticmethod
    def create_email_input(parent, label_text, placeholder, row, column, colspan=1):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 14), text_color="black")
        label.grid(row=row, column=column, sticky="w", padx=20, pady=(10, 2))

        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=250, height=35)
        entry.grid(row=row + 1, column=column, columnspan=colspan, padx=20, pady=(0, 10))

        def validate_email(event=None):
            email = entry.get()
            if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showwarning("Invalid Email", "Please enter a valid email address.")

        # Run validation when user leaves the email field
        entry.bind("<FocusOut>", validate_email)

        return entry

    @staticmethod
    def create_password_input(parent, label_text, placeholder, row, column, colspan=1):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 14), text_color="black")
        label.grid(row=row, column=column, sticky="w", padx=20, pady=(10, 2))

        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, show="*", width=250, height=35)
        entry.grid(row=row + 1, column=column, columnspan=colspan, padx=20, pady=(0, 10))

        # Show/hide button
        def toggle_password():
            if entry.cget("show") == "*":
                entry.configure(show="")  # Show text
                toggle_btn.configure(text="Hide")
            else:
                entry.configure(show="*")  # Hide text
                toggle_btn.configure(text="Show")

        toggle_btn = ctk.CTkButton(parent, text="Show", width=60, height=30, command=toggle_password)
        toggle_btn.grid(row=row+1,column=1,sticky='w',padx=30, pady=(0, 10))  # Adjust as needed

        return entry