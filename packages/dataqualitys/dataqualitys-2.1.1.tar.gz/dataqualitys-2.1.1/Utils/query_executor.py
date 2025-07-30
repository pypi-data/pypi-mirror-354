from jinja2 import Environment, FileSystemLoader, ChoiceLoader
import pkg_resources
import os
from typing import Dict,List

class QueryExecutor:
    def __init__(self, connector, db_type: str, config: Dict):
        self.connector = connector
        self.db_type = db_type
        self.config = config

        base_template_path = pkg_resources.resource_filename('dataqualitys', 'templates')

        # Construct full paths using db_type and common
        db_type_template_path = os.path.join(base_template_path, db_type)
        common_template_path = os.path.join(base_template_path, "common")

        # Use ChoiceLoader for multiple fallback locations
        self.env = Environment(
            loader=ChoiceLoader([
                FileSystemLoader(db_type_template_path),
                FileSystemLoader(common_template_path)
            ]),
            trim_blocks=True,
            lstrip_blocks=True
        )

    ''' def render_query(self, template_name: str, context: Dict) -> str:
        """  Process column names before rendering """
        if 'column_name' in context:
            context['column_name'] = quote_if_reserved(context['column_name'])

        """Render SQL template with context"""
        template = self.env.get_template(template_name)
        return template.render(context)
     '''

    def render_query(self, template_name: str, context: Dict) -> str:
        """Process column names before rendering"""
        if 'column_name' in context:
            context['column_name'] = quote_if_reserved(context['column_name'])

        # Add database name to context if available
        if 'database_name' not in context and 'database' in self.config:
            context['database_name'] = self.config['database']

        """Render SQL template with context"""
        template = self.env.get_template(template_name)
        return template.render(context)

    def execute(self, query: str) -> List[Dict]:
        """Execute query and return results"""
        return self.connector.run_query(query)
