# ============================================
# MÓDULO 1: CÁLCULOS FÍSICOS DEL MONTACARGAS
# ============================================

GRAVEDAD = 9.81  # Constante gravitacional m/s²

def calcular_peso(masa_kg):
    """Calcula el peso de la carga en Newtons."""
    if masa_kg <= 0:
        raise ValueError("La masa debe ser mayor a 0.")
    return round(masa_kg * GRAVEDAD, 2)


def calcular_factor_seguridad(carga_real, carga_maxima):
    """Calcula el factor de seguridad del montacargas."""
    if carga_real <= 0:
        raise ValueError("La carga real debe ser mayor a 0.")
    return round(carga_maxima / carga_real, 2)


def estado_carga(factor_seguridad):
    """Retorna el estado de la carga según el factor de seguridad."""
    if factor_seguridad >= 2.0:
        return "✅ SEGURO"
    elif factor_seguridad >= 1.5:
        return "⚠️ PRECAUCIÓN"
    else:
        return "🚨 PELIGROSO"


def calcular_torque(masa_kg, distancia_m):
    """Calcula el torque en Newton·metro."""
    if masa_kg <= 0 or distancia_m <= 0:
        raise ValueError("La masa y distancia deben ser mayores a 0.")
    peso = calcular_peso(masa_kg)
    return round(peso * distancia_m, 2)


def calcular_potencia(masa_kg, altura_m, tiempo_s):
    """Calcula la potencia necesaria en Watts."""
    if tiempo_s <= 0:
        raise ValueError("El tiempo debe ser mayor a 0.")
    if masa_kg <= 0 or altura_m <= 0:
        raise ValueError("La masa y altura deben ser mayores a 0.")
    return round((masa_kg * GRAVEDAD * altura_m) / tiempo_s, 2)


def watts_a_hp(watts):
    """Convierte Watts a Caballos de Fuerza (HP)."""
    return round(watts / 745.7, 4)


def verificar_estabilidad(peso_carga, peso_contrapeso, dist_carga, dist_contrapeso):
    """Verifica si el montacargas es estable comparando momentos."""
    momento_volcador = round(peso_carga * dist_carga, 2)
    momento_estabilizador = round(peso_contrapeso * dist_contrapeso, 2)
    estable = momento_estabilizador >= momento_volcador
    return {
        "momento_volcador": momento_volcador,
        "momento_estabilizador": momento_estabilizador,
        "estable": estable,
        "estado": "✅ ESTABLE" if estable else "🚨 INESTABLE"
    }


def resumen_calculo(masa_kg, carga_maxima, distancia_m, altura_m, tiempo_s, peso_contrapeso, dist_contrapeso):
    """Genera un resumen completo de todos los cálculos del montacargas."""
    peso = calcular_peso(masa_kg)
    fs = calcular_factor_seguridad(masa_kg, carga_maxima)
    estado = estado_carga(fs)
    torque = calcular_torque(masa_kg, distancia_m)
    potencia_w = calcular_potencia(masa_kg, altura_m, tiempo_s)
    potencia_hp = watts_a_hp(potencia_w)
    estabilidad = verificar_estabilidad(peso, peso_contrapeso, distancia_m, dist_contrapeso)

    return {
        "masa_kg": masa_kg,
        "peso_N": peso,
        "factor_seguridad": fs,
        "estado_carga": estado,
        "torque_Nm": torque,
        "potencia_W": potencia_w,
        "potencia_HP": potencia_hp,
        "estabilidad": estabilidad["estado"],
        "momento_volcador": estabilidad["momento_volcador"],
        "momento_estabilizador": estabilidad["momento_estabilizador"]
    }