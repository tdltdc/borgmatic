import logging

import pytest
from flexmock import flexmock

from borgmatic.borg import info as module

from ..test_verbosity import insert_logging_mock


def test_display_archives_info_calls_borg_with_parameters():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags').with_args('repo', 'repo').and_return(
        ('--repo', 'repo')
    )
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(())
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'info', '--repo', 'repo'),
        output_log_level=logging.WARNING,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.display_archives_info(
        repository='repo',
        storage_config={},
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive=None, json=False, prefix=None),
    )


def test_display_archives_info_without_borg_features_calls_borg_without_repo_flag():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(())
    flexmock(module.feature).should_receive('available').and_return(False)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'info', 'repo'),
        output_log_level=logging.WARNING,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.display_archives_info(
        repository='repo',
        storage_config={},
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive=None, json=False, prefix=None),
    )


def test_display_archives_info_with_log_info_calls_borg_with_info_parameter():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags').with_args('repo', 'repo').and_return(
        ('--repo', 'repo')
    )
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(())
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'info', '--info', '--repo', 'repo'),
        output_log_level=logging.WARNING,
        borg_local_path='borg',
        extra_environment=None,
    )
    insert_logging_mock(logging.INFO)
    module.display_archives_info(
        repository='repo',
        storage_config={},
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive=None, json=False, prefix=None),
    )


def test_display_archives_info_with_log_info_and_json_suppresses_most_borg_output():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags').with_args('repo', 'repo').and_return(
        ('--repo', 'repo')
    )
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(('--json',))
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'info', '--json', '--repo', 'repo'),
        output_log_level=None,
        borg_local_path='borg',
        extra_environment=None,
    ).and_return('[]')

    insert_logging_mock(logging.INFO)
    json_output = module.display_archives_info(
        repository='repo',
        storage_config={},
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive=None, json=True, prefix=None),
    )

    assert json_output == '[]'


def test_display_archives_info_with_log_debug_calls_borg_with_debug_parameter():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags').with_args('repo', 'repo').and_return(
        ('--repo', 'repo')
    )
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(())
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'info', '--debug', '--show-rc', '--repo', 'repo'),
        output_log_level=logging.WARNING,
        borg_local_path='borg',
        extra_environment=None,
    )
    insert_logging_mock(logging.DEBUG)

    module.display_archives_info(
        repository='repo',
        storage_config={},
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive=None, json=False, prefix=None),
    )


def test_display_archives_info_with_log_debug_and_json_suppresses_most_borg_output():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags').with_args('repo', 'repo').and_return(
        ('--repo', 'repo')
    )
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(('--json',))
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'info', '--json', '--repo', 'repo'),
        output_log_level=None,
        borg_local_path='borg',
        extra_environment=None,
    ).and_return('[]')

    insert_logging_mock(logging.DEBUG)
    json_output = module.display_archives_info(
        repository='repo',
        storage_config={},
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive=None, json=True, prefix=None),
    )

    assert json_output == '[]'


def test_display_archives_info_with_json_calls_borg_with_json_parameter():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags').with_args('repo', 'repo').and_return(
        ('--repo', 'repo')
    )
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(('--json',))
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'info', '--json', '--repo', 'repo'),
        output_log_level=None,
        borg_local_path='borg',
        extra_environment=None,
    ).and_return('[]')

    json_output = module.display_archives_info(
        repository='repo',
        storage_config={},
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive=None, json=True, prefix=None),
    )

    assert json_output == '[]'


def test_display_archives_info_with_archive_calls_borg_with_glob_archives_parameter():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags').with_args('repo', 'repo').and_return(
        ('--repo', 'repo')
    )
    flexmock(module.flags).should_receive('make_flags').with_args(
        'glob-archives', 'archive'
    ).and_return(('--glob-archives', 'archive'))
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(())
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'info', '--repo', 'repo', '--glob-archives', 'archive'),
        output_log_level=logging.WARNING,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.display_archives_info(
        repository='repo',
        storage_config={},
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive='archive', json=False, prefix=None),
    )


def test_display_archives_info_with_archive_and_without_borg_features_calls_borg_with_repo_archive_parameter():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(())
    flexmock(module.feature).should_receive('available').and_return(False)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'info', 'repo::archive'),
        output_log_level=logging.WARNING,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.display_archives_info(
        repository='repo',
        storage_config={},
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive='archive', json=False, prefix=None),
    )


def test_display_archives_info_with_local_path_calls_borg_via_local_path():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags').with_args('repo', 'repo').and_return(
        ('--repo', 'repo')
    )
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(())
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg1', 'info', '--repo', 'repo'),
        output_log_level=logging.WARNING,
        borg_local_path='borg1',
        extra_environment=None,
    )

    module.display_archives_info(
        repository='repo',
        storage_config={},
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive=None, json=False, prefix=None),
        local_path='borg1',
    )


def test_display_archives_info_with_remote_path_calls_borg_with_remote_path_parameters():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags').with_args('repo', 'repo').and_return(
        ('--repo', 'repo')
    )
    flexmock(module.flags).should_receive('make_flags').with_args(
        'remote-path', 'borg1'
    ).and_return(('--remote-path', 'borg1'))
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(())
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'info', '--remote-path', 'borg1', '--repo', 'repo'),
        output_log_level=logging.WARNING,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.display_archives_info(
        repository='repo',
        storage_config={},
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive=None, json=False, prefix=None),
        remote_path='borg1',
    )


def test_display_archives_info_with_lock_wait_calls_borg_with_lock_wait_parameters():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags').with_args('repo', 'repo').and_return(
        ('--repo', 'repo')
    )
    flexmock(module.flags).should_receive('make_flags').with_args('lock-wait', 5).and_return(
        ('--lock-wait', '5')
    )
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(())
    storage_config = {'lock_wait': 5}
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'info', '--lock-wait', '5', '--repo', 'repo'),
        output_log_level=logging.WARNING,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.display_archives_info(
        repository='repo',
        storage_config=storage_config,
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive=None, json=False, prefix=None),
    )


def test_display_archives_info_with_prefix_calls_borg_with_glob_archives_parameters():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags').with_args('repo', 'repo').and_return(
        ('--repo', 'repo')
    )
    flexmock(module.flags).should_receive('make_flags').with_args(
        'glob-archives', 'foo*'
    ).and_return(('--glob-archives', 'foo*'))
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(())
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'info', '--glob-archives', 'foo*', '--repo', 'repo'),
        output_log_level=logging.WARNING,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.display_archives_info(
        repository='repo',
        storage_config={},
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive=None, json=False, prefix='foo'),
    )


@pytest.mark.parametrize('argument_name', ('glob_archives', 'sort_by', 'first', 'last'))
def test_display_archives_info_passes_through_arguments_to_borg(argument_name):
    flag_name = f"--{argument_name.replace('_', ' ')}"
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags').with_args('repo', 'repo').and_return(
        ('--repo', 'repo')
    )
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(
        (flag_name, 'value')
    )
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'info', flag_name, 'value', '--repo', 'repo'),
        output_log_level=logging.WARNING,
        borg_local_path='borg',
        extra_environment=None,
    )

    module.display_archives_info(
        repository='repo',
        storage_config={},
        local_borg_version='2.3.4',
        info_arguments=flexmock(archive=None, json=False, prefix=None, **{argument_name: 'value'}),
    )
