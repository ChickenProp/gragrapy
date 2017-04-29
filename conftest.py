def pytest_addoption(parser):
    parser.addoption('--accept-plots', action='store_true',
        help="Accept plots as comparison standards for future changes")

def pytest_generate_tests(metafunc):
    if 'accept_plots' in metafunc.fixturenames:
        metafunc.parametrize('accept_plots',
                             [metafunc.config.option.accept_plots])
