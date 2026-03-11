from src.analyzer.match_analyzer import MatchAnalyzer

def main():

    analyzer = MatchAnalyzer()

    print("Iniciando análisis de partidos...")

    analyzer.analyze_all_matches()

    print("Análisis completado")


if __name__ == "__main__":
    main()