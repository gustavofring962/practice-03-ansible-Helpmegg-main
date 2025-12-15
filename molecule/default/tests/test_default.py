import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_packages_installed(host):
    """
    Check if packages are installed
    """
    packages = ['nginx', 'python3', 'python3-pip', 'python3-venv']
    for pkg in packages:
        package = host.package(pkg)
        assert package.is_installed


def test_flask_app_service(host):
    """
    Check if Flask service is active
    """
    service = host.service('flask_app')
    assert service.is_enabled
    assert service.is_running


def test_nginx_service(host):
    """
    Check if Nginx service is active
    """
    service = host.service('nginx')
    assert service.is_enabled
    assert service.is_running


def test_flask_app_running(host):
    """
    Check if Flask responds to requests
    """
    cmd = host.run('curl -I http://localhost:8080/')
    assert 'Content-Type: image/gif' in cmd.stdout


def test_nginx_proxy(host):
    """
    Check if Nginx acts as proxy
    """
    cmd = host.run('curl -I http://localhost/')
    assert 'Content-Type: image/gif' in cmd.stdout


def test_static_image(host):
    """
    Check if image is accessible using Nginx
    """
    cmd = host.run('curl -I http://localhost/static/cat.gif')
    assert '200 OK' in cmd.stdout
