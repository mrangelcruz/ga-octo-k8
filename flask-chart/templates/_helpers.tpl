{{- define "flask-chart.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "flask-chart.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end }}
