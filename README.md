## Instalación

1. Crear un ambiente virtual de python e instalar los requerimientos del `requirements.txt`
2. Colocar en la raiz del repositorio los modelos entrenados para la detección de entidades.
3. Lanzar el servidor de anotación con el comando `<ubicación de los binarios del ambiente virtual>/python app.py`

## Utilización

Este servicio web expone endpoints para la búsqueda de distintas entidades y las expone en `/<nombre de la entidad>`. Para realizar una anotación, se debe enviar una petición POST al respectivo endpoint con un objeto JSON que contenga la propiedad `text`.

El sevicio responderá con un objeto JSON que contiene las anotaciones con las siguientes propiedades:

* `entities`: Lista de entidades anotadas, en donde cada anotación es una lista que contiene el índice de la anotación, el nombre de la entidad, y una lista que contiene el caracter de inicio y fin de la anotación.
* `labels`: Lista de etiquetas asociadas a cada uno de los tokens del texto consultado.
* `normalized_text`: Texto preprocesado.
* `probabilities`: Probabilidades asociadas a cada uno de los tokens respecto a cada una de las etiquetas.
* `raw_text`: Texto consultado.
* `tagged_string`: Texto consultado con las anotaciones agregadas.
* `tokens`: Lista de tokens encontrados en el texto consultado.

## Ejemplo de utilización

Para anotar la cadena de texto *paciente con carcinoma espinocelular de borde de lengua* se debe realizar la siguiente petición:

```bash
curl --location --request POST 'http(s)://<server url>/neoplasm_morphologies' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text":"paciente con carcinoma espinocelular de borde de lengua"
}'
```

y la respuesta será la siguiente:

```javascript
{
    "entities": [
        [
            "T1",
            "MORFOLOGIA_NEOPLASIA",
            [
                [
                    13,
                    36
                ]
            ]
        ]
    ],
    "labels": [
        "O",
        "O",
        "B-MORFOLOGIA_NEOPLASIA",
        "I-MORFOLOGIA_NEOPLASIA",
        "O",
        "O",
        "O",
        "O"
    ],
    "normalized_text": "paciente con carcinoma espinocelular de borde de lengua",
    "probabilities": [
        {
            "ner": [
                "<unk> (0.0)",
                "O (0.9997)",
                "B-MORFOLOGIA_NEOPLASIA (0.0)",
                "I-MORFOLOGIA_NEOPLASIA (0.0)",
                "<START> (0.0)",
                "<STOP> (0.0002)"
            ]
        },
        {
            "ner": [
                "<unk> (0.0)",
                "O (0.9727)",
                "B-MORFOLOGIA_NEOPLASIA (0.0)",
                "I-MORFOLOGIA_NEOPLASIA (0.0)",
                "<START> (0.0)",
                "<STOP> (0.0272)"
            ]
        },
        {
            "ner": [
                "<unk> (0.0)",
                "O (0.0)",
                "B-MORFOLOGIA_NEOPLASIA (0.9878)",
                "I-MORFOLOGIA_NEOPLASIA (0.0)",
                "<START> (0.0)",
                "<STOP> (0.0122)"
            ]
        },
        {
            "ner": [
                "<unk> (0.0)",
                "O (0.0005)",
                "B-MORFOLOGIA_NEOPLASIA (0.0)",
                "I-MORFOLOGIA_NEOPLASIA (0.999)",
                "<START> (0.0)",
                "<STOP> (0.0004)"
            ]
        },
        {
            "ner": [
                "<unk> (0.0001)",
                "O (0.7672)",
                "B-MORFOLOGIA_NEOPLASIA (0.0)",
                "I-MORFOLOGIA_NEOPLASIA (0.232)",
                "<START> (0.0)",
                "<STOP> (0.0007)"
            ]
        },
        {
            "ner": [
                "<unk> (0.0)",
                "O (0.5432)",
                "B-MORFOLOGIA_NEOPLASIA (0.0)",
                "I-MORFOLOGIA_NEOPLASIA (0.408)",
                "<START> (0.0)",
                "<STOP> (0.0487)"
            ]
        },
        {
            "ner": [
                "<unk> (0.0)",
                "O (0.9662)",
                "B-MORFOLOGIA_NEOPLASIA (0.0)",
                "I-MORFOLOGIA_NEOPLASIA (0.0256)",
                "<START> (0.0)",
                "<STOP> (0.0081)"
            ]
        },
        {
            "ner": [
                "<unk> (0.0)",
                "O (0.8688)",
                "B-MORFOLOGIA_NEOPLASIA (0.0002)",
                "I-MORFOLOGIA_NEOPLASIA (0.0327)",
                "<START> (0.0)",
                "<STOP> (0.0982)"
            ]
        }
    ],
    "raw_text": "paciente con carcinoma espinocelular de borde de lengua",
    "tagged_string": "paciente con carcinoma <B-MORFOLOGIA_NEOPLASIA> espinocelular <I-MORFOLOGIA_NEOPLASIA> de borde de lengua",
    "tokens": [
        "paciente",
        "con",
        "carcinoma",
        "espinocelular",
        "de",
        "borde",
        "de",
        "lengua"
    ]
}
```