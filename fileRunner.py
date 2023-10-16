import subprocess
import os
import sys
# Define the Flask app script file and the list of ports
app_script = 'app.py'

# Function to run a Flask app on a specified port
def run_app_on_port(port):
    env = os.environ.copy()
    env['FLASK_APP'] = app_script
    env['FLASK_ENV'] = 'development'  # Change to 'production' for production mode

    subprocess.Popen(['flask', 'run', '--port', str(port)], env=env)

def main(port):
    i=0
    port = int(port)
    ports=[]
    while i<=10:
        k = port+i
        ports.append(k)
        run_app_on_port(k)
        i+=1

    print(f"Started the app on ports: {', '.join(map(str, ports))}")
if __name__=='__main__':
    port = sys.argv[1]
    main(port)
