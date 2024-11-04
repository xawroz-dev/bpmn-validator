import pandas as pd

class Validator:
    def __init__(self, config):
        self.config = config
        self.approved_variables = pd.read_csv(config.approved_variables_file)
        self.has_errors = False  # Add this flag

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

            # Default service task name check
            check_cfg = self.config.checks.get('default_service_task_name', {})
            if check_cfg.get('enabled', False) and task['id'].startswith('Activity_'):
                issue = task_info.copy()
                issue['severity'] = check_cfg.get('severity', 'warning')
                results['default_name_issues'].append(issue)
                if issue['severity'] == 'error':
                    self.has_errors = True

            # Variable name validation
            check_cfg = self.config.checks.get('validate_variables', {})
            if check_cfg.get('enabled', False):
                var_issues = self.validate_variables(task['inputOutput'], task_info, check_cfg)
                if var_issues:
                    results['variable_name_issues'].extend(var_issues)

        return results

    def validate_variables(self, variables, task_info, check_cfg):
        issues = []
        for var in variables:
            if var not in self.approved_variables['variable_name'].values:
                result = process.extractOne(
                    var,
                    self.approved_variables['variable_name'],
                    score_cutoff=self.config.fuzzy_match_threshold
                )
                if result:
                    suggestion, score = result[0], result[1]
                    issue = {
                        'file_name': task_info['file_name'],
                        'task_id': task_info['task_id'],
                        'task_name': task_info['task_name'],
                        'variable': var,
                        'suggestion': suggestion,
                        'score': score,
                        'severity': check_cfg.get('severity', 'warning')
                    }
                else:
                    issue = {
                        'file_name': task_info['file_name'],
                        'task_id': task_info['task_id'],
                        'task_name': task_info['task_name'],
                        'variable': var,
                        'suggestion': 'No close match found',
                        'score': 'N/A',
                        'severity': check_cfg.get('severity', 'warning')
                    }
                issues.append(issue)
                if issue['severity'] == 'error':
                    self.has_errors = True
        return issues
