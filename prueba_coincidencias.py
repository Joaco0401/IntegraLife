from coincidencias import clave_empresa, buscar_coincidencia

print(clave_empresa("John O'Ryan Surveyors"))
print(clave_empresa("John ORyan Surveyors"))
print(clave_empresa("JOHN O´RYAN SURVEYORS."))

candidatos = [{"id": "1", "nombre": "John ORyan Surveyors"}]
resultado, puntaje = buscar_coincidencia("John O'Ryan Surveyors", candidatos, es_empresa=True)
print("Coincide con:", resultado, "puntaje:", puntaje)