from __future__ import annotations

import pandas as pd


def generate_content_brief(row: pd.Series) -> dict:
    tema = row.get("conteudo", "tema cultural")
    prioridade = row.get("prioridade", "Testar")
    score = row.get("score_oportunidade", 0)
    origem = row.get("origem", "múltiplas fontes")

    return {
        "tema": tema,
        "decisao": f"{prioridade} — score {score:.1f}/100",
        "por_que_agora": f"O sinal aparece em {origem}, indicando oportunidade de transformar conversa cultural em conteúdo testável.",
        "gancho": f"O que {tema} revela sobre o comportamento das pessoas agora?",
        "formato_recomendado": "vídeo curto + carrossel explicativo + corte para Reels/TikTok/Shorts",
        "roteiro_30s": [
            "0-3s: abrir com uma pergunta ou afirmação provocativa.",
            "4-12s: mostrar o dado ou sinal cultural detectado.",
            "13-23s: explicar o motivo de isso importar para o público.",
            "24-30s: fechar com CTA para comentário, enquete ou compartilhamento.",
        ],
        "experimento": "Publicar 3 variações de gancho e medir retenção, CTR, comentários e compartilhamentos nas primeiras 24h.",
    }


def build_ai_prompt(row: pd.Series, brand_context: str = "") -> str:
    tema = row.get("conteudo", "")
    score = row.get("score_oportunidade", 0)
    origem = row.get("origem", "")
    return f"""
Você é um estrategista de conteúdo de classe mundial.
Crie um plano de conteúdo para o tema: {tema}.
Score de oportunidade: {score:.1f}/100.
Fontes de sinal: {origem}.
Contexto da marca: {brand_context or 'marca em crescimento que deseja autoridade, engajamento e conversão'}.
Entregue: 5 títulos, 5 ganchos, roteiro de 60 segundos, formato ideal, público-alvo, risco reputacional e métrica de sucesso.
""".strip()
