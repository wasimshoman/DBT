{% macro run_clustering() %}
    {% set python_cmd %}
        python "C:\\Users\\wss7\\Projects\\internal\\DBT\\retail_pg\\Train_Classifier.py"
    {% endset %}

    {% do run_query(python_cmd) %}
    {{ log("Executed clustering script", info=true) }}
{% endmacro %}