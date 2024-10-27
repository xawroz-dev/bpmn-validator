import os
from lxml import etree

class BPMNParser:
    def parse_directory(self, directory):
        service_tasks = []
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.bpmn'):
                    file_path = os.path.join(root, filename)
                    service_tasks.extend(self.parse_file(file_path, filename))
        return service_tasks

    def parse_files(self, file_paths):
        service_tasks = []
        for file_path in file_paths:
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                service_tasks.extend(self.parse_file(file_path, filename))
            else:
                print(f"File not found: {file_path}")
        return service_tasks

    def parse_file(self, file_path, filename):
        tree = etree.parse(file_path)
        namespace = {
            'bpmn2': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
            'camunda': 'http://camunda.org/schema/1.0/bpmn'
        }
        tasks = tree.xpath('//bpmn2:serviceTask', namespaces=namespace)
        service_tasks = []
        for task in tasks:
            task_id = task.get('id')
            task_name = task.get('name')
            input_output = self.parse_io(task, namespace)
            service_tasks.append({
                'file_name': filename,   # Add BPMN file name
                'id': task_id,
                'name': task_name,
                'inputOutput': input_output
            })
        return service_tasks

    def parse_io(self, task, namespace):
        variables = []
        extension_elements = task.find('bpmn2:extensionElements', namespaces=namespace)
        if extension_elements is not None:
            input_output = extension_elements.find('camunda:inputOutput', namespaces=namespace)
            if input_output is not None:
                # Parse input parameters
                input_parameters = input_output.findall('camunda:inputParameter', namespaces=namespace)
                for param in input_parameters:
                    variables.append(param.get('name'))
                # Parse output parameters
                output_parameters = input_output.findall('camunda:outputParameter', namespaces=namespace)
                for param in output_parameters:
                    variables.append(param.get('name'))
        return variables
