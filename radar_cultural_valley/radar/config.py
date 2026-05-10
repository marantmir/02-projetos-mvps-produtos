from dataclasses import dataclass


@dataclass(frozen=True)
class ProductConfig:
    app_name: str = "Radar Cultural AI"
    app_subtitle: str = "Inteligência cultural para transformar dados em conteúdo de alta performance"
    default_country: str = "Brasil"
    min_rows_for_model: int = 8


@dataclass(frozen=True)
class ScoreWeights:
    # A soma deve ser 1.0 para manter explicabilidade.
    popularity: float = 0.25
    engagement: float = 0.25
    trend_signal: float = 0.20
    social_volume: float = 0.15
    novelty: float = 0.10
    strategic_fit: float = 0.05

    def as_dict(self) -> dict:
        return {
            "popularidade": self.popularity,
            "engajamento": self.engagement,
            "sinal_tendencia": self.trend_signal,
            "volume_social": self.social_volume,
            "novidade": self.novelty,
            "aderencia_estrategica": self.strategic_fit,
        }
