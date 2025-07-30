from rich.console import Console
from rich.panel import Panel

def show_banner():
    console = Console()
    banner = """[bold red]


 _    ________   _____ _________    _   __
| |  / /_  __/  / ___// ____/   |  / | / /
| | / / / /_____\__ \/ /   / /| | /  |/ / 
| |/ / / /_____/__/ / /___/ ___ |/ /|  /  
|___/ /_/     /____/\____/_/  |_/_/ |_/   
                                          



[/bold red]"""
    console.print(Panel(banner, subtitle="Created by Bismoy Ghosh", style="bold green"))
