import pandas as pd
from thefuzz import process

class Validator:
    def __init__(self, config):
        self.config = config
        self.approved_variables = pd.read_csv(config.approved_variables_file)

    def validate(self, service_tasks):
        results = {
            'default_name_issues': [],
            'variable_name_issues': []
        }
        for task in service_tasks:
            task_info = {
                'file_name': task['file_name'],
                'task_id': task['id'],
                'task_name': task['name']
            }
            if self.config.checks.get('default_service_task_name') and task['id'].startswith('Activity_'):
                # Include file name and task name in the issue
                results['default_name_issues'].append(task_info)
            if self.config.checks.get('validate_variables'):
                var_issues = self.validate_variables(task['inputOutput'], task_info)
                if var_issues:
                    results['variable_name_issues'].extend(var_issues)
        return results

    def validate_variables(self, variables, task_info):
        issues = []
        for var in variables:
            if var not in self.approved_variables['variable_name'].values:
                result = process.extractOne(
                    var,
                    self.approved_variables['variable_name'],
                    score_cutoff=self.config.fuzzy_match_threshold
                )
                if result:
                    # Unpack result depending on its length
                    if len(result) == 2:
                        suggestion, score = result
                    elif len(result) == 3:
                        suggestion, score, _ = result
                    else:
                        raise ValueError(f"Unexpected result length: {len(result)}")
                    issue = {
                        'file_name': task_info['file_name'],
                        'task_id': task_info['task_id'],
                        'task_name': task_info['task_name'],
                        'variable': var,
                        'suggestion': suggestion,
                        'score': score
                    }
                else:
                    issue = {
                        'file_name': task_info['file_name'],
                        'task_id': task_info['task_id'],
                        'task_name': task_info['task_name'],
                        'variable': var,
                        'suggestion': 'No close match found',
                        'score': 'N/A'
                    }
                issues.append(issue)
        return issues

