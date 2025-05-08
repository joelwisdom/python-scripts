import platform
import psutil
import os
import socket
import netifaces as ni
import argparse

def get_distro_info():
  """Gets the operating system distribution information."""
  return platform.linux_distribution()

def get_memory_info():
  """Gets memory usage statistics."""
  mem = psutil.virtual_memory()
  return {
      "total": f"{mem.total / (1024 ** 3):.2f} GB",
      "used": f"{mem.used / (1024 ** 3):.2f} GB",
      "free": f"{mem.free / (1024 ** 3):.2f} GB",
  }

def get_cpu_info():
  """Gets CPU information."""
  return {
      "model": platform.processor(),
      "cores": psutil.cpu_count(logical=False),
      "threads": psutil.cpu_count(logical=True),
      "speed": f"{psutil.cpu_freq().current:.2f} MHz",
  }

def get_user_info():
  """Gets the current username."""
  return os.getlogin()

def get_load_average():
  """Gets the system load average."""
  if hasattr(os, 'getloadavg'):
    load1, load5, load15 = os.getloadavg()
    return f"{load1:.2f}, {load5:.2f}, {load15:.2f} (1, 5, 15 min)"
  else:
    return "Not available on this system"

def get_ip_address():
  """Gets the primary non-loopback IP address."""
  try:
    # Get a list of all network interfaces
    interfaces = ni.interfaces()
    for iface in interfaces:
      if iface != 'lo':  # Skip the loopback interface
        try:
          addresses = ni.ifaddresses(iface)
          if socket.AF_INET in addresses:
            # Get the first IPv4 address
            ip_info = addresses[socket.AF_INET][0]
            if 'addr' in ip_info:
              return ip_info['addr']
        except KeyError:
          pass  # Interface might not have IPv4
        except OSError:
          pass # Handle potential OS errors with interface details
    return "Could not determine IP address"
  except Exception as e:
    return f"Error getting IP address: {e}"

def main():
  """Main function to parse arguments and display system information."""
  parser = argparse.ArgumentParser(description="Get system information based on specified resources.")
  parser.add_argument('-d', '--distro', action='store_true', help='Show distribution info')
  parser.add_argument('-m', '--memory', action='store_true', help='Show memory information')
  parser.add_argument('-c', '--cpu', action='store_true', help='Show CPU information')
  parser.add_argument('-u', '--user', action='store_true', help='Show current user')
  parser.add_argument('-l', '--load', action='store_true', help='Show load average')
  parser.add_argument('-i', '--ip', action='store_true', help='Show IP address')
  args = parser.parse_args()

  if not any(vars(args).values()):
    print("No resource specified. Use -h for help.")
    return

  print("System Information:")
  if args.distro:
    distro = get_distro_info()
    print(f"  Distribution: {' '.join(distro)}")
  if args.memory:
    memory = get_memory_info()
    print(f"  Memory: Total={memory['total']}, Used={memory['used']}, Free={memory['free']}")
  if args.cpu:
    cpu = get_cpu_info()
    print(f"  CPU: Model={cpu['model']}, Cores={cpu['cores']}, Threads={cpu['threads']}, Speed={cpu['speed']}")
  if args.user:
    user = get_user_info()
    print(f"  Current User: {user}")
  if args.load:
    load = get_load_average()
    print(f"  Load Average: {load}")
  if args.ip:
    ip_address = get_ip_address()
    print(f"  IP Address: {ip_address}")

if __name__ == "__main__":
  main()