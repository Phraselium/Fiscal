"""Validaciones de identificadores y códigos usados en los ficheros tributarios."""

from __future__ import annotations

import re

LETRAS_NIF = "TRWAGMYFPDXBNJZSQVHLCKE"
LETRAS_CIF = "JABCDEFGHI"
CIF_LETRA_OBLIGATORIA = set("KPQRSNW")
CIF_NUMERO_OBLIGATORIO = set("ABEH")

# Prefijos de NIF-IVA de los Estados miembros de la UE (Irlanda del Norte: XI).
PREFIJOS_NIF_IVA = {
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR",
    "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT", "NL", "PL", "PT", "RO",
    "SE", "SI", "SK", "XI",
}


def limpiar(valor: str) -> str:
    return re.sub(r"[^0-9A-Za-z]", "", str(valor or "")).upper()


def validar_nif(valor: str) -> tuple[bool, str]:
    """Valida NIF de persona física, NIE y CIF. Devuelve (válido, motivo)."""
    nif = limpiar(valor)
    if len(nif) != 9:
        return False, f"'{valor}' no tiene 9 caracteres"

    # NIE: X/Y/Z + 7 dígitos + letra
    if nif[0] in "XYZ":
        numero = str("XYZ".index(nif[0])) + nif[1:8]
        if not numero.isdigit() or not nif[8].isalpha():
            return False, "formato de NIE incorrecto"
        esperada = LETRAS_NIF[int(numero) % 23]
        if nif[8] != esperada:
            return False, f"letra de control incorrecta (esperada {esperada})"
        return True, "NIE válido"

    # NIF persona física: 8 dígitos + letra
    if nif[:8].isdigit() and nif[8].isalpha():
        esperada = LETRAS_NIF[int(nif[:8]) % 23]
        if nif[8] != esperada:
            return False, f"letra de control incorrecta (esperada {esperada})"
        return True, "NIF válido"

    # CIF: letra + 7 dígitos + dígito o letra de control
    if nif[0].isalpha() and nif[1:8].isdigit():
        digitos = nif[1:8]
        suma_pares = sum(int(d) for d in digitos[1::2])
        suma_impares = 0
        for d in digitos[0::2]:
            doble = int(d) * 2
            suma_impares += doble // 10 + doble % 10
        control = (10 - (suma_pares + suma_impares) % 10) % 10
        candidatos = set()
        if nif[0] not in CIF_LETRA_OBLIGATORIA:
            candidatos.add(str(control))
        if nif[0] not in CIF_NUMERO_OBLIGATORIO:
            candidatos.add(LETRAS_CIF[control])
        if nif[8] not in candidatos:
            return False, f"dígito de control incorrecto (esperado {sorted(candidatos)})"
        return True, "CIF válido"

    return False, f"'{valor}' no responde a ningún formato de NIF, NIE o CIF"


def validar_nif_iva(valor: str) -> tuple[bool, str]:
    """Comprobación sintáctica del NIF-IVA intracomunitario.

    No sustituye a la consulta en VIES, que es la única prueba admitida para
    aplicar la exención del art. 25 LIVA. Consúltalo y guarda el justificante.
    """
    codigo = limpiar(valor)
    if len(codigo) < 4:
        return False, f"'{valor}' es demasiado corto para ser un NIF-IVA"
    prefijo, resto = codigo[:2], codigo[2:]
    if prefijo not in PREFIJOS_NIF_IVA:
        return False, f"prefijo de país '{prefijo}' no pertenece a la UE"
    if not resto.isalnum():
        return False, "el cuerpo del NIF-IVA contiene caracteres no admitidos"
    if prefijo == "ES":
        valido, motivo = validar_nif(resto)
        if not valido:
            return False, f"NIF español incorrecto: {motivo}"
    return True, f"sintaxis correcta ({prefijo}) — pendiente de comprobar en VIES"


def validar_iban(valor: str) -> tuple[bool, str]:
    iban = limpiar(valor)
    if len(iban) < 15 or len(iban) > 34:
        return False, "longitud de IBAN fuera de rango"
    reordenado = iban[4:] + iban[:4]
    numerico = "".join(str(int(c, 36)) for c in reordenado)
    if int(numerico) % 97 != 1:
        return False, "dígitos de control de IBAN incorrectos"
    return True, "IBAN válido"


def validar_codigo_nc8(valor: str) -> tuple[bool, str]:
    """Código de la Nomenclatura Combinada usado en Intrastat: 8 dígitos."""
    codigo = re.sub(r"\D", "", str(valor or ""))
    if len(codigo) != 8:
        return False, f"el código NC debe tener 8 dígitos, tiene {len(codigo)}"
    return True, "formato correcto — contrastar con el arancel TARIC vigente"


def validar_referencia_catastral(valor: str) -> tuple[bool, str]:
    referencia = limpiar(valor)
    if len(referencia) not in (14, 20):
        return False, "la referencia catastral debe tener 14 o 20 caracteres"
    return True, "formato correcto"


if __name__ == "__main__":
    import sys

    for entrada in sys.argv[1:]:
        ok, motivo = validar_nif(entrada)
        print(f"{entrada}: {'OK' if ok else 'ERROR'} — {motivo}")
