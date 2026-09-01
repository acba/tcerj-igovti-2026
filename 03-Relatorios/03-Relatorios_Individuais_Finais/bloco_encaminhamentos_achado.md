### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }} a {{ auditado.sigla }}** para que, {{ e.fundamentacao_encaminhamento.rstrip('.;') }}, {{ e.encaminhamento.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
