import pandas as pd


def load_demo_sources() -> dict[str, pd.DataFrame]:
    """Dados simulados para permitir demonstração sem APIs reais."""
    spotify = pd.DataFrame({
        "nome": ["Funk futurista", "Trap melódico", "Sertanejo universitário", "Afrobeats BR", "Lo-fi estudo", "Gospel pop", "Pagode romântico", "Phonk treino"],
        "artista": ["Artista A", "Artista B", "Artista C", "Artista D", "Artista E", "Artista F", "Artista G", "Artista H"],
        "popularidade": [88, 82, 91, 73, 65, 77, 84, 70],
        "genero": ["funk", "trap", "sertanejo", "afrobeats", "lofi", "gospel", "pagode", "phonk"],
    })

    youtube = pd.DataFrame({
        "titulo": ["Como usar IA para criar música", "Bastidores de show", "Treino com phonk", "Rotina de estudo lo-fi", "Trend de dança", "Histórias de superação", "Review de clipe", "Desafio musical"],
        "canal": ["Canal 1", "Canal 2", "Canal 3", "Canal 4", "Canal 5", "Canal 6", "Canal 7", "Canal 8"],
        "visualizacoes": [320000, 180000, 410000, 95000, 520000, 210000, 165000, 260000],
        "likes": [18000, 9000, 26000, 5000, 41000, 15000, 8000, 17000],
        "tema": ["ia musica", "bastidores", "phonk treino", "lofi estudo", "trend dança", "superação", "review clipe", "desafio musical"],
    })

    trends = pd.DataFrame({
        "termo": ["ia na música", "trend dança", "phonk treino", "afrobeats brasil", "lofi estudo", "funk futurista", "gospel pop", "pagode romântico"],
        "interesse": [91, 95, 89, 74, 63, 78, 70, 82],
        "crescimento_pct": [34, 41, 28, 22, 9, 31, 12, 19],
    })

    x = pd.DataFrame({
        "assunto": ["ia na música", "trend dança", "phonk treino", "funk futurista", "pagode romântico", "afrobeats brasil", "gospel pop", "lofi estudo"],
        "volume": [12500, 22100, 18400, 9100, 7600, 6900, 5400, 4300],
        "sentimento": [0.62, 0.70, 0.55, 0.61, 0.68, 0.59, 0.72, 0.50],
        "created_at": pd.date_range("2026-05-01", periods=8, freq="D"),
    })

    return {"spotify": spotify, "youtube": youtube, "trends": trends, "x": x}
