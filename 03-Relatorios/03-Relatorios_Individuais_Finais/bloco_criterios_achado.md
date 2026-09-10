### Critérios
{% set criterios_achado = auditado.get_criterios_achado(id_achado) %}
{% set criterios_gerais = criterios_achado | rejectattr('especifico') | list %}
{% set criterios_especificos = criterios_achado | selectattr('especifico') | list %}
{% for criterio in criterios_gerais %}
* {{ criterio.descricao.rstrip('.') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% if criterios_especificos %}

{% for criterio in criterios_especificos %}
* {{ criterio.descricao.rstrip('.') }}{{ '.' if loop.last else ';' }}
{% endfor %}

{% endif %}
