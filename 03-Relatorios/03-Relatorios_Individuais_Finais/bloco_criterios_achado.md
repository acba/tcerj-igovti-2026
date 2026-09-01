### Critérios
{% set criterios_achado = auditado.get_criterios_achado(nome_achado) %}
{% for criterio in criterios_achado if not criterio.especifico %}
* {{ criterio.descricao.rstrip('.') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% set enquadramentos_especificos = auditado.get_enquadramentos_especificos_achado(nome_achado) %}
{% if enquadramentos_especificos %}
{% set criterios_especificos = criterios_achado | selectattr('especifico') | list %}

{% for criterio in criterios_especificos %}
* {{ criterio.descricao.rstrip('.') }}{{ '.' if loop.last else ';' }}
{% endfor %}

{% endif %}
