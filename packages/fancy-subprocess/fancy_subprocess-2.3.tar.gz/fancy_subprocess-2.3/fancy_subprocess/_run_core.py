__all__ = [
    'run',
    'RunError',
    'RunResult',
]

import os
import subprocess
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from typing_extensions import Unpack

from fancy_subprocess._print import default_print, PrintFunction, silenced_print
from fancy_subprocess._run_param import AnyExitCode, check_run_params, RunParams, Success
from fancy_subprocess._utils import oslex_join, stringify_exit_code, value_or

@dataclass(kw_only=True, frozen=True)
class RunResult:
    """
    `fancy_subprocess.run()` and similar functions return a `RunResult` instance on success.

    `RunResult` has the following properties:
    - `exit_code: int` - Exit code of the finished process. (On Windows, this is a signed `int32` value, i.e. in the range of [-2<sup>31</sup>, 2<sup>31</sup>-1].)
    - `output: str` - Combination of the process's output on stdout and stderr.
    """

    exit_code: int = 0
    output: str = ''

@dataclass(kw_only=True, frozen=True)
class RunError(Exception):
    """
    `fancy_subprocess.run()` and similar functions raise `RunError` on error. There are two kinds of errors that result in a `RunError`:
    - If the requested command has failed, the `completed` property will be `True`, and the `exit_code` and `output` properties will be set.
    - If the command couldn't be run (eg. because the executable wasn't found), the `completed` property will be `False`, and the `oserror` property will be set to the `OSError` exception instance originally raised by the underlying `subprocess.Popen()` call.

    Calling `str()` on a `RunError` object returns a detailed one-line description of the error:
    - The failed command is included in the message.
    - If an `OSError` happened, its message is included in the message.
    - On Windows, if the exit code of the process is recognized as a known `NTSTATUS` error value, its name is included in the message, otherwise its hexadecimal representation is included (to make searching it on the internet easier).
    - On Unix systems, if the exit code represents a signal, its name is included in the message.

    `RunError` has the following properties:
    - `cmd: Sequence[str | Path]` - Original command passed to `fancy_subprocess.run()`.
    - `completed: bool` - `True` if the process completed (with an error), `False` if the underlying `subprocess.Popen()` call raised an OSError (eg. because it could not start the process).
    - `exit_code: int` - Exit code of the completed process. Raises `ValueError` if `completed` is `False`.
    - `output: str` - Combination of the process's output on stdout and stderr. Raises `ValueError` if `completed` is `False`.
    - `oserror: OSError` - The `OSError` raised by `subprocess.Popen()`. Raises `ValueError` if `completed` is `True`.
    """

    cmd: Sequence[str | Path]
    result: RunResult | OSError = RunResult()

    @property
    def completed(self) -> bool:
        return isinstance(self.result, RunResult)

    @property
    def exit_code(self) -> int:
        if isinstance(self.result, RunResult):
            return self.result.exit_code
        else:
            raise ValueError('...')

    @property
    def output(self) -> str:
        if isinstance(self.result, RunResult):
            return self.result.output
        else:
            raise ValueError('...')

    @property
    def oserror(self) -> OSError:
        if isinstance(self.result, OSError):
            return self.result
        else:
            raise ValueError('...')

    @property
    def message(self) -> str:
        if isinstance(self.result, RunResult):
            exit_code_str = stringify_exit_code(self.exit_code)
            if exit_code_str is not None:
                exit_code_comment = f' ({exit_code_str})'
            else:
                exit_code_comment = ''
            return f'Command failed with exit code {self.exit_code}{exit_code_comment}: {oslex_join(self.cmd)}'
        else:
            return f'Exception {type(self.result).__name__} with message "{str(self.result)}" was raised while trying to run command: {oslex_join(self.cmd)}'

    def __str__(self) -> str:
        return self.message

def run(
    cmd: Sequence[str | Path],
    *,
    print_message: Optional[PrintFunction] = None,
    print_output: Optional[PrintFunction] = None,
    **kwargs: Unpack[RunParams],
) -> RunResult:
    """
    An extended (and in some aspects, constrained) version of `subprocess.run()`. It runs a command and prints its output line-by-line using a customizable `print_output` function, while printing informational messages (eg. which command it is running) using a customizable `print_message` function.

    Key differences compared to `subprocess.run()`:
    - The command must be specified as a list, simply specifying a string is not allowed.
    - The command's stdout and stderr is always combined into a single stream. (Like `subprocess.run(stderr=STDOUT)`.)
    - The output of the command is always assumed to be textual, not binary. (Like `subprocess.run(text=True)`.)
    - The output of the command is always captured, but it is also immediately printed using `print_output`.
    - The exit code of the command is checked, and an exception is raised on failure, like `subprocess.run(check=True)`, but the list of exit codes treated as success is customizable, and the raised exception is `RunError` instead of `CalledProcessError`.
    - `OSError` is never raised, it gets converted to `RunError`.
    - `RunResult` is returned instead of `CompletedProcess` on success.

    Arguments (all of them except `cmd` are optional):
    - `cmd: Sequence[str | Path]` - Command to run. See `subprocess.run()`'s documentation for the interpretation of `cmd[0]`. It is recommended to use `fancy_subprocess.which()` to produce `cmd[0]`.
    - `print_message: Callable[[str], None]` - Function used to print informational messages. If unspecified or set to `None`, defaults to `fancy_subprocess.default_print`. Use `message_quiet=True` to disable printing informational messages.
    - `print_output: Callable[[str], None]` - Function used to print a line of the output of the command. If unspecified or set to `None`, defaults to `fancy_subprocess.default_print`. Use `output_quiet=True` to disable printing the command's output.
    - `message_quiet: bool` - If `True`, `print_message` is ignored, and no informational messages are printed. If unspecified or set to `None`, defaults to `False`.
    - `output_quiet: bool` - If `True`, `print_output` is ignored, and the command's output it not printed. If unspecified or set to `None`, defaults to `False`. Note that this parameter also affects the default value of `description`.
    - `description: str` - Description printed before running the command. If unspecified or set to `None`, defaults to `Running command: ...` when `output_quiet` is `False`, and `Running command (output silenced): ...` when `output_quiet` is `True`.
    - `success: Sequence[int] | AnyExitCode` - List of exit codes that should be considered successful. If set to `fancy_subprocess.ANY_EXIT_CODE`, then all exit codes are considered successful. If unspecified or set to `None`, defaults to `[0]`. Note that 0 is not automatically included in the list of successful exit codes, so if a list without 0 is specified, then the function will consider 0 a failure.
    - `flush_before_subprocess: bool` - If `True`, flushes both the standard output and error streams before running the command. If unspecified or set to `None`, defaults to `True`.
    - `trim_output_lines: bool` - If `True`, remove trailing whitespace from the lines of the output of the command before calling `print_output` and adding them to the `output` field of `RunResult`. If unspecified or set to `None`, defaults to `True`.
    - `max_output_size: int` - Maximum number of characters to be recorded in the `output` field of `RunResult`. If the command produces more than `max_output_size` characters, only the last `max_output_size` will be recorded. If unspecified or set to `None`, defaults to 10,000,000.
    - `retry: int` - Number of times to retry running the command on failure. Note that the total number of attempts is one greater than what's specified. (I.e. `retry=2` attempts to run the command 3 times.) If unspecified or set to `None`, defaults to 0.
    - `retry_initial_sleep_seconds: float` - Number of seconds to wait before retrying for the first time. If unspecified or set to `None`, defaults to 10.
    - `retry_backoff: float` - Factor used to increase wait times before subsequent retries. If unspecified or set to `None`, defaults to 2.
    - `env_overrides: Mapping[str, str]` - Dictionary used to set environment variables. Note that unline the `env` argument of `subprocess.run()`, `env_overrides` does not need to contain all environment variables, only the ones you want to add/modify compared to os.environ. If unspecified or set to `None`, defaults to empty dictionary, i.e. no change to the environment.
    - `cwd: str | Path` - If not `None`, change current working directory to `cwd` before running the command.
    - `encoding: str` - This encoding will be used to open stdout and stderr of the command. If unspecified or set to `None`, see default behaviour in `io.TextIOWrapper`'s documentation.
    - `errors: str` - This specifies how text decoding errors will be handled. (See possible options in `io.TextIOWrapper`'s documentation.) If unspecified or set to `None`, defaults to `replace`. Note that this differs from `io.TextIOWrapper`'s default behaviour, which is to use `strict`.
    - `replace_fffd_with_question_mark: bool` - Replace Unicode Replacement Character U+FFFD (`�`, usually introduced by `errors='replace'`) with ASCII question mark (`?`) in lines of the output of the command before calling `print_output` and adding them to the `output` field of `RunResult`. If unspecified or set to `None`, defaults to `True`.
    """

    check_run_params(**kwargs)

    message_quiet = value_or(kwargs.get('message_quiet'), False)
    output_quiet = value_or(kwargs.get('output_quiet'), False)
    if output_quiet:
        default_description = f'Running command (output silenced): {oslex_join(cmd)}'
    else:
        default_description = f'Running command: {oslex_join(cmd)}'
    description = value_or(kwargs.get('description'), default_description)
    success: Success = value_or(kwargs.get('success'), [0])
    flush_before_subprocess = value_or(kwargs.get('flush_before_subprocess'), True)
    trim_output_lines = value_or(kwargs.get('trim_output_lines'), True)
    max_output_size = value_or(kwargs.get('max_output_size'), 10*1000*1000)
    retry = value_or(kwargs.get('retry'), 0)
    retry_initial_sleep_seconds = value_or(kwargs.get('retry_initial_sleep_seconds'), 10)
    retry_backoff = value_or(kwargs.get('retry_backoff'), 2)
    env_overrides = value_or(kwargs.get('env_overrides'), dict())
    cwd = kwargs.get('cwd')
    encoding = kwargs.get('encoding')
    errors = value_or(kwargs.get('errors'), 'replace')
    replace_fffd_with_question_mark = value_or(kwargs.get('replace_fffd_with_question_mark'), True)

    if message_quiet:
        print_message = silenced_print
    else:
        print_message = value_or(print_message, default_print)

    if output_quiet:
        print_output = silenced_print
    else:
        print_output = value_or(print_output, default_print)

    env = dict(os.environ)
    if sys.platform=='win32':
        env.update((key.upper(), value) for key,value in env_overrides.items())
    else:
        env.update(env_overrides)

    def attempt_run() -> RunResult:
        print_message(description)

        if flush_before_subprocess:
            sys.stdout.flush()
            sys.stderr.flush()

        output = ''
        try:
            with subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, cwd=cwd, env=env, encoding=encoding, errors=errors) as proc:
                assert proc.stdout is not None # passing stdout=subprocess.PIPE guarantees this

                for line in iter(proc.stdout.readline, ''):
                    line = line.removesuffix('\n')
                    if trim_output_lines:
                        line = line.rstrip()
                    if replace_fffd_with_question_mark:
                        line = line.replace('\ufffd', '?')

                    print_output(line)

                    output += line + '\n'
                    if len(output)>max_output_size+1:
                        output = output[-max_output_size-1:] # drop the beginning of the string

                proc.wait()
                result = RunResult(exit_code=proc.returncode, output=output.removesuffix('\n'))
        except OSError as e:
            raise RunError(cmd=cmd, result=e) from e

        if isinstance(success, AnyExitCode) or result.exit_code in success:
            return result
        else:
            raise RunError(cmd=cmd, result=result)

    sleep_seconds = retry_initial_sleep_seconds
    for attempts_left in range(retry, 0, -1):
        try:
            return attempt_run()
        except RunError as e:
            print_message(str(e))
            if attempts_left!=1:
                plural = 's'
            else:
                plural = ''
            print_message(f'Retrying in {sleep_seconds} seconds ({attempts_left} attempt{plural} left)...')
            time.sleep(sleep_seconds)
            sleep_seconds *= retry_backoff

    return attempt_run()
