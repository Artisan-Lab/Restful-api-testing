import json
import sys

from foREST_setting import foRESTSetting
import argparse
from log.get_logging import Log
from entity.resource_pool import ResourcePool
from module.foREST_monitor.foREST_monitor import foRESTMonitor
from module.parser.open_api_parse.api_parser import *
from module.data_analysis.data_analysis import data_analysis
from module.testing.testing import TestingMonitor


if __name__ == "__main__":
    # command-line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--foREST_mode',
                            help='pure testing or data-based testing'
                                 f'(default pure testing)',
                            type=str, default="pure testing", required=False)
    arg_parser.add_argument('--log_type',
                            help='data-based testing argument, specific log type'
                                 'json or foREST(default json)',
                            type=str, default='json', required=False)
    arg_parser.add_argument('--log_path',
                            help='data-based testing argument: log absolute path, '
                                 'required if data-based testing',
                            type=str, required=False)
    arg_parser.add_argument('--time_budget',
                            help='Testing run time in hours '
                                 f'(default 1 hours)',
                            type=float, default=1, required=False)
    arg_parser.add_argument('--token',
                            help='User identification code'
                                 f'(default',
                            type=str, required=False)
    arg_parser.add_argument('--api_file_path',
                            help='The read path of the API documentation',
                            type=str, required=True)
    arg_parser.add_argument('--settings_file',
                            help='Custom user settings file path',
                            type=str, default='', required=False)
    arg_parser.add_argument('--target_ip',
                            help='service under testing ip',
                            type=str)
    arg_parser.add_argument('--dict_type',
                            help='rbtree or dict')
    args = arg_parser.parse_args()

    # convert the command-line arguments to a dict
    args_dict = vars(args)

    # combine settings from settings file to the command-line arguments
    if args.settings_file:
        try:
            setting_file = json.load(open(args.settings_file))
            args_dict.update(setting_file)
        except Exception as error:
            print(f"\n Argument Error::\n\t{error!s}")
            sys.exit(-1)

    # configure foREST setting and start monitor
    foREST_settings = foRESTSetting(args_dict)
    foREST_monitor = foRESTMonitor()

    # start time monitor
    foREST_monitor.create_time_monitor(foREST_settings.time_budget)
    foREST_monitor.start_time_monitor()

    # parsing API file
    APIListParser().parsing_api_file(foREST_settings.api_file_path)

    # Initialize the resource pool
    resource_pool = ResourcePool()
    foREST_monitor.resource_pool = resource_pool

    # api dependency analysis
    api_list_parser().foREST_dependency_analysis()
    api_list = api_list_parser().api_list
    foREST_monitor.api_list = api_list_parser().api_list

    # data analysis
    if foREST_settings.foREST_mode == "data-based testing":
        data_analysis_result = data_analysis(foREST_settings.log_type, foREST_settings.log_path, foREST_settings.dict_type)
        for api in data_analysis_result:
            for parameter in data_analysis_result[api]:
                data_analysis_result[api][parameter] = sorted(data_analysis_result[api][parameter].items(), key=lambda s:s[1], reverse=True)


        data_analysis_result_log = Log(f"data_analysis_{foREST_settings.dict_type}.json")
        data_analysis_result_log.save_json(data_analysis_result)

    testing_monitor = TestingMonitor(api_list_parser().root)
    testing_monitor.foREST_tree_based_bfs()
    api_log = Log("api_log.json")
    api_log.save_object(api_list)
    foREST_monitor.time_monitor.terminate()
    print(foREST_monitor.time_monitor.testing_time)
