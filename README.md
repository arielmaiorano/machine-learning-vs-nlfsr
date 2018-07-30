### Clasificación de registros desplazables no lineales mediante aprendizaje automático

Experimento, utilizando diferentes técnicas de aprendizaje automático, para medir la eficacia de clasificar configuraciones de registros desplazables no lineales -o NLFSRs, por sus siglas en inglés: Non Linear Feedback Shift Registers-, de tamaños predeterminados, en dos grupos o clases; siendo el obje-tivo identificar aquellos con período de recursión máximo.

#### Instalación de requisitos

Ejemplo utilizando Anaconda (Windows) dentro de carpeta del proyecto:

```

conda create --prefix  .\env python=3.6

activate .\env

pip install tensorflow

pip install keras

pip install pandas

pip install sklearn

```

#### Generación de dataset

Se incluyen los archivos .txt con los listados de NLFSRs encontrados mediante búsqueda exhaustiva por Elena Dubrova (ver http://eprint.iacr.org/2012/166.pdf).

```

python generar_dataset.py

```

#### Entrenamiento y validación

Se incluye salida de ejemplo obtenida ejecutando:

```

python experimento.py > salida_experimento.txt

```


