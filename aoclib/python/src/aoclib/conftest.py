# TODO: Replace this with a pytest plugin
# from ward.hooks import hook
# from ward.config import Config
# from ward.testing import Test

# @hook
# def preprocess_tests(config: Config, collected_tests: list[Test]) -> None:  # pylint: disable=unused-argument
#     for test in collected_tests:
#         if test.module_name == "test_main":
#             # break if there is a module named `test_main` which is a year/day module in order to do sorting
#             break

#     else:
#         return  # pragma: no cover

#     collected_tests.sort(key=lambda k: k.description)