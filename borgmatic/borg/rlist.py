import logging

import borgmatic.logger
from borgmatic.borg import environment, feature, flags
from borgmatic.execute import execute_command, execute_command_and_capture_output

logger = logging.getLogger(__name__)


def resolve_archive_name(
    repository_path,
    archive,
    storage_config,
    local_borg_version,
    local_path='borg',
    remote_path=None,
):
    '''
    Given a local or remote repository path, an archive name, a storage config dict, a local Borg
    path, and a remote Borg path, simply return the archive name. But if the archive name is
    "latest", then instead introspect the repository for the latest archive and return its name.

    Raise ValueError if "latest" is given but there are no archives in the repository.
    '''
    if archive != 'latest':
        return archive

    lock_wait = storage_config.get('lock_wait', None)

    full_command = (
        (
            local_path,
            'rlist' if feature.available(feature.Feature.RLIST, local_borg_version) else 'list',
        )
        + flags.make_flags('remote-path', remote_path)
        + flags.make_flags('lock-wait', lock_wait)
        + flags.make_flags('last', 1)
        + ('--short',)
        + flags.make_repository_flags(repository_path, local_borg_version)
    )

    output = execute_command_and_capture_output(
        full_command, extra_environment=environment.make_environment(storage_config),
    )
    try:
        latest_archive = output.strip().splitlines()[-1]
    except IndexError:
        raise ValueError('No archives found in the repository')

    logger.debug(f'{repository_path}: Latest archive is {latest_archive}')

    return latest_archive


MAKE_FLAGS_EXCLUDES = ('repository', 'prefix', 'match_archives')


def make_rlist_command(
    repository_path,
    storage_config,
    local_borg_version,
    rlist_arguments,
    local_path='borg',
    remote_path=None,
):
    '''
    Given a local or remote repository path, a storage config dict, the local Borg version, the
    arguments to the rlist action, and local and remote Borg paths, return a command as a tuple to
    list archives with a repository.
    '''
    lock_wait = storage_config.get('lock_wait', None)

    return (
        (
            local_path,
            'rlist' if feature.available(feature.Feature.RLIST, local_borg_version) else 'list',
        )
        + (
            ('--info',)
            if logger.getEffectiveLevel() == logging.INFO and not rlist_arguments.json
            else ()
        )
        + (
            ('--debug', '--show-rc')
            if logger.isEnabledFor(logging.DEBUG) and not rlist_arguments.json
            else ()
        )
        + flags.make_flags('remote-path', remote_path)
        + flags.make_flags('lock-wait', lock_wait)
        + (
            (
                flags.make_flags('match-archives', f'sh:{rlist_arguments.prefix}*')
                if feature.available(feature.Feature.MATCH_ARCHIVES, local_borg_version)
                else flags.make_flags('glob-archives', f'{rlist_arguments.prefix}*')
            )
            if rlist_arguments.prefix
            else (
                flags.make_match_archives_flags(
                    rlist_arguments.match_archives or storage_config.get('match_archives'),
                    storage_config.get('archive_name_format'),
                    local_borg_version,
                )
            )
        )
        + flags.make_flags_from_arguments(rlist_arguments, excludes=MAKE_FLAGS_EXCLUDES)
        + flags.make_repository_flags(repository_path, local_borg_version)
    )


def list_repository(
    repository_path,
    storage_config,
    local_borg_version,
    rlist_arguments,
    local_path='borg',
    remote_path=None,
):
    '''
    Given a local or remote repository path, a storage config dict, the local Borg version, the
    arguments to the list action, and local and remote Borg paths, display the output of listing
    Borg archives in the given repository (or return JSON output).
    '''
    borgmatic.logger.add_custom_log_levels()
    borg_environment = environment.make_environment(storage_config)

    main_command = make_rlist_command(
        repository_path,
        storage_config,
        local_borg_version,
        rlist_arguments,
        local_path,
        remote_path,
    )

    if rlist_arguments.json:
        return execute_command_and_capture_output(main_command, extra_environment=borg_environment)
    else:
        execute_command(
            main_command,
            output_log_level=logging.ANSWER,
            borg_local_path=local_path,
            extra_environment=borg_environment,
        )
