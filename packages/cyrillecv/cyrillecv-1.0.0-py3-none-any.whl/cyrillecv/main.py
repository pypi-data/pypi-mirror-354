# cyrillecv/main.py

import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def afficher_cv():
    console.print(Panel.fit("[bold green]🚀 Installation de Cyrille Gbale...[/bold green]"))
    time.sleep(1)
    console.print("📦 Téléchargement du profil...")
    time.sleep(1)
    console.print("✅ Dépendances : [cyan]Data Analysis, Data Engineering, BI, SQL, Python[/cyan]")
    time.sleep(1)

    console.print("\n[bold underline]🎓 FORMATIONS[/bold underline]")
    console.print("- Mastère Big Data – Sup De Vinci (2023–2024)")
    console.print("- Certificat Data Engineer – IBM via Coursera (2023–2024)")
    console.print("- Certificat RNCP Data Analyst – Wild Code School (2023)")
    console.print("- Master Économie – Université Moulay Ismail, Maroc (2010–2012)")

    console.print("\n[bold underline]💼 EXPÉRIENCES CLÉS[/bold underline]")
    console.print("- Data Engineer – Tibco Telecom (Dépuis 2024)")
    console.print("- Data Analyst – Terrena Groupe (2023–2024)")
    console.print("- Analyst Risque – Crédit Agricole, BPI, BNP Paribas (2019–2022)")
    console.print("- Responsable Agence – Atlantic Microfinance (2015–2018)")

    console.print("\n[bold underline]🧠 COMPÉTENCES[/bold underline]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Domaine", width=20)
    table.add_column("Compétences")

    table.add_row("Analyse de données", "Pandas, Python, Power BI")
    table.add_row("ETL / BDD", "Airflow, SQL Server SSIS, PostgreSQL")
    table.add_row("Outils", "Jira, Confluence, GLPI")
    table.add_row("Big Data", "Spark, Kafka")
    table.add_row("Langues", "Français (natif), Anglais (universitaire)")
    console.print(table)

    console.print("\n[bold underline]📫 CONTACT[/bold underline]")
    console.print("- Email : crvgbale@gmail.com")
    console.print("- Téléphone : 07 73 75 54 79")
    console.print("- Localisation : Le Gâvre, 44130")

    console.print("\n🎸 Centres d’intérêt : Arbitre de foot, Bricolage, Guitare acoustique")
    console.print("\n[bold green]CV installé avec succès ![/bold green]")

def main():
    afficher_cv()
