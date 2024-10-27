from jinja2 import Environment, FileSystemLoader
import os

class Reporter:
    def __init__(self, config):
        self.config = config

    def generate_report(self, validation_results):
        env = Environment(loader=FileSystemLoader(os.path.dirname(self.config.template_file)))
        template = env.get_template(os.path.basename(self.config.template_file))
        html_content = template.render(results=validation_results)
        with open(self.config.output_file, 'w') as f:
            f.write(html_content)
