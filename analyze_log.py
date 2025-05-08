import sys
from collections import Counter

def analyze_log_file(log_file_path):
  """
  Reads an access log file, counts unique User Agents, and provides request statistics.

  Args:
    log_file_path: The path to the access log file.

  Returns:
    A tuple containing:
      - The total number of unique User Agents.
      - A Counter object with User Agents as keys and their request counts as values.
  """
  user_agents = []
  try:
    with open(log_file_path, 'r') as log_file:
      for line in log_file:
        # Assuming the User Agent string is typically found within double quotes
        # and often after some common fields like IP, timestamp, request.
        # This is a simplified approach and might need adjustments based on
        # the specific format of your access log file.
        parts = line.split('"')
        if len(parts) > 5:  # Heuristic to find a line likely containing User Agent
          user_agent = parts[5].strip()
          if user_agent:
            user_agents.append(user_agent)
  except FileNotFoundError:
    print(f"Error: Log file not found at '{log_file_path}'")
    sys.exit(1)
  except Exception as e:
    print(f"An error occurred while reading the log file: {e}")
    sys.exit(1)

  user_agent_counts = Counter(user_agents)
  total_unique_agents = len(user_agent_counts)

  return total_unique_agents, user_agent_counts

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: analyze_log.py <log_file_path>")
    sys.exit(1)

  log_file = sys.argv[1]
  total_unique, agent_stats = analyze_log_file(log_file)

  print(f"Total number of unique User Agents: {total_unique}\n")
  print("Request statistics per User Agent:")
  for agent, count in agent_stats.items():
    print(f"- {agent}: {count}")