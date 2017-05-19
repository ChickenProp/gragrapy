def pytest_addoption(parser):
    parser.addoption('--accept-plots', action='store_true',
        help="Accept plots as comparison standards for future changes")
    parser.addoption('--show-plots', action='store_true',
        help="Show plots even if they haven't changed since last --accept-plots")

def pytest_generate_tests(metafunc):
    if 'accept_plots' in metafunc.fixturenames:
        metafunc.parametrize('accept_plots',
                             [metafunc.config.option.accept_plots])
    if 'show_plots' in metafunc.fixturenames:
        metafunc.parametrize('show_plots',
                             [metafunc.config.option.show_plots])
