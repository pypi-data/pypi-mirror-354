# Instrucciones de uso
Esta librería consta de 3 clases:
1. graficar_2d: Análisis de sensibilidad simple. Se pueden pedir uno o dos resultados a la vez. Si se piden 2 se crea automáticamente un gráfico con doble eje Y. Se puede controlar la escala de cada eje Y de forma independiente ('linear' o 'log') usando el parámetro escalas_y
    GraficadorCombustion(nombre_combustible='YYY').graficar_2d(
        variable_x='rel_equivalencia',
        rango_x=(0.6, 1.4, 40),
        variables_y=['T_out_K', 'X_NOx'], # Pido dos resultados
        parametros_fijos={ ... },
        escalas_y=['linear', 'log'] # El primer eje lineal, el segundo logarítmico
    )
2. graficar_3d: Mapeo de superficie. Sirve para obtener una visión global de cómo un resultado se comporta en un espacio de diseño definido por dos variables de entrada. Genera una superficie 3D interactiva que puedes rotar con el ratón para explorar su forma.
    GraficadorCombustion(nombre_combustible='YYY').graficar_3d(
        variable_x='T_in_K',
        rango_x=(600, 1000, 25),
        variable_y='rel_equivalencia',
        rango_y=(0.7, 1.3, 25),
        variable_z='X_NOx', # El resultado que forma la "montaña"
        parametros_fijos={ ... }
    )
3. graficar_barrido_parametrico: Análisis paramétrico. ¿Cómo se ve afectada mi curva de Y vs X si varía otro input? Define una variable para el eje X (variable_x), una para el eje Y (variable_y), y una tercera para el barrido (variable_barrido). Genera múltiples curvas en el mismo gráfico, una para cada valor del parámetro de barrido.
    GraficadorCombustion(nombre_combustible='YYY').graficar_barrido_parametrico(
        variable_x='rel_equivalencia',
        rango_x=(0.7, 1.3, 50), 
        variable_y='X_NOx',
        variable_barrido='P_in_atm', # Barreré la presión
        valores_barrido=[5, 10, 15, 20], # Para estas 4 presiones
        parametros_fijos={ ... }
    )
# Lista de parámetros con los que trabajar:
Entrada:
    nombre_combustible: El nombre del combustible que se usará en la simulación (ej. 'CH4', 'NC10H22'). Debe ser una especie que exista en el mecanismo de reacción
    rel_equivalencia
    T_in_K
    P_in_atm
    tiempo_residencia_s
Salida:
    T_out_K
    efficiency_pct
    X_NOx
    X_fuel_inquemado
    X_CO
    X_CO2
    X_otros_HC

# script de ejemplo

    from graficombustion import GraficadorCombustion
    import cantera as ct

# --- 1. Gráfico 2D con dos ejes: uno lineal y uno logarítmico ---
    print("--- EJEMPLO 1: GRÁFICO 2D CON ESCALAS MIXTAS ---")
    try:
        graficador_2d = GraficadorCombustion(nombre_combustible='NC10H22')
        graficador_2d.graficar_2d(
            variable_x='rel_equivalencia',
            rango_x=(0.5, 1.5, 30),  #(min, max, discretizacion)
            parametros_fijos={
              'T_in_K': 750,
               'P_in_atm': 20,
               'P_in_atm': 20,
               'tiempo_residencia_s': 0.005
            },
             escalas_y=['linear', 'log']
        )
    except (ValueError, ImportError) as e:
        print(f"Error: {e}")

# --- 2. Gráfico 2D con escala lineal por defecto ---
    print("\n--- EJEMPLO 2: GRÁFICO 2D CON ESCALA LINEAL (POR DEFECTO) ---")
    try:
        graficador_lineal = GraficadorCombustion(nombre_combustible='CH4')
        graficador_lineal.graficar_2d(
            variable_x='rel_equivalencia',
            rango_x=(0.7, 1.3, 25),
            variables_y=['X_NOx', 'X_CO'],
            parametros_fijos={
                'T_in_K': 800,
                'P_in_atm': 10,
                'tiempo_residencia_s': 0.01
            }
        )
    except (ValueError, ImportError) as e:
        print(f"Error: {e}")

# --- 3. Gráfico 3D (funciona como antes) ---
    print("\n--- EJEMPLO 3: GRÁFICO 3D ---")
    try:
        graficador_3d = GraficadorCombustion(nombre_combustible='CH4')
        graficador_3d.graficar_3d(
            variable_x='T_in_K',
            rango_x=(600, 1000, 25),
            variable_y='rel_equivalencia',
            rango_y=(0.7, 1.3, 25),
            variable_z='X_NOx',
            parametros_fijos={
                'P_in_atm': 10,
                'tiempo_residencia_s': 0.004
            }
        )
    except (ValueError, ImportError) as e:
        print(f"Error: {e}")

# --- 4. Ejemplo Avanzado: Presión y Temperatura Acopladas ---
    print("\n--- EJEMPLO 4: GRÁFICO AVANZADO CON PARÁMETRO FUNCIONAL ---")
    try:
        # 1. Definir la función que calcula la temperatura. Esta función recibirá la presión actual (la variable x) y devolverá la temperatura calculada.
        nombre_combustible_av = 'CH4'
        phi_av = 0.7
        T1_K_av = 300.0
        P1_atm_av = 1.0
        #Aqui usamos un poquito de cantera para calcular el exponente isentropico, si sacamos los datos de unas tablas o algo nos ahorramos esto y lo declaramos directamente
        gas_ref = ct.Solution('gri30.yaml')
        gas_ref.TP = T1_K_av, P1_atm_av * ct.one_atm
        gas_ref.set_equivalence_ratio(phi_av, nombre_combustible_av, 'O2:1.0, N2:3.76')
        exponente_av = (ct.gas_constant / gas_ref.mean_molecular_weight) / gas_ref.cp_mass


    def temperatura_isentropica(P2_atm):
        """Calcula la temperatura T2 para una presión P2 dada."""
        return T1_K_av * (max(P2_atm / P1_atm_av, 1e-9)) ** exponente_av


    # 2. Llamar al graficador
    graficador_avanzado = GraficadorCombustion(nombre_combustible=nombre_combustible_av)
    graficador_avanzado.graficar_2d(
        variable_x='P_in_atm',
        rango_x=(1, 40, 40),
        variables_y=['X_NOx', 'X_CO'],
        parametros_fijos={
            'T_in_K': temperatura_isentropica,  # ¡Pasamos la función como parámetro!
            'rel_equivalencia': phi_av,
            'tiempo_residencia_s': 0.025
        },
        escalas_y=['linear', 'linear']  # Forzamos escala lineal para ambos ejes
    )
    except (ValueError, ImportError) as e:
        print(f"Error: {e}")

# --- 5. Ejemplo Final: Gráfico de Barrido Paramétrico ---
    print("\n--- EJEMPLO 5: GRÁFICO DE BARRIDO PARAMÉTRICO ---")
    try:
        graficador_barrido = GraficadorCombustion(nombre_combustible='NC10H22')

        # Este método generará un gráfico de NOx vs. Phi para varias presiones
        graficador_barrido.graficar_barrido_parametrico(
            variable_x='rel_equivalencia',
            rango_x=(0.7, 1.3, 50),
            variable_y='X_NOx',
            variable_barrido='P_in_atm',
            valores_barrido=[5, 15, 20, 30],  # Lista de presiones para cada curva
            parametros_fijos={
                'T_in_K': 600,  # Temperatura de entrada fija y alta para generar NOx
                'tiempo_residencia_s': 0.020
            },
            escala_y='linear'
        )

    except (ValueError, ImportError) as e:
        print(f"Error: {e}")