#!/usr/bin/env python3

import argparse
import json
import logging
import os
import re
import shlex
import subprocess
import sys


class InvalidSpecException(Exception):
    pass


def process_docker_spec(
    spec,
    /,
    dockerfile=None,
    debug=False,
    run=True,
    allow_shell=False,
    ignore_missing=False,
    mode=None,
    custom_opts=[],
) -> int:
    logger = logging.getLogger(__name__)

    # Make sure we have a valid spec
    if spec is None or spec == "":
        raise InvalidSpecException("Spec must not be empty")

    if not os.path.exists(spec):
        raise InvalidSpecException(f"Spec does not exist: {spec}")

    # Make sure the mode is valid
    if mode is None:
        mode = "default"
    elif mode == "" or re.search(r"^[A-Za-z0-9]+$", mode) is None:
        raise ValueError("Invalid mode specified - Must be [A-Za-z0-9]+")

    # Work out what to do with the spec and optional dockerfile
    if dockerfile is not None and dockerfile != "":
        # We have a dockerfile reference, so the spec must be a directory
        if not os.path.isdir(spec):
            raise InvalidSpecException(
                "Dockerfile specified, but the spec is not a directory"
            )
    else:
        if os.path.isfile(spec):
            dockerfile = spec
            spec = os.path.dirname(dockerfile)
        elif os.path.isdir(spec):
            dockerfile = os.path.join(spec, "Dockerfile")
        else:
            raise InvalidSpecException(
                f"Could not determine type of target spec (directory or file): {spec}"
            )

    # At this point, spec is the path to the Docker build directory and dockerfile
    # is the location of the actual Dockerfile
    logger.debug(f"Directory: {spec}")
    logger.debug(f"Dockerfile: {dockerfile}")

    build_opts = ""
    run_opts = ""
    image_opts = ""
    shell = False

    # Read the dockerfile for processing
    lines = []
    try:
        with open(dockerfile, "r") as file:
            lines = file.read().splitlines()
    except FileNotFoundError as e:
        if not ignore_missing:
            logger.error("Dockerfile ({dockerfile}) not found: %s", e)
            raise

        logger.warning("Dockerfile ({dockerfile}) not found %s", e)
        return 0

    # Look for any of the Dockerfile options affecting the build or run
    for line in lines:
        match = re.search(r"^\s*#\s*BUILD_OPTS\s*(.*)", line)
        if match is not None:
            build_opts = f"{build_opts} {match.groups()[0]}"
            continue

        match = re.search(r"^\s*#\s*RUN_OPTS\s*(.*)", line)
        if match is not None:
            run_opts = f"{run_opts} {match.groups()[0]}"
            continue

        match = re.search(r"^\s*#\s*IMAGE_OPTS\s*(.*)", line)
        if match is not None:
            image_opts = f"{image_opts} {match.groups()[0]}"
            continue

        match = re.search(r"^\s*#\s*USE_SHELL\s*(.*)", line)
        if match is not None:
            if not allow_shell:
                raise Exception(
                    "Dockerfile requires shell parsing, but shell parsing not allowed"
                )

            shell = True
            continue

        if mode is not None and mode != "":
            match = re.search(r"^\s*#\s*" + mode + r"_BUILD_OPTS\s*(.*)", line)
            if match is not None:
                build_opts = f"{build_opts} {match.groups()[0]}"
                continue

            match = re.search(r"^\s*#\s*" + mode + r"_RUN_OPTS\s*(.*)", line)
            if match is not None:
                run_opts = f"{run_opts} {match.groups()[0]}"
                continue

            match = re.search(r"^\s*#\s*" + mode + r"_IMAGE_OPTS\s*(.*)", line)
            if match is not None:
                image_opts = f"{image_opts} {match.groups()[0]}"
                continue

    logger.debug(f"Build Options: {build_opts}")
    logger.debug(f"Run Options: {run_opts}")
    logger.debug(f"Image Options: {image_opts}")
    logger.debug(f"Custom Options: {custom_opts}")

    # Configure environment variables for use by docker commands
    os.environ["DFBAR_DOCKER_DIR"] = spec
    os.environ["DFBAR_DOCKERFILE"] = dockerfile
    os.environ["DFBAR_USER_ID"] = str(os.getuid())
    os.environ["DFBAR_GROUP_ID"] = str(os.getgid())
    os.environ["DFBAR_CWD"] = os.getcwd()

    # Perform a build of the Dockerfile
    build_cmd = f"docker build -f {dockerfile} -q {spec} {build_opts}"

    call_args: list[str] | str

    if shell:
        call_args = build_cmd
    else:
        call_args = shlex.split(build_cmd)
        call_args = [os.path.expandvars(x) for x in call_args]

    logger.debug(f"Build call args: {call_args}")

    sys.stdout.flush()
    proc = subprocess.run(
        call_args, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if proc.returncode != 0:
        logger.error(proc.stdout.decode("ascii"))
        return proc.returncode

    docker_image = proc.stdout.decode("ascii").splitlines()[-1]
    logger.debug(f"Docker image SHA: {docker_image}")

    # Run the container image
    if run:
        logger.debug("Running container image")

        interactive_arg = ""
        if sys.stdin.isatty():
            logger.debug("Input is a TTY")
            interactive_arg = " -i "
        else:
            logger.debug("Input is not a TTY")

        run_cmd = f"docker run --rm {interactive_arg} -t {run_opts} {docker_image} {image_opts}"
        if shell:
            call_args = run_cmd
            for opt in custom_opts:
                call_args = '%s "%s"' % (call_args, opt.replace('"', '\\"'))
        else:
            call_args = shlex.split(run_cmd)
            call_args = [os.path.expandvars(x) for x in call_args]
            call_args = call_args + custom_opts

        logger.debug(f"Run call args: {call_args}")

        sys.stdout.flush()
        return subprocess.run(call_args, shell=shell).returncode

    return 0


def process_args():
    # Process the command line arguments
    parser = argparse.ArgumentParser(
        prog="dfbar", description="Dockerfile Build and Run", exit_on_error=False
    )

    # Mutually exclusive group to alter default behaviour
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-p",
        action="store_true",
        dest="profile",
        help="A profile name to run. This is the name of a directory under ~/.dfbar to build and run",
    )

    group.add_argument(
        "-f",
        action="store",
        dest="dockerfile",
        help="Override the location of the Dockerfile. This is not valid is spec resolves to a directory",
    )

    group.add_argument(
        "-b",
        action="store_true",
        dest="basedir",
        help='The "spec" is a directory with subdirectories that should be built and run, in lexical order',
    )

    # Other options
    parser.add_argument(
        "-n",
        action="store_false",
        dest="run",
        help="Do not run the Dockerfile, only build",
    )

    parser.add_argument(
        "-i",
        action="store_true",
        dest="ignore_missing",
        help="Ignore missing Dockerfiles when running with a base directory",
    )

    parser.add_argument(
        "-v", "-d", action="store_true", dest="debug", help="Verbose/debug output"
    )

    parser.add_argument(
        "-s",
        action="store_true",
        dest="allow_shell",
        help=(
            "Allow use of the shell to execute the build, run and image options. "
            "This can be dangerous if the Dockerfile is from an untrusted source"
        ),
    )

    parser.add_argument(
        "-m",
        action="store",
        dest="mode",
        default=None,
        help=(
            "Mode to apply to the dockerfile build and run. Mode affects the "
            "configuration directives read from the Dockerfile"
        ),
    )

    parser.add_argument(
        "spec",
        action="store",
        help=(
            "The Dockerfile directory, Dockerfile, base directory or image profile, "
            "depending on options. Default to determine Dockerfile directory or Dockerfile"
        ),
    )

    parser.add_argument(
        "custom_opts",
        action="store",
        nargs=argparse.REMAINDER,
        help="Custom options to supply to the image being run",
    )

    args = parser.parse_args()

    # Store the options here to allow modification depending on options
    ignore_missing = args.ignore_missing
    dockerfile = args.dockerfile
    debug = args.debug
    run = args.run
    allow_shell = args.allow_shell
    mode = args.mode
    custom_opts = args.custom_opts

    # Logging configuration
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")
    logger = logging.getLogger(__name__)

    # Allow use of the shell for parsing by environment variable
    env_shell = os.environ.get("DFBAR_ALLOW_SHELL")
    if env_shell is not None and env_shell.lower() in ["1", "true"]:
        allow_shell = True

    spec_list = []

    # Make sure we have a valid spec
    if args.spec is None or args.spec == "":
        raise Exception("Spec must not be empty")

    # If we have a profile, set the directory to the location of the profile
    if args.profile:
        if ignore_missing:
            logger.warning("ignore missing does not apply with a profile name.")
            ignore_missing = False

        # Shell parsing is automatically allowed for profiles, unless disabled by environment var
        env_shell = os.environ.get("DFBAR_ALLOW_PROFILE_SHELL")
        if env_shell is not None and env_shell.lower() not in ["1", "true"]:
            allow_shell = False
        else:
            allow_shell = True

        # dockerfile should be empty and we have an array of a single directory/spec, representing the
        # profile to run
        spec_list = [os.path.join(os.path.expanduser("~"), ".dfbar", args.spec)]
    elif args.basedir:
        if dockerfile:
            logger.warning("Dockerfile is not valid with a base directory.")
            dockerfile = None

        # Collect a list of subdirectories and sort lexically
        spec_list = [x.path for x in os.scandir(args.spec) if x.is_dir()]
        spec_list.sort()
    else:
        # Not a base directory or profile

        if ignore_missing:
            logger.warning("ignore missing does not apply with a single directory.")
            ignore_missing = False

        spec_list = [args.spec]

    logger.debug("Processing specs:")
    logger.debug(json.dumps(spec_list, indent=2))
    logger.debug("")

    # Process the specs
    ret = 0
    try:
        for spec in spec_list:
            ret = process_docker_spec(
                spec,
                dockerfile=dockerfile,
                debug=debug,
                run=run,
                allow_shell=allow_shell,
                ignore_missing=ignore_missing,
                mode=mode,
                custom_opts=custom_opts,
            )

            if ret != 0:
                break
    except Exception as e:
        logger.error(f"Processing failed with error: {e}")
        return 1

    return ret


def main():
    try:
        ret = process_args()
        sys.stdout.flush()
        sys.exit(ret)
    except Exception as e:
        logging.getLogger(__name__).exception(e)
        sys.stdout.flush()
        sys.exit(1)


if __name__ == "__main__":
    main()
