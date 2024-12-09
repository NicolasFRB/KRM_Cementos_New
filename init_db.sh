#!/bin/sh

# Esperar a que la base de datos esté lista (puedes ajustar el host y el puerto según tu configuración)
until pg_isready -h 10.37.131.53 -p 5432 -U krm_admin; do
  echo "Esperando a que la base de datos esté lista..."
  sleep 2
done

# Insertar la fila en la tabla cuando la base de datos esté lista
psql -h 10.37.131.53 -U krm_admin -d krmpostgres_dev -c "
INSERT INTO configuration_configuration (app_name, main_email, enable_emails)
VALUES ('ECI KRM Tool', 'joseantonio.davilaperez@colaborador.elcorteingles.es', true)
ON CONFLICT DO NOTHING;
"

# Ejecutar el comando principal de la aplicación
exec "$@"
