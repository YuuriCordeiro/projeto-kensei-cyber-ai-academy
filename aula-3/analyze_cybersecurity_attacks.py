import argparse
import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CSV_PATH = SCRIPT_DIR / "cybersecurity_attacks.csv"
CLEANED_CSV_PATH = SCRIPT_DIR / "cybersecurity_attacks_cleaned.csv"


def load_data(path: Path) -> pd.DataFrame:
    """Carrega o CSV de ataques cibernéticos."""
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa o dataset removendo duplicados, convertendo datas e tratando valores inválidos."""
    initial_count = len(df)
    df = df.drop_duplicates().copy()

    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        median = df[col].median()
        df[col] = df[col].fillna(median if pd.notna(median) else 0)

    fill_values = {
        "Malware Indicators": "None",
        "Alerts/Warnings": "None",
        "Proxy Information": "None",
        "Firewall Logs": "None",
        "IDS/IPS Alerts": "None",
        "Payload Data": "None",
        "Attack Type": "Unknown",
        "Attack Signature": "Unknown",
        "Action Taken": "Unknown",
        "Severity Level": "Unknown",
        "Network Segment": "Unknown",
        "Log Source": "Unknown",
    }
    for col, value in fill_values.items():
        if col in df.columns:
            df[col] = df[col].fillna(value)

    for port_col in ["Source Port", "Destination Port"]:
        if port_col in df.columns:
            df.loc[~df[port_col].between(0, 65535), port_col] = pd.NA
            df[port_col] = df[port_col].fillna(0).astype(int)

    if "Packet Length" in df.columns:
        df.loc[df["Packet Length"] <= 0, "Packet Length"] = pd.NA
        df["Packet Length"] = df["Packet Length"].fillna(df["Packet Length"].median()).astype(int)

    required_columns = [col for col in ["Timestamp", "Source IP Address", "Destination IP Address", "Attack Type"] if col in df.columns]
    if required_columns:
        df = df.dropna(subset=required_columns)

    if "Timestamp" in df.columns:
        df = df[~df["Timestamp"].isna()]

    cleaned_count = len(df)
    print(f"Limpeza: {initial_count} -> {cleaned_count} linhas após remoção de duplicados e dados inválidos")
    return df


def show_head(df: pd.DataFrame, n: int = 5) -> None:
    print("=== PRIMEIRAS LINHAS ===")
    print(df.head(n).to_string(index=False))
    print()


def show_info(df: pd.DataFrame) -> None:
    print("=== INFO ===")
    df.info()
    print()


def show_statistics(df: pd.DataFrame) -> None:
    print("=== ESTATÍSTICAS ===")
    print(df.describe(include="all").transpose().to_string())
    print()


def save_cleaned_data(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)
    print(f"Dados limpos salvos em: {path.name}")


def main() -> None:
    df = load_data(CSV_PATH)
    df_clean = clean_data(df)
    save_cleaned_data(df_clean, CLEANED_CSV_PATH)
    show_head(df_clean)
    show_info(df_clean)
    show_statistics(df_clean)


if __name__ == "__main__":
    main()
