import numpy as np
import matplotlib.pyplot as plt
from simcombustion import CombustionAnalyzer


class GraficadorCombustion:
    """
    Librería robusta para generar gráficos de simulaciones de combustión.
    Crea gráficos 2D (con uno o dos ejes Y) y 3D de forma sencilla.
    """

    def __init__(self, nombre_combustible):
        print(f"INFO: Creando instancia de GraficadorCombustion para '{nombre_combustible}'.")
        self.analizador = CombustionAnalyzer(fuel_name=nombre_combustible)
        self._mapa_entradas = {
            'rel_equivalencia': 'rel_equivalencia',
            'T_in_K': 'T_in_K',
            'P_in_atm': 'P_in_atm',
            'tiempo_residencia_s': 'tiempo_residencia_s'
        }

    def graficar_2d(self, variable_x, rango_x, variables_y, parametros_fijos, escalas_y=None):
        """
        Genera un gráfico 2D con control sobre la escala de los ejes Y.

        Args:
            variable_x (str): Nombre de la variable independiente (eje X).
            rango_x (tuple): Rango para la variable x (inicio, fin, num_puntos).
            variables_y (list): Lista con una o dos variables de salida (ejes Y).
            parametros_fijos (dict): Diccionario con los valores fijos.
            escalas_y (list, opcional): Lista con la escala para cada eje Y (ej. ['linear', 'log']).
                                        Si no se especifica, todos serán lineales.
        """
        if not isinstance(variables_y, list) or not (1 <= len(variables_y) <= 2):
            raise ValueError("`variables_y` debe ser una lista con 1 o 2 nombres de variables.")

        valores_x = np.linspace(rango_x[0], rango_x[1], rango_x[2])
        resultados_y = {name: [] for name in variables_y}

        print(f"INFO: Iniciando barrido 2D para {variables_y} vs {variable_x}...")

        for valor_x_actual in valores_x:
            params_sim = {}
            for key, value in parametros_fijos.items():
                if callable(value):
                    params_sim[key] = value(valor_x_actual)
                else:
                    params_sim[key] = value

            params_sim[self._mapa_entradas[variable_x]] = valor_x_actual
            resultados_sim = self.analizador.calcular_propiedades(**params_sim)
            for name in variables_y:
                resultados_y[name].append(resultados_sim.get(name, np.nan))

        # --- Creación y configuración del gráfico ---
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Eje Y principal (izquierdo)
        var1_name = variables_y[0]
        color1 = 'tab:blue'
        ax1.set_xlabel(variable_x)
        ax1.set_ylabel(var1_name, color=color1)
        ax1.plot(valores_x, resultados_y[var1_name], color=color1, marker='o', linestyle='-', label=var1_name)
        ax1.tick_params(axis='y', labelcolor=color1)

        # --- NUEVA LÓGICA PARA LA ESCALA ---
        if escalas_y and len(escalas_y) >= 1:
            ax1.set_yscale(escalas_y[0])

        # Eje Y secundario (derecho), si es necesario
        if len(variables_y) == 2:
            var2_name = variables_y[1]
            color2 = 'tab:red'
            ax2 = ax1.twinx()
            ax2.set_ylabel(var2_name, color=color2)
            ax2.plot(valores_x, resultados_y[var2_name], color=color2, marker='x', linestyle='--', label=var2_name)
            ax2.tick_params(axis='y', labelcolor=color2)

            # --- NUEVA LÓGICA PARA LA ESCALA ---
            if escalas_y and len(escalas_y) >= 2:
                ax2.set_yscale(escalas_y[1])

        fig.tight_layout()
        plt.title(f'Análisis de {self.analizador.fuel_name}')
        ax1.grid(True)
        # Añadimos una leyenda
        fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
        plt.show()

    def graficar_3d(self, variable_x, rango_x, variable_y, rango_y, variable_z, parametros_fijos):
        # El método 3D vuelve a su forma original y simple.
        if variable_x not in self._mapa_entradas or variable_y not in self._mapa_entradas:
            raise ValueError("Una de las variables independientes no es reconocida.")

        vals_x = np.linspace(rango_x[0], rango_x[1], rango_x[2])
        vals_y = np.linspace(rango_y[0], rango_y[1], rango_y[2])
        X, Y = np.meshgrid(vals_x, vals_y)
        Z = np.zeros_like(X)

        print(f"INFO: Iniciando barrido 3D para {variable_z} vs ({variable_x}, {variable_y})...")

        for i, val_y in enumerate(vals_y):
            for j, val_x in enumerate(vals_x):
                params_sim = parametros_fijos.copy()
                params_sim[self._mapa_entradas[variable_x]] = val_x
                params_sim[self._mapa_entradas[variable_y]] = val_y

                resultados_sim = self.analizador.calcular_propiedades(**params_sim)
                Z[i, j] = resultados_sim.get(variable_z, np.nan)

        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', rstride=1, cstride=1, antialiased=False)
        ax.set_xlabel(variable_x)
        ax.set_ylabel(variable_y)
        ax.set_zlabel(variable_z)
        plt.title(f'Superficie 3D de {variable_z} para {self.analizador.fuel_name}')
        fig.colorbar(surf, shrink=0.5, aspect=5, label=variable_z)
        plt.show()

    def graficar_barrido_parametrico(self, variable_x, rango_x, variable_y,
                                     variable_barrido, valores_barrido,
                                     parametros_fijos, escala_y='linear'):
        """
        Genera un gráfico 2D con múltiples curvas, cada una correspondiendo
        a un valor de un parámetro de barrido.

        Args:
            variable_x (str): Nombre de la variable del eje X.
            rango_x (tuple): Rango para la variable x (inicio, fin, num_puntos).
            variable_y (str): Nombre de la variable del eje Y.
            variable_barrido (str): Nombre del parámetro que varía en cada curva.
            valores_barrido (list): Lista de valores para el parámetro de barrido.
            parametros_fijos (dict): Diccionario con el resto de parámetros fijos.
            escala_y (str, opcional): Escala para el eje Y ('linear' o 'log').
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        # Bucle externo: itera sobre los valores del parámetro de barrido (ej. presiones)
        for valor_barrido in valores_barrido:
            print(f"INFO: Calculando curva para {variable_barrido} = {valor_barrido}...")

            valores_x = np.linspace(rango_x[0], rango_x[1], rango_x[2])
            valores_y_curva = []

            # Bucle interno: calcula los puntos de una curva (ej. barrido en phi)
            for valor_x_actual in valores_x:
                params_sim = parametros_fijos.copy()
                params_sim[self._mapa_entradas[variable_x]] = valor_x_actual
                params_sim[self._mapa_entradas[variable_barrido]] = valor_barrido

                # Los parámetros funcionales también funcionan aquí si estuvieran en parametros_fijos
                for key, value in params_sim.items():
                    if callable(value):
                        params_sim[key] = value(valor_x_actual)

                resultados_sim = self.analizador.calcular_propiedades(**params_sim)
                valores_y_curva.append(resultados_sim.get(variable_y, np.nan))

            # Dibuja la curva calculada en el gráfico
            ax.plot(valores_x, valores_y_curva, marker='o', linestyle='-',
                    label=f'{variable_barrido.replace("_", " ")} = {valor_barrido}')

        # Configuración final del gráfico
        ax.set_xlabel(variable_x)
        ax.set_ylabel(variable_y)
        ax.set_yscale(escala_y)
        ax.set_title(f'{variable_y} vs {variable_x} para diferentes {variable_barrido}')
        ax.legend()
        ax.grid(True, linestyle=':')
        plt.show()