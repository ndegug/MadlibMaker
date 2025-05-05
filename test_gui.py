import PySimpleGUI as sg

def main_screen():
    layout = [
        [sg.Multiline(size=(60, 5), key='-TOP-', enable_events=True, autoscroll=True)],
        [sg.Button('noun')],
        [sg.Multiline(size=(60, 5), key='-BOTTOM-', disabled=True)],
        [sg.Button('Print')]
    ]

    window = sg.Window('Madlib Editor', layout, finalize=True)

    top_element = window['-TOP-']
    bottom_element = window['-BOTTOM-']
    top_widget = top_element.Widget  # Get underlying tkinter Text widget

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == '-TOP-':
            bottom_element.update(values['-TOP-'])

        elif event == 'noun':
            # Directly insert into the Text widget to preserve formatting
            top_widget.insert("insert", "/nou")
            # Force sync both fields
            new_text = top_widget.get("1.0", "end-1c")
            bottom_element.update(new_text)

        elif event == 'Print':
            madlib_text = top_widget.get("1.0", "end-1c")
            window.close()
            display_screen(madlib_text)
            break

    window.close()

def display_screen(madlib_text):
    layout = [
        [sg.Text("This is your madlib:")],
        [sg.Multiline(default_text=madlib_text, size=(60, 10), disabled=True)],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Madlib Output', layout)

    while True:
        event, _ = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break

    window.close()

if __name__ == "__main__":
    main_screen()