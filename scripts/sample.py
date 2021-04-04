import pandas as pd
import sweetviz as sv

def main():
    # On charge les données
    df = pd.read_csv('../data/MOCK_DATA.csv')

    # On analyse les données
    r = sv.analyze(df)

    # On affiche le rapport
    r.show_html('../out/myReport.html')

    # On compare les 500 premières lignes avec les 500 dernières
    df1 = sv.compare(df[500:], df[:500])
    df1.show_html('../out/comparaison.html')

if __name__ == "__main__":
    main()