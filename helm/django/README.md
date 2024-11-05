# ECI HELM Chart Template

## Cambios a realizar en el template:

### /pom.xml
- artifactId = Nombre del repositorio de despliegue.
- name = Nombre de aplicacion.
```xml
<artifactId>poc-component-3-deployconfig</artifactId>
<name>poc-component-3</name>
```

### /Chart.yaml
- name = Nombre del repositorio de despliegue.
```yaml
name: srv-std-0ae-pma-poc-component-10-deployment
```

### /templates/_helpers.tpl
- default = Nombre de la organizacion Quay, se corresponde con el nombre del proyecto de Bitbucket.
```
{{- default "0ae-pma-pocs-devsecops-atp" -}}  
```

## Configuracion de despliegue en el template:

Dentro de la carpeta /config, están disponibles subcarpetas que contienen la configuración de despliegue propia del entorno.

## Comandos para test en entorno local

### Pre-requisitos uso Helm en entorno local:
- Instalado cliente Helm
- Instalado cliente Kubernetes/Openshift ( kubectl / oc )

### Instalacion

```shell
helm upgrade {NOMBRE_CHART} {RUTA_CHART_LOCAL} -n {NAMESPACE} -f {RUTA_CHART_LOCAL}/config/{LOGICAL_ENVIRONMENT}/values.yaml --atomic --install --timeout=900s --set appVersion=1.0.1-SNAPSHOT
```
### Desinstalacion

```shell
helm uninstall {NOMBRE_CHART}
```
