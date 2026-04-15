from flask import Flask, render_template, request
from tabla import TABLA, MESES, SEXOS

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    error = None
    modo = 'edad_mes'

    if request.method == 'POST':
        modo = request.form.get('modo', 'edad_mes')

        try:
            edad = int(request.form.get('edad', '').strip())
            if edad not in TABLA:
                raise ValueError('La edad ingresada no existe en la tabla.')

            if modo == 'edad_mes':
                mes = request.form.get('mes', '').strip()
                if mes not in MESES:
                    raise ValueError('Mes inválido.')

                sexo = TABLA[edad].get(mes)
                if not sexo:
                    raise ValueError('No se encontró resultado para esa combinación.')

                resultado = {
                    'tipo': 'sexo',
                    'edad': edad,
                    'mes': MESES[mes],
                    'sexo': 'Masculino' if sexo == 'Mas' else 'Femenino'
                }

            elif modo == 'edad_sexo':
                sexo = request.form.get('sexo', '').strip()
                if sexo not in SEXOS:
                    raise ValueError('Sexo inválido.')

                meses = [MESES[codigo] for codigo, valor in TABLA[edad].items() if valor == sexo]

                resultado = {
                    'tipo': 'meses',
                    'edad': edad,
                    'sexo': 'Masculino' if sexo == 'Mas' else 'Femenino',
                    'meses': meses
                }
            else:
                raise ValueError('Modo de consulta inválido.')

        except ValueError as e:
            error = str(e)
        except Exception:
            error = 'Ocurrió un error al procesar la consulta.'

    edades = sorted(TABLA.keys())
    return render_template(
        'index.html',
        edades=edades,
        meses=MESES,
        sexos=SEXOS,
        resultado=resultado,
        error=error,
        modo=modo
    )

if __name__ == '__main__':
    app.run(debug=True)
