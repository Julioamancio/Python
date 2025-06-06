from challenges_iniciantes import CHALLENGES_INICIANTES
from challenges_intermediarios import CHALLENGES_INTERMEDIARIOS
from challenges_avancados import CHALLENGES_AVANCADOS

# Dicionário central de desafios por nível
CHALLENGES = {
    "Iniciante": CHALLENGES_INICIANTES,
    "Intermediário": CHALLENGES_INTERMEDIARIOS,
    "Avançado": CHALLENGES_AVANCADOS
}

def get_topics_by_level(level):
    """Retorna os tópicos disponíveis para um determinado nível."""
    desafios = CHALLENGES.get(level)
    if not desafios:
        # Aceita também nome sem acento para compatibilidade
        level_alt = level.replace('í', 'i').replace('á', 'a').replace('â', 'a').replace('ã', 'a')
        desafios = CHALLENGES.get(level_alt)
    if not desafios:
        return []
    return sorted(list(set([c.get("topic", "") for c in desafios])))

def get_challenges_filtered(level, topic, exclude_ids=None):
    """Filtra desafios por nível, tópico e ids a excluir (já feitos pelo aluno)."""
    exclude_ids = exclude_ids or []
    desafios = CHALLENGES.get(level)
    if not desafios:
        # Compatibilidade sem acento
        level_alt = level.replace('í', 'i').replace('á', 'a').replace('â', 'a').replace('ã', 'a')
        desafios = CHALLENGES.get(level_alt, [])
    return [c for c in desafios if c.get("topic") == topic and c.get("id") not in exclude_ids]

def get_challenge_by_id(ch_id):
    """Busca um desafio por ID em todos os níveis."""
    for desafios in CHALLENGES.values():
        for c in desafios:
            if c.get("id") == ch_id:
                return c
    return None

def get_points(challenge):
    """Retorna a pontuação de um desafio, padrão 1."""
    return challenge.get("points", 1)

def get_challenges_by_topic(topic):
    """
    Retorna todos os desafios (de todos os níveis) para um dado tópico (assunto).
    Útil para relatórios e envio de e-mail ao concluir um assunto.
    """
    results = []
    for group in CHALLENGES.values():
        for ch in group:
            if ch.get("topic") == topic:
                results.append(ch)
    return results