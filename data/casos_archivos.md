Casos de prueba para archivos CSV
1. Archivo: playas.csv
Fila	Datos	Condición que se prueba	Resultado esperado
2	Rodadero;10;2026;11;18	Registro válido	Aceptar
3	Playa Blanca;8;2026;11;19	Registro válido	Aceptar
4	Taganga;15;2026;12;5	Registro válido	Aceptar
5	;10;2026;11;20	Nombre vacío	Rechazar o reportar error
6	Rodadero;12;2026;11;21	Nombre repetido	Rechazar o reportar duplicado
7	Playa Salguero;abc;2026;11;22	Cantidad no entera	Rechazar o reportar error
8	Playa Grande;0;2026;11;23	Cantidad igual a cero	Rechazar o reportar error
9	Playa Bello;7.5;2026;11;24	Cantidad decimal	Rechazar o reportar error
10	Playa Cristal;9;2026;2;30	Fecha inexistente	Rechazar o reportar error
2. Archivo: alquileres.csv
Fila	Datos	Condición que se prueba	Resultado esperado
2	Rodadero;3	Alquiler válido	Aceptar
3	Playa Blanca;5	Alquiler válido	Aceptar
4	Taganga;10	Alquiler válido	Aceptar
5	;2	Nombre de playa vacío	Rechazar o reportar error
6	Rodadero	Falta la cantidad alquilada	Rechazar o reportar error
7	Playa Inexistente;2	Playa no registrada	Rechazar o reportar error
8	Rodadero;abc	Cantidad no entera	Rechazar o reportar error
9	Rodadero;12	Alquiler superior a las 10 carpas instaladas	Rechazar o reportar error
3. Observaciones para revisar con el equipo
Confirmar si el programa rechaza solamente la fila incorrecta o todo el archivo.
Confirmar cómo se manejan los nombres repetidos.
Confirmar si las fechas pasadas o futuras son permitidas.
Confirmar qué mensaje muestra el programa cuando encuentra un dato inválido.
Verificar que los archivos utilicen punto y coma (;) como separador y estén guardados en UTF-8.
