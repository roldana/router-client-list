import socket
import subprocess
import platform

def get_default_gateway():
    if platform.system() == "Linux":
        # Run the 'ip route' command to get the default gateway on Linux
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if 'default' in line:
                return line.split()[2]
    elif platform.system() == "Windows":
        # Run the 'ipconfig' command to get the default gateway on Windows
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if 'Default Gateway' in line:
                parts = line.split(':')
                if len(parts) > 1:
                    return parts[1].strip()
    return None

def is_router_ip(ip):
    try:
        # Try to create a socket connection to the IP address on port 80 (HTTP)
        socket.create_connection((ip, 80), timeout=2)
        return True
    except OSError:
        return False

def find_router_ip():
    gateway_ip = get_default_gateway()
    if gateway_ip and is_router_ip(gateway_ip):
        return gateway_ip
    return None

if __name__ == "__main__":
    router_ip = find_router_ip()
    if router_ip:
        print(f"Router IP address: {router_ip}")
    else:
        print("Router IP address not found.")
