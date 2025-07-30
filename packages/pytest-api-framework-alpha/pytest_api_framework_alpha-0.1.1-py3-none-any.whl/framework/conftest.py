import os
import re
import sys
import copy
import inspect
import platform
import importlib
import traceback
from pathlib import Path
from urllib.parse import urljoin

import retry
import allure
import pytest
from box import Box
from itertools import groupby
from framework.utils.log_util import logger
from framework.utils.yaml_util import YamlUtil
from framework.utils.encrypt import RsaByPubKey
from framework.utils.teams_util import TeamsUtil
from framework.utils.common import generate_2fa_code, snake_to_pascal, get_apps
from framework.exit_code import ExitCode
from framework.http_client import HttpClient
from framework.render_data import RenderData
from framework.allure_report import generate_report
from framework.global_attribute import CONTEXT, CONFIG
from config.settings import DATA_DIR, CASES_DIR, ROOT_DIR

test_results = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
# 获取当前系统的文件分隔符
file_separator = os.sep

# 判断用例是否需要被跳过
should_skip = False
all_app = get_apps()


def pytest_configure(config):
    """
    初始化时被调用，可以用于设置全局状态或配置
    :param config:
    :return:
    """

    for app in all_app:
        # 将所有app对应环境的基础测试数据加到全局
        CONTEXT.set_from_yaml(f"config/{app}/context.yaml", CONTEXT.env, app)
        # 将所有app对应环境的中间件配置加到全局
        CONFIG.set_from_yaml(f"config/{app}/config.yaml", CONTEXT.env, app)
    CONTEXT.set(key="all_app", value=all_app)
    CONTEXT.init_test_case_data_dict()
    sys.path.append(CASES_DIR)


def find_data_path_by_case(app, case_file_name):
    """
    基于case文件名称查找与之对应的yml文件路径
    :param app:
    :param case_file_name:
    :return:
    """
    for file_path in Path(os.path.join(DATA_DIR, app)).rglob(f"{case_file_name}.y*"):
        if file_path:
            return file_path


def __init_allure(params):
    """设置allure中case的 title, description, level"""
    case_level_map = {
        "p0": allure.severity_level.BLOCKER,
        "p1": allure.severity_level.CRITICAL,
        "p2": allure.severity_level.NORMAL,
        "p3": allure.severity_level.MINOR,
        "p4": allure.severity_level.TRIVIAL,
    }
    allure.dynamic.title(params.get("title"))
    allure.dynamic.description(params.get("describe"))
    allure.dynamic.severity(case_level_map.get(params.get("level")))
    allure.dynamic.feature(params.get("module"))
    allure.dynamic.story(params.get("describe"))


def pytest_generate_tests(metafunc):
    """
    生成（多个）对测试函数的参数化调用
    :param metafunc:
    :return:
    """
    # 获取测试函数所属的模块
    module = metafunc.module
    # 获取模块的文件路径
    class_path = os.path.abspath(module.__file__)
    root_path = ROOT_DIR + file_separator
    class_id = class_path.replace(root_path, "").replace(file_separator, '.')
    # 获取测试函数名
    function_name = metafunc.function.__name__
    # 构建全路径
    full_id = f"{class_id}::{function_name}"

    # print(f"测试用例全路径: {full_id}")
    # 获取当前待执行用例的文件名
    module_name = metafunc.module.__name__.split('.')[-1]
    # 获取当前待执行用例的函数名
    func_name = metafunc.function.__name__
    # 获取测试用例所属app
    belong_app = Path(class_path).relative_to(CASES_DIR).parts[0]
    # 获取当前用例对应的测试数据路径
    data_path = find_data_path_by_case(belong_app, module_name)

    if not data_path:
        logger.error(f"未找到{metafunc.module.__file__}对应的测试数据文件")
        traceback.print_exc()
        pytest.exit(ExitCode.CASE_YAML_NOT_EXIST)
    test_data = YamlUtil(data_path).load_yml()
    # 测试用例公共数据
    case_common = test_data.get("case_common")
    # 标记用例是否跳过
    metafunc.function.ignore = case_common.get("ignore")

    scenario_list = case_common.get('scenarios')

    test_case_datas = []

    if scenario_list is None:
        test_case_datas = [{'casedata': {}}]
    else:
        for scenario in scenario_list:
            if hasattr(CONTEXT, "mark"):
                if scenario.get('scenario') is not None and str(scenario.get('scenario').get('flag')) == CONTEXT.mark:
                    test_case_datas.append({'casedata': scenario.get('scenario').get('data')})
            else:
                if scenario.get('scenario') is not None and scenario.get('scenario').get('data') is not None:
                    test_case_datas.append({'casedata': scenario.get('scenario').get('data')})

        if len(scenario_list) == 0:
            test_case_datas = [{'casedata': {}}]

    case_data_list = []
    ids = []
    case_suite_index = 0

    test_case_data_dict = dict()

    # 是否是@test_suite_setup标识的setup方法
    is_test_setup = 'test_setup' in metafunc.definition.keywords
    is_test_teardown = 'test_teardown' in metafunc.definition.keywords
    if is_test_setup or is_test_teardown:
        for test_case_data in test_case_datas:
            case_suite_index += 1
            test_case_data_dict[f'{full_id}#{case_suite_index}'] = test_case_data
            case_data_list.append(test_case_data)
            ids.append(f'{full_id}#{str(case_suite_index)}')

    else:

        for test_case_data in test_case_datas:
            case_suite_index += 1
            test_case_data_dict[f'{full_id}#{case_suite_index}'] = test_case_data

            # 测试用例数据
            case_data = test_data.get(func_name)

            if not is_test_setup and not case_data:
                logger.error(f"未找到用例{func_name}对应的数据")
                pytest.exit(ExitCode.CASE_DATA_NOT_EXIST)

            if case_data.get("request") is None:
                case_data["request"] = dict()
            if case_data.get("request").get("headers") is None:
                case_data["request"]["headers"] = dict()

            # 合并测试数据
            case_data.setdefault("module", case_common.get("module"))
            case_data.setdefault("describe", case_common.get("describe"))
            case_data["_belong_app"] = belong_app

            if case_data.get("request").get("url") is not None or case_common.get("url") is not None:
                # 是一个带请求的case 反之 表示这条case不是一个带请求的case
                domain = CONTEXT.get(key="domain", app=belong_app)
                domain = domain if domain.startswith("http") else f"https://{domain}"
                url = case_data.get("request").get("url")
                if url.startswith('${'):
                    placeholder = url[2:len(url) - 1]
                    actual_url = CONTEXT.get(key=placeholder, app=belong_app)
                    if actual_url:
                        url = actual_url
                method = case_data.get("request").get("method")
                if not url:
                    if not case_common.get("url"):
                        logger.error(f"测试数据request中缺少必填字段: url", case_data)
                        pytest.exit(ExitCode.YAML_MISSING_FIELDS)
                    case_data["request"]["url"] = urljoin(domain, case_common.get("url"))
                else:
                    case_data["request"]["url"] = urljoin(domain, url)

                if not method:
                    if not case_common.get("method"):
                        logger.error(f"测试数据request中缺少必填字段: method", case_data)
                        pytest.exit(ExitCode.YAML_MISSING_FIELDS)
                    case_data["request"]["method"] = case_common.get("method")

            for key in ["title"]:
                if key not in case_data:
                    logger.error(f"测试数据{func_name}中缺少必填字段: {key}", case_data)
                    pytest.exit(ExitCode.YAML_MISSING_FIELDS)

            # 给用例打order标记
            if case_data.get("order", None):
                metafunc.function.order = int(case_data.get("order"))
            else:
                metafunc.function.order = None

            # 给用例打mark标记
            if case_data.get("mark", None):
                metafunc.function.marks = [case_data.get("mark"), case_data.get("level")]
            else:
                metafunc.function.marks = [case_data.get("level")]

            case_data_list.append(case_data)
            ids.append(f'{full_id}#{case_suite_index}')

    CONTEXT.set(key=f'{full_id}#test_case_datas', value=test_case_data_dict)

    metafunc.parametrize("data", case_data_list, ids=ids, scope='function')


@pytest.hookimpl
def pytest_runtest_setup(item):
    allure.dynamic.sub_suite(item.allure_suite_mark)


def pytest_collection_modifyitems(items):
    # 重新排序
    new_items = sort(items)
    # Demo: new_items = [items[0],items[2],items[1],items[3]]
    items[:] = new_items
    for item in items:
        # 用例打标记
        try:
            marks = item.function.marks
            for mark in marks:
                item.add_marker(mark)
            # 用例排序
            order = item.function.order
            if order:
                item.add_marker(pytest.mark.order(order))
        except Exception:  # 忽略test_setup,test_teardown方法
            pass


def __get_group_key__(item):
    return '::'.join(item.nodeid.split('::')[:2])


def sort(case_items):
    # 按测试类全路径分类,同一个类文件的用例归集到一起
    # 使用 groupby 函数进行分组
    item_group_list = [list(group) for _, group in groupby(case_items, key=__get_group_key__)]

    all_item_list = []
    clase_id = None
    for items in item_group_list:
        # 找出被test_setup标记的方法
        custom_scope_setup_items = [item for item in items if 'test_setup' in item.keywords]
        custom_scope_teardown_items = [item for item in items if 'test_teardown' in item.keywords]
        # 未被test_setup/test_teardown 标记的test方法
        non_custom_scope_items = [item for item in items if
                                  'test_setup' not in item.keywords and 'test_teardown' not in item.keywords]
        item_list = []
        # 用例的组数
        case_suite_num = 0
        # 生成每个组当前的索引
        ori_name_temp = None
        ori_name_list = []

        for item in non_custom_scope_items:
            clase_id = item.cls.__name__
            original_name = item.originalname

            if ori_name_temp is None or ori_name_temp == original_name:
                ori_name_temp = original_name
                case_suite_num += 1
                ori_name_list.append([original_name, item])
            else:
                break

        # 根据组数 创建各组的数组 并插入第一个case
        case_dict = dict()
        for i in range(case_suite_num):
            item = ori_name_list[i][1]
            id = item.callspec.id

            first_part = id.split('#', 1)[-1]
            index = first_part.split(']')[0]
            case_dict[index] = [item]

        new_start_index = case_suite_num
        # 以new_start_index为起点 重新遍历items
        for i in range(new_start_index, len(non_custom_scope_items)):
            item = non_custom_scope_items[i]
            id = item.callspec.id
            first_part = id.split('#', 1)[-1]
            index = first_part.split(']')[0]
            case_dict.get(index).append(item)

        setup_dict = dict()
        for item in custom_scope_setup_items:
            id = item.callspec.id
            first_part = id.split('#', 1)[-1]
            index = first_part.split(']')[0]
            setup_dict[index] = [item]

        teardown_dict = dict()
        for item in custom_scope_teardown_items:
            id = item.callspec.id
            first_part = id.split('#', 1)[-1]
            index = first_part.split(']')[0]
            teardown_dict[index] = [item]

        index = 0
        for id in case_dict:
            index += 1
            if setup_dict:
                setup_item_list = setup_dict.get(id)
                for item in setup_item_list:
                    allure_suite_mark = f'{clase_id}#{index}'
                    setattr(item, 'allure_suite_mark', allure_suite_mark)

                item_list += setup_item_list

            case_item_list = case_dict.get(id)
            for item in case_item_list:
                allure_suite_mark = f'{clase_id}#{index}'
                setattr(item, 'allure_suite_mark', allure_suite_mark)
            item_list += case_item_list

            if teardown_dict:
                teardown_item_list = teardown_dict.get(id)
                for item in teardown_item_list:
                    allure_suite_mark = f'{clase_id}#{index}'
                    setattr(item, 'allure_suite_mark', allure_suite_mark)
                item_list += teardown_item_list

        all_item_list += item_list

    return all_item_list


def pytest_runtest_call(item):
    """
    模版渲染，运行用例
    :param item:
    :return:
    """
    # 是否是test—setup 或 test-teardown方法
    is_around_function = item.get_closest_marker("test_setup") or item.get_closest_marker("test_teardown")
    if not is_around_function:
        if item.function.ignore:
            # 如果是普通方法 而且由于之前步骤出错则skiped
            pytest.skip('skiped')

    id = item.callspec.id

    # 支持本地调试的标记
    CONTEXT.set(key='run#index', value=id.split('::')[1])

    # 获取参数化数据 放入上下文中
    full_id = id.split('#')[0]
    test_case_datas = CONTEXT.get(key=f'{full_id}#test_case_datas')
    CONTEXT.set_from_dict(test_case_datas.get(id))

    # 获取原始测试数据
    origin_data = item.funcargs.get("data")
    # 深拷贝这份数据
    deep_copied_origin_data = copy.deepcopy(origin_data)
    item.funcargs["origin_data"] = Box(origin_data)

    __init_allure(origin_data)
    logger.info(f"执行用例: {item.nodeid}")
    # 对原始请求数据进行渲染替换
    rendered_data = RenderData(deep_copied_origin_data).render()
    # 测试用例函数添加参数data
    http = item.funcargs.get("http")
    item.funcargs["data"] = Box(rendered_data)
    item.funcargs["belong_app"] = origin_data.get("_belong_app")
    item.funcargs["config"] = CONFIG
    item.funcargs["context"] = CONTEXT
    if item.cls:
        item.cls.http = http
        item.cls.data = Box(rendered_data)
        item.cls.origin_data = Box(origin_data)
        item.cls.belong_app = origin_data.get("_belong_app")
        item.cls.context = CONTEXT
        item.cls.config = config

    # 获取测试函数体内容
    func_source = re.sub(r'(?<!["\'])#.*', '', inspect.getsource(item.function))
    # 校验测试用例中是否有断言
    if 'test_setup' not in item.keywords and 'test_teardown' not in item.keywords and "assert" not in func_source:
        logger.error(f"测试方法:{item.originalname}缺少断言")
        pytest.exit(ExitCode.MISSING_ASSERTIONS)

    # # 检查函数体内容是否包含语句self.request，如果没有则自动发送请求
    # if "self.request" not in func_source:
    #     # 测试用例函数添加参数response
    #     response = client.request(rendered_data)
    #     item.funcargs["response"] = response
    #     if item.cls:
    #         item.cls.response = response


def pytest_runtest_logreport(report):
    """收集测试结果"""
    if report.when == "call":  # 确保是测试调用阶段（忽略setup和teardown）
        test_results["total"] += 1
        if report.passed:
            test_results["passed"] += 1
        elif report.failed:
            test_results["failed"] += 1
        elif report.skipped:
            test_results["skipped"] += 1


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 获取测试报告
    outcome = yield
    report = outcome.get_result()

    # 如果测试失败并且是执行阶段
    if report.when == "call" and report.failed:
        # 获取断言失败的消息
        logger.error(f"断言失败: {report.longrepr.reprcrash}")
        # 用于控制失败步骤后是否继续的标志
        failStepContinuationFlag = item.callspec.params.get('data').get('failStepContinuationFlag')

        global should_skip
        if failStepContinuationFlag is None:
            should_skip = True
        else:
            if failStepContinuationFlag == True:
                should_skip = False
            else:
                should_skip = True


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """在 pytest 结束后修改统计数据或添加自定义报告"""
    stats = terminalreporter.stats
    # 统计各种测试结果
    passed = len(stats.get("passed", []))
    failed = len(stats.get("failed", []))
    skipped = len(stats.get("skipped", []))
    total = passed + failed + skipped
    try:
        pass_rate = round(passed / (total - skipped) * 100, 2)
    except ZeroDivisionError:
        pass_rate = 0
    # 打印自定义统计信息
    terminalreporter.write("\n============ 执行结果统计 ============\n", blue=True, bold=True)
    terminalreporter.write(f"执行用例总数: {passed + failed + skipped}\n", bold=True)
    terminalreporter.write(f"通过用例数: {passed}\n", green=True, bold=True)
    terminalreporter.write(f"失败用例数: {failed}\n", red=True, bold=True)
    terminalreporter.write(f"跳过用例数: {skipped}\n", yellow=True, bold=True)
    terminalreporter.write(f"用例通过率: {pass_rate}%\n", green=True, bold=True)
    terminalreporter.write("====================================\n", blue=True, bold=True)
    # 生成allure测试报告
    generate_report()


@pytest.fixture(autouse=True)
def response():
    response = None
    yield response


@pytest.fixture(autouse=True)
def data():
    data: dict = dict()
    yield data


@pytest.fixture(autouse=True)
def origin_data():
    origin_data: dict = dict()
    yield origin_data


@pytest.fixture(autouse=True)
def belong_app():
    app = None
    yield app


@pytest.fixture(autouse=True)
def config():
    config = None
    yield config


@pytest.fixture(autouse=True)
def context():
    context = None
    yield context


class Http(object):
    pass


@retry.retry(tries=3, delay=1)
@pytest.fixture(scope="session", autouse=True)
def http():
    module = importlib.import_module("conftest")
    try:
        for app in all_app:
            setattr(Http, app, getattr(module, f"{snake_to_pascal(app)}Login")(app))
        return Http
    except Exception as e:
        logger.error(f"登录{app}异常:{e}")
        traceback.print_exc()
        pytest.exit(ExitCode.LOGIN_ERROR)
        return None
