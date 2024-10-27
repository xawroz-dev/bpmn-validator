import argparse
from src.config import Config
from src.parser import BPMNParser
from src.validator import Validator
from src.reporter import Reporter

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='BPMN Validator')
    parser.add_argument('--file-list', type=str, help='Path to a file containing list of BPMN files to process')
    args = parser.parse_args()

    # Load configuration
    config = Config('config.yaml')

    # Parse BPMN files
    bpmn_parser = BPMNParser()
    if args.file_list:
        with open(args.file_list, 'r') as f:
            file_paths = [line.strip() for line in f if line.strip()]
        service_tasks = bpmn_parser.parse_files(file_paths)
    else:
        service_tasks = bpmn_parser.parse_directory('path/to/bpmn/files')  # Update the path as needed

    if not service_tasks:
        print("No BPMN files to process.")
        return


    # Load configuration
    # config = Config('config.yaml')
    #
    # # Parse BPMN files
    # bpmn_parser = BPMNParser()
    # service_tasks = bpmn_parser.parse_directory('bpmn_files')

        # Rest of the code remains the same
    # Validate service tasks
    validator = Validator(config)
    validation_results = validator.validate(service_tasks)

    # Generate report
    reporter = Reporter(config)
    reporter.generate_report(validation_results)

if __name__ == '__main__':
    main()
