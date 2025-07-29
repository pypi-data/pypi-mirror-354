import os
import sys

import pytest
import crestic

import builtins

testroot = os.path.dirname(__file__)


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    monkeypatch.delitem(os.environ, "CRESTIC_CONFIG_FILE", raising=False)
    monkeypatch.delitem(os.environ, "CRESTIC_CONFIG_PATHS", raising=False)
    monkeypatch.delitem(os.environ, "CRESTIC_DRYRUN", raising=False)
    monkeypatch.delitem(os.environ, "B2_ACCOUNT_ID", raising=False)
    monkeypatch.delitem(os.environ, "B2_ACCOUNT_KEY", raising=False)


@pytest.fixture(autouse=True)
def mock_call(mocker):
    mocker.patch("os.execvpe")
    mocker.patch("os.chdir")


@pytest.fixture
def mock_print(mocker):
    mocker.patch("builtins.print")


@pytest.fixture()
def conffile():
    return [testroot + "/crestic.cfg", testroot + "/overloading.cfg"]


@pytest.fixture(params=[True, False])
def dryrun(monkeypatch, clean_env, request):
    if request.param:
        monkeypatch.setitem(os.environ, "CRESTIC_DRYRUN", "1")
        return None
    else:
        return True


@pytest.fixture(params=[True, False])
def environ(monkeypatch, request):
    if request.param:
        return None
    else:
        return os.environ


@pytest.fixture(params=[True, False], autouse=True)
def mock_parse_intermixed_args(request, monkeypatch):
    if request.param:
        if sys.version_info < (3, 7):
            pytest.skip("requires python3.7 or higher")

        import argparse

        monkeypatch.delattr(argparse.ArgumentParser, "parse_intermixed_args")

    return request.param


def test_plain_backup(conffile, environ):
    crestic.main(["plain", "backup"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "bla", "/home/user"],
        env=os.environ,
    )


def test_plain_forget(conffile, environ):
    crestic.main(["plain", "forget"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "forget", "--exclude-file", "bla"],
        env=os.environ,
    )


def test_boolean(conffile, environ):
    crestic.main(["boolean", "backup"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "bla", "--quiet", "/home/user"],
        env=os.environ,
    )


def test_emptystring(conffile, environ):
    crestic.main(["emptystring", "backup"], conffile=conffile, environ=environ)

    os.execvpe.assert_called_once_with(
        "restic",
        [
            "restic",
            "backup",
            "--exclude-file",
            "bla",
            "--empty",
            "",
            "--noval",
            "/home/user",
        ],
        env=os.environ,
    )


def test_singlechar(conffile, environ):
    crestic.main(["singlechar", "backup"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "bla", "-r", "repo-url", "/home/user"],
        env=os.environ,
    )


def test_multivals(conffile, environ):
    crestic.main(["multivals", "backup"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        "restic",
        [
            "restic",
            "backup",
            "--exclude-file",
            "bla",
            "--exclude",
            "config.py",
            "--exclude",
            "passwords.txt",
            "/home/user",
        ],
        env=os.environ,
    )


def test_overloaded(conffile, environ):
    crestic.main(["overloaded", "backup"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "overloaded", "/home/user"],
        env=os.environ,
    )


def test_overloaded2(conffile, environ):
    crestic.main(["overloaded2", "backup"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "overloaded2", "/home/user"],
        env=os.environ,
    )


def test_overloadedargs(conffile, environ):
    crestic.main(
        ["plain", "backup", "--exclude-file", "foo"], conffile=conffile, environ=environ
    )
    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "foo", "/home/user"],
        env=os.environ,
    )


def test_multipleargs(conffile, environ):
    crestic.main(
        ["plain", "backup", "--exclude-file", "foo", "--exclude-file", "bar"],
        conffile=conffile,
        environ=environ,
    )
    os.execvpe.assert_called_once_with(
        "restic",
        [
            "restic",
            "backup",
            "--exclude-file",
            "foo",
            "--exclude-file",
            "bar",
            "/home/user",
        ],
        env=os.environ,
    )


def test_extraargs(conffile, environ):
    crestic.main(["plain", "backup", "--quiet"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "bla", "--quiet", "/home/user"],
        env=os.environ,
    )


def test_environ(conffile, environ):
    crestic.main(["environ", "backup"], conffile=conffile, environ=environ)

    environ = dict(os.environ)
    environ.update(
        {
            "B2_ACCOUNT_ID": "testid",
            "B2_ACCOUNT_KEY": "testkey",
        }
    )

    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "bla", "/home/user"],
        env=environ,
    )


@pytest.fixture
def environ_testkey(monkeypatch):
    monkeypatch.setitem(os.environ, "TESTKEY", "asd")


def test_environ_expand(conffile, environ_testkey, environ, monkeypatch):
    crestic.main(["environ_expand", "backup"], conffile=conffile, environ=environ)

    environ = dict(os.environ)
    environ.update(
        {
            "B2_ACCOUNT_ID": "testid",
            "B2_ACCOUNT_KEY": "asd",
        }
    )

    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "bla", "/home/user"],
        env=environ,
    )


def test_dryrun(mock_print, dryrun, conffile, environ):
    retval = crestic.main(
        ["environ", "backup"], dryrun=dryrun, conffile=conffile, environ=environ
    )

    os.execvpe.assert_not_called()
    builtins.print.assert_called_with(
        "    Expanded command:", '"restic" "backup" "--exclude-file" "bla" "/home/user"'
    )
    assert retval == 1


def test_invalid(mock_print):
    with pytest.raises(SystemExit):
        crestic.main(["@nas", "backup"])

    os.execvpe.assert_not_called()


def test_expanded_tilde(conffile, environ):
    crestic.main(["plain", "backup", "~"], conffile=conffile, environ=environ)

    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "bla", os.path.expanduser("~")],
        env=os.environ,
    )


def test_expanded_variable(conffile, environ):
    crestic.main(["plain", "backup", "$HOME"], conffile=conffile, environ=environ)

    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "bla", os.path.expandvars("$HOME")],
        env=os.environ,
    )


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_intermixed(conffile, environ, mock_parse_intermixed_args):
    if mock_parse_intermixed_args:
        pytest.skip()

    crestic.main(
        ["plain", "restore", "--include", "path space", "--target", ".", "asd"],
        conffile=conffile,
        environ=environ,
    )
    os.execvpe.assert_called_once_with(
        "restic",
        [
            "restic",
            "restore",
            "--exclude-file",
            "bla",
            "--include",
            "path space",
            "--target",
            ".",
            "asd",
        ],
        env=os.environ,
    )


@pytest.mark.skipif(sys.version_info >= (3, 7), reason="requires python3.6 or lower")
def test_intermixed_error(conffile, environ, mock_parse_intermixed_args):
    if not mock_parse_intermixed_args:
        pytest.skip()

    with pytest.raises(SystemExit):
        crestic.main(
            ["plain", "restore", "--include", "path space", "--target", ".", "asd"],
            conffile=conffile,
            environ=environ,
        )


def test_overloaded_config(conffile, environ):
    crestic.main(["overloaded_config", "backup"], conffile=conffile, environ=environ)

    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "valid", "/home/user"],
        env=os.environ,
    )


def test_deprecated_arguments(conffile, environ):
    """The use of arguments: is invalid now, this test reproduces the resulting broken behaviour

    Use _arguments: instead.
    """
    crestic.main(["deprecated-arguments", "backup"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        "restic",
        [
            "restic",
            "backup",
            "--exclude-file",
            "bla",
            "--arguments",
            "/home/user",
            "/home/user",
        ],
        env=os.environ,
    )


def test_workdir_config(conffile, environ):
    crestic.main(["workdir", "backup"], conffile=conffile, environ=environ)

    os.chdir.assert_called_once_with("/foo/bar")
    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "bla", "/home/user"],
        env=os.environ,
    )


def test_workdir2_config(conffile, environ):
    crestic.main(["workdir2", "backup"], conffile=conffile, environ=environ)

    os.chdir.assert_called_once_with(os.path.expandvars("$HOME") + "/foo/bar")
    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "bla", "/home/user"],
        env=os.environ,
    )


def test_workdir3_config(conffile, environ):
    crestic.main(["workdir3", "backup"], conffile=conffile, environ=environ)

    os.chdir.assert_called_once_with("foo")
    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "bla", "/home/user"],
        env=os.environ,
    )


def test_command_config(conffile, environ):
    crestic.main(["command", "alias"], conffile=conffile, environ=environ)

    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "bla", "/home/user"],
        env=os.environ,
    )


def test_interpolated_config(conffile, environ):
    crestic.main(["interpolated", "backup"], conffile=conffile, environ=environ)

    os.execvpe.assert_called_once_with(
        "restic",
        [
            "restic",
            "backup",
            "--exclude-file",
            "valid",
            "--exclude-file",
            "newfile",
            "/home/user",
        ],
        env=os.environ,
    )


def test_interpolation_envvar(conffile, environ):
    crestic.main(["interpolation-envvar", "backup"], conffile=conffile, environ=environ)

    os.execvpe.assert_called_once_with(
        "restic",
        ["restic", "backup", "--exclude-file", "bla", os.path.expandvars("$HOME")],
        env=os.environ,
    )
