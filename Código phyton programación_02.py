from scipy.integrate import quad # type: ignore

# Diccionario con los coeficientes de Joback para cada grupo funcional
coeficientes_joback = {
    #Incremento sin anillo
    '-CH3': (19.5, -0.00808, 0.000153, -0.0000000967),
    '>CH2': (-0.909, 0.095, -0.0000544, 0.0000000119),
    '>CH-': (-23.0, 0.204, -0.000265, 0.00000012),
    '>C<': (-66.2, 0.427, -0.000641, 0.000000301),
    '=CH2': (23.6, -0.0381, 0.000172, -0.000000103),
    '=CH-': ( -8.00, 0.105, -0.0000963, 0.0000000356),
    '=C<': (-28.1, 0.208, -0.000306, 0.000000146 ),
    '=C=': (27.4, -0.0557, 0.000101, -0.0000000502),
    '≡CH': ( 24.5,  -0.02716, 0.000111, -0.0000000678),
    '≡C-': (7.87, 0.0201, -0.00000833, 0.00000000139 ),
    #Incremento con anillo
    '-CH2-': (-6.03, 0.0854, -0.00000800, -0.0000000180),
    '>CH-': (-20.5, 0.162, -0.00016, 0.0000000624),
    '>C<': (-90.9, 0.557, -0.0009, 0.000000469),
    '=CH-': (-2.14, 0.0574, -0.00000164, -0.0000000159),
    '-C<': (-8.25, 0.101, -0.000142, 0.000000678),
    #Incremento de Halógenos
    '-F': (26.8, -0.0913, 0.000191, -0.000000103),
    '-CL': (33.3, -0.0963, 0.000187, -0.0000000996),
    '-BR': ( 28.6, -0.0649, 0.000136, -0.0000000745),
    '-I': (32.1, -0.0641, 0.000126, -0.0000000687),
    #Incremento oxígeno
    '-OH(alcohol)': (25.7, -0.0691, 0.000177, -0.0000000988),
    '-OH(phenol)': (-2.81, 0.111, -0.000116, 0.0000000494),
    '-O-(nonring)': (25.5, -0.0632, 0.000111, -0.0000000548),
    '-O-(ring)': (12.2, -0.0296, 0.0000603, -0.0000000356),
    '>C=O(nonring)': (6.45, -0.067, 0.0000357, -0.000000311),
    '>C=O(ring)': (30.4, -0.0327, 0.000236, -0.0000000195),
    'O=CH-(aldehyde)': (30.9, -0.0336, 0.000194, -0.0000000986),
    '-COOH(acid)': (24.5, 0.0472, 0.0000402, -0.0000000452),
    '-COO-(ester)': (24.5, 0.0196, 0.0000402, -0.0000000452),
    '=O(except as above)': (6.82, 0.0196, 0.0000127, -0.0000000178),
    #Incrementos nitrógenos
    '-NH2': (26.9, -0.0412, 0.000164, -0.0000000976),
    '>NH(nonring)': (-1.21, 0.0762, -0.0000486, 0.0000000105),
    '>NH(ring)': (-11.8, -0.023, 0.000107, -0.0000000628),
    '>N-(nonring)': (31.1, 0.227, -0.00032, 0.000000146),
    '-N=(nonring)': (0,0,0,0),
    '-N=(ring)': (8.83, -0.00384, 0.0000435, -0.000000026),
    '=NH': (5.69, -0.00412, 0.000128, -0.0000000888),
    '-CN': (35.6, -0.0332, 0.000184, -0.000000103),
    '-NO2': (25.9, -0.00374, 0.000129, -0.0000000888),
    #Sulfuro incrementos
    '-SH': (35.3, -0.0758, 0.000185, -0.000000103),
    '-S-(nonring)': (19.6, -0.00561, 0.0000402, -0.0000000276),
    '-S-(ring)': (16.7, 0.00481, 0.0000277, -0.0000000211),
}


def calcular_cp_integral(grupos_funcionales, temperatura_min, temperatura_max):
    """
    Calcular el calor específico por integración numérica.
    """
    # Inicializar acumuladores para los coeficientes ajustados
    suma_a = suma_b = suma_c = suma_d = 0
    
    # Sumar los coeficientes para cada grupo funcional
    for grupo, cantidad in grupos_funcionales.items():
        if grupo in coeficientes_joback:
            a, b, c, d = coeficientes_joback[grupo]
            suma_a += cantidad * a
            suma_b += cantidad * b
            suma_c += cantidad * c
            suma_d += cantidad * d
        else:
            return None, "Grupo funcional no encontrado"

    # Definir la función a integrar
    def integrand(temperatura):
        return (suma_a - 37.93) + (suma_b + 0.210) * temperatura + (suma_c - 3.91e-4) * temperatura**2 + (suma_d + 2.06e-7) * temperatura**3

    # Realizar la integración numérica
    cp_integral, _ = quad(integrand, temperatura_min, temperatura_max)
    
    # Crear la fórmula para mostrar
    formula = f"CP = ({suma_a - 37.93} ) + ({suma_b + 0.210} ) * T + ({suma_c - 3.91e-4}) * T^2 + ({suma_d + 2.06e-7}) * T^3"" en J/mol*K"
    
    return cp_integral, formula

# Solicitar datos al usuario
def obtener_datos_usuario():
    """
    Obtener los datos de entrada del usuario.
    """
    # Función para imprimir el diccionario formateado
    print("GRUPOS FUNCIONALES")
    print("--------------------------------------------------------")
    print("Incremento sin anillo: '-CH3', '>CH2', '>CH-', '>C<', '=CH2', '=CH-', '=C<', '=C=', '≡CH', '≡C-")
    print("Incremento con anillo': '-CH2-', '>CH-', '>C<', '=CH-', '-C<")
    print("Incremento de Halógenos': '-F', '-Cl', '-Br', '-I")
    print("Incremento oxígeno': '-OH (alcohol', '-OH (fenol)', '-O- (nonring)', '-O- (ring)', '>C=O (nonring)', '>C=O (ring)', 'O=CH- (aldehyde)', '-COOH (acid)', '-COO- (ester)', '=O (except as above)")
    print("Incrementos nitrógenos': '-NH2', '>NH (nonring)', '>NH (ring)', '>N- (nonring)', '-N= (nonring)', '-N= (ring)', '=NH', '-CN', '-NO2")
    print("Sulfuro incrementos': '-SH', '-S- (nonring)', '-S- (ring)")
    print("--------------------------------------------------------")


        
    grupos_funcionales = {}
    while True:
        grupo = input("Ingrese el grupo funcional (o 'salir' para terminar): ")
        if grupo.lower() == 'salir':
            break
        cantidad = float(input(f"Ingrese la cantidad de {grupo}: "))
        grupos_funcionales[grupo] = cantidad
    
    temperatura_min = float(input("Ingrese la temperatura mínima: "))
    temperatura_max = float(input("Ingrese la temperatura máxima: "))
    
    return grupos_funcionales, temperatura_min, temperatura_max

# Función principal
def main():
    """
    Función principal del programa.
    """
    grupos_funcionales, temperatura_min, temperatura_max = obtener_datos_usuario()
    
    if temperatura_min >= temperatura_max:
        print("Error: La temperatura mínima debe ser menor que la temperatura máxima.")
        return

    resultado, formula = calcular_cp_integral(grupos_funcionales, temperatura_min, temperatura_max)
    
    if resultado is None:
        print(f"Error: {formula}")  # La variable 'formula' contiene el mensaje de error en este caso
    else:
        print(f"Entalpia: {resultado}")
        print(f"Fórmula: {formula}")

if __name__ == '__main__':
    main()
