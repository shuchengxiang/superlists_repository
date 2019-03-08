from fabric.api import run, env, hosts
from fabric.context_managers import settings

env.passwords = {
    'scx@172.16.207.51:22': '123456',
}


@hosts('172.16.207.51')
def host_os_type():
    run('uname -a')


def _get_manage_dot_py(host):
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'


def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'scx@{host}'):
        run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'scx@{host}'):
        session_key = run(f'{manage_dot_py} create_session email={email}')
        return session_key.strip()
