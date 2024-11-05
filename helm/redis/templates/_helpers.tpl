{{/* vim: set filetype=mustache: */}}
{{/*
Extract the name of the artifact.
*/}}

{{- define "artifact.name" -}}
{{- default "krm-kpmg-redis-app" -}}
{{- end -}}

{{- define "project.name" -}}
{{- default "dockland" -}}
{{- end -}}