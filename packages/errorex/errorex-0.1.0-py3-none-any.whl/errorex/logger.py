# errorex/logger.py

import os
from datetime import datetime
from errorex.formatter import format_markdown

def log_to_markdown(error_info: dict, directory="logs"):
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{directory}/error_report_{timestamp}.md"
    error_info["timestamp"] = timestamp  # Attach timestamp to info

    content = format_markdown(error_info)

    with open(filename, "w") as f:
        f.write(content)

    print(f"\n[green]📝 Error report saved to:[/green] {filename}")
