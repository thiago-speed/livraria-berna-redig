def validar_titulo(texto: str) -> str:
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("titulo invalido")
    return texto.strip()


def validar_autor(texto: str) -> str:
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("autor invalido")
    return texto.strip()


def validar_ano_publicacao(valor: int | str) -> int:
    try:
        ano = int(valor)
    except (TypeError, ValueError) as exc:
        raise ValueError("ano_publicacao invalido") from exc
    if ano < 0 or ano > 9999:
        raise ValueError("ano_publicacao invalido")
    return ano


def validar_preco(valor: float | str) -> float:
    try:
        preco = float(valor)
    except (TypeError, ValueError) as exc:
        raise ValueError("preco invalido") from exc
    if preco < 0:
        raise ValueError("preco invalido")
    return round(preco, 2)


