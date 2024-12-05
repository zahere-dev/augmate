from termcolor import colored

def log_message(message: str, level: str):
    if level == 'REASON':
        # Print informational message in blue
        print(colored('REASON: ' + message, 'blue'))
    elif level == 'ACTION':
        # Print warning message in yellow
        print(colored('ACTION: ' + message, 'yellow'))
    elif level == 'error':
        # Print error message in red
        print(colored('ERROR: ' + message, 'red'))
    elif level == 'RESPONSE':
        # Print success message in green
        print(colored('RESPONSE: ' + message, 'green'))