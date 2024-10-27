# src/config.py

import yaml
import os

class Config:
    def __init__(self, config_file):
        # Check if the configuration file exists
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

        # Load the configuration from the YAML file
        with open(config_file, 'r') as f:
            cfg = yaml.safe_load(f)

        # Assign configuration parameters with defaults where necessary
        self.checks = cfg.get('checks', {})
        self.fuzzy_match_threshold = cfg.get('fuzzy_match_threshold', 80)
        self.approved_variables_file = cfg.get('approved_variables_file', 'data/approved_variables.csv')
        self.report = cfg.get('report', {})
        self.output_file = self.report.get('output_file', 'reports/report.html')
        self.template_file = self.report.get('template_file', 'templates/report_template.html')

        # Validate essential configuration parameters
        self.validate_config()

    def validate_config(self):
        # Ensure the approved variables file exists
        if not os.path.exists(self.approved_variables_file):
            raise FileNotFoundError(f"Approved variables file '{self.approved_variables_file}' not found.")

        # Ensure the template file exists
        if not os.path.exists(self.template_file):
            raise FileNotFoundError(f"Template file '{self.template_file}' not found.")

        # Ensure the output directory exists; if not, create it
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

    # You can add any additional methods if necessary
