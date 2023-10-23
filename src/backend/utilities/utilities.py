import subprocess

def isHostReachable(host):
    try:
        subprocess.check_output(["ping", "-c", "1", "-w", "5", host])
        print(f"{host} is reachable.")
        return True
    except subprocess.CalledProcessError:
        print(f"{host} is not reachable.")
        return False