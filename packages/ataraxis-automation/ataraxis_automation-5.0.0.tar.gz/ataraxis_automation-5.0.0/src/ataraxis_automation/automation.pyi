from pathlib import Path
from dataclasses import dataclass

import click

def _format_message(message: str) -> str:
    """Formats input message strings to follow the general Ataraxis style.

    This function uses the same parameters as the default Console class implementation available through
    the ataraxis-base-utilities library. This function is used to decouple the ataraxis-automation library from
    the ataraxis-base-utilities library, removing the circular dependency introduced for these libraries in versions 2
    and 3 and allows mimicking the output of console.error() method.

    Args:
        message: The input message string to format.

    Returns:
        Formatted message string with appropriate line breaks.
    """

def _colorize_message(message: str, color: str, format_message: bool = True) -> str:
    """Modifies the input string to include an ANSI color code and, if necessary, formats the message by wrapping it
    at 120 lines.

    This function uses the same parameters as the default Console class implementation available through
    the ataraxis-base-utilities library. This function is used to decouple the ataraxis-automation library from
    ataraxis-base-utilities and, together with click.echo, allows mimicking the output of console.echo() method.

    Args:
        message: The input message string to format and colorize.
        color: The ANSI color code to use for coloring the message.
        format_message: If True, the message will be formatted by wrapping it at 120 lines.

    Returns:
        Colorized and formatted (if requested) message string.
    """
@dataclass
class EnvironmentCommands:
    """Provides a convenient interface for storing conda environment commands.

    Specifically, after commands are resolved as part of resolve_environment_commands() function runtime, they are
    packaged into an instance of this class to be used by all upstream functions.
    """

    activate_command: str
    deactivate_command: str
    create_command: str
    create_from_yml_command: str | None
    remove_command: str
    conda_dependencies_command: str | None
    pip_dependencies_command: str | None
    update_command: str | None
    export_yml_command: str
    export_spec_command: str
    environment_name: str
    install_project_command: str
    uninstall_project_command: str
    provision_command: str
    environment_directory: Path

def resolve_project_directory() -> Path:
    """Gets the current working directory from the OS and verifies that it points to a valid python project.

    This function was introduced when automation moved to a separate package to decouple the behavior of this module's
    functions from the physical location of the module source code.

    Returns:
        The absolute path to the project root directory.

    Raises:
        RuntimeError: If the current working directory does not point to a valid Python project.
    """

def resolve_library_root(project_root: Path) -> Path:
    """Determines the absolute path to the library root directory.

    Library root differs from project root. Library root is the root folder that will be included in the binary
    distribution of the project and is typically either the 'src' directory or the folder directly under 'src'.

    Notes:
        Since C-extension and pure-Python projects in Sun Lab use a slightly different layout, this function is
        used to resolve whether /src or /src/library is used as a library root. To do so, it uses a simple heuristic:
        library root is a directory at most one level below /src with __init__.py. There can only be one library root.

    Args:
        project_root: The absolute path to the root directory of the processed project.

    Returns:
        The absolute path to the root directory of the library.

    Raises:
        RuntimeError: If the valid root directory candidate cannot be found based on the determination heuristics.
    """

def resolve_environment_files(project_root: Path, environment_base_name: str) -> tuple[str, Path, Path]:
    """Determines the OS of the host platform and uses it to generate the absolute paths to os-specific conda
    environment '.yml' and 'spec.txt' files.

    Currently, this command explicitly supports only 3 OSes: OSx (ARM64, Darwin), Linux (AMD64) and Windows (AMD64).

    Args:
        project_root: The absolute path to the root directory of the processed project.
        environment_base_name: The name of the environment excluding the os_suffix, e.g.: 'axa_dev'. This function
            modifies this base name by appending the os-suffix matching the host platform OS and any necessary
            extensions to generate environment file names and paths.

    Returns:
        A tuple of three elements. The first element is the name of the environment with os-suffix, suitable
        for local conda commands. The second element is the absolute path to the os-specific conda environment '.yml'
        file. The third element is the absolute path to the os-specific environment conda 'spec.txt' file.

    Raises:
        RuntimeError: If the host OS does not match any of the supported operating systems.
    """

def resolve_conda_engine() -> str:
    """Determines whether mamba or conda can be accessed from this script by silently calling 'COMMAND --version'.

    If mamba is available, it is used over conda. This process optimizes conda-related operations
    (especially de novo environment creation) to use the fastest available engine.

    Returns:
        The string-name of the cmdlet to use for all conda (or mamba) related commands.

    Raises:
        RuntimeError: If neither conda nor mamba is accessible via subprocess call through the shell.
    """

def resolve_pip_engine() -> str:
    """Determines whether uv or pip can be accessed from this script by silently calling 'command --version'.

    If uv is available, it is used over pip. This process optimizes pip-related operations
    (especially package installation) to use the fastest available engine.

    Returns:
        The string-name of the cmdlet to use for all pip (or uv) related commands.

    Raises:
        RuntimeError: If neither pip nor uv is accessible via subprocess call through the shell.
    """

def get_base_name(dependency: str) -> str:
    """Extracts the base name of a dependency, removing versions and extras.

    This helper function is used by the main resolve_dependencies() function to match tox.ini dependencies with
    pyproject.toml dependencies.

    Args:
        dependency: The name of the dependency that can include [extras] and version data that needs to be
            stripped from the base name.

    Returns:
        The base name of the dependency.
    """

def add_dependency(
    dependency: str, dependencies_list: list[str], processed_dependencies: set[str]
) -> tuple[list[str], set[str]]:
    """Verifies that dependency base-name is not already added to the input list and, if not, adds it to list.

    Primarily, this method is used to ensure that duplicate dependencies are not stored inside the same
    pyproject.toml list (e.g.: conda and noconda).

    Args:
        dependency: The name of the evaluated dependency. Can contain extras and version, but these
            details will be stripped before the check.
        dependencies_list: The list (conda or pip) to add the dependency to if it passes verification.
        processed_dependencies: The set used to store already processed dependencies to filter duplicates.

    Returns:
        A tuple with two elements. The first element is the updated dependencies_list that includes the verified
        dependency name (with extras / version). The second element is the updated processed_dependencies set that
        includes the stripped name of the processed dependency.

    Raises:
        ValueError: If the extracted dependency is found in multiple major pyproject.toml dependency lists
            (conda, noconda, and condarun).
    """

def resolve_dependencies(project_root: Path) -> tuple[list[str], list[str]]:
    """Extracts dependencies from pyproject.toml, verifies that they cover all dependencies listed in tox.ini file and
    separates them into conda-installable and pip-installable lists.

    This function is used as a standard checkout step to ensure metadata integrity and to automate environment
    manipulations. Specifically, it is used to resolve dependencies that are then used to create / update existing
    project-specific conda environment(s).

    Args:
        project_root: The absolute path to the root directory of the processed project.

    Returns:
        A tuple containing two elements. The first element is a list of dependencies that can be installed with conda
        or pip. The second element is a list of dependencies only installable with pip (at least for some of the
        supported platforms).

    Raises:
        ValueError: If duplicate version-less dependencies are found in different pyproject optional dependency lists
            or if tox.ini contains dependencies (disregarding version and extras) not in pyproject.toml.
    """

def resolve_project_name(project_root: Path) -> str:
    """Extracts the project name from the pyproject.toml file.

    This function reads the pyproject.toml file and extracts the project name from the [project] section. The project
    name is useful for some operations, such as uninstalling or reinstalling the project into a conda environment.

    Args:
        project_root: The absolute path to the root directory of the processed project.

    Returns:
        The name of the project.

    Raises:
        ValueError: If the project name is not defined in the pyproject.toml file. Also, if the pyproject.toml file is
            corrupted or otherwise malformed.
    """

def generate_typed_marker(library_root: Path) -> None:
    """Crawls the library directory tree and ensures py.typed marker exists only at the root level of the directory.

    Specifically, if the 'py.typed' is not found in the root directory, adds the marker file. If it is found in any
    subdirectory, removes the marker file.

    Notes:
        The marker file has to be present in-addition to the '.pyi' typing files to notify type-checkers, like mypy,
        that the library contains type-annotations. This is necessary to allow other projects using type-checkers to
        verify this library API is accessed correctly.

    Args:
        library_root: The path to the root level of the library directory.
    """

def move_stubs(stubs_dir: Path, library_root: Path) -> None:
    """Moves typing stubs from the \'stubs\' directory to appropriate level(s) of the library directory tree.

    This function should be called after running stubgen on the built library package. It distributes the stubs
    generated by stubgen to their final destinations.

    Notes:
        This function expects that the \'stubs\' directory has exactly one subdirectory, which contains an __init__.pyi
        file. This subdirectory is considered to be the library root in the stubs\' structure.

    Args:
        stubs_dir: The absolute path to the "stubs" directory, expected to be found under the project root directory.
        library_root: The absolute path to the library root directory.
    """

def delete_stubs(library_root: Path) -> None:
    """Removes all .pyi stub files from the library root directory and its subdirectories.

    This function is intended to be used before running the linting task, as mypy tends to be biased to analyze the
    .pyi files, ignoring the source code. When .pyi files are not present, mypy reverts to properly analyzing the
    source code.

    Args:
        library_root: The absolute path to the library root directory.
    """

def verify_pypirc(file_path: Path) -> bool:
    """Verifies that the .pypirc file located at the input path contains valid options to support automatic
    authentication for pip uploads.

    Assumes that the file is used only to store the API token to upload compiled packages to pip. Does not verify any
    other information.

    Returns:
        True if the .pypirc is well-configured and False otherwise.
    """

def rename_all_envs(project_root: Path, new_name: str) -> None:
    """Loops over the contents of the /envs directory and replaces base environment names with the input name.

    Also updates the 'name' filed of the .yml files before renaming the files. This function is mainly designed to be
    used during template project adoption. However, it also can be used as part of tox-task to rename all
    environments in the folder (for example, when changing the environment naming pattern for the whole project).

    Notes:
        This method does not rename any existing conda environments. Manually rename any existing environments as
        needed for your project.

    Args:
        project_root: The absolute path to the root directory of the processed project.
        new_name: The new base-name to use for all environment files.
    """

def replace_markers_in_file(file_path: Path, markers: dict[str, str]) -> int:
    """Replaces all occurrences of every input marker in the contents of the provided file with the appropriate
    replacement value.

    This method opens the file and scans through file contents searching for any 'markers' dictionary keys. If keys
    are found, they are replaced with the corresponding value from the dictionary. This is used to replace the
    placeholder values used in template projects with user-defined values during project adoption.

    Args:
        file_path: The path to file in which to replace the markers.
        markers: The shallow dictionary that contains markers to replace as keys and replacement values as values.

    Returns:
        The number of placeholder values modified during this method's runtime. Minimum number is 0 for no
        modifications.
    """

def validate_library_name(_ctx: click.Context, _param: click.Parameter, value: str) -> str:
    """Verifies that the input library name contains only letters, numbers, and underscores.

    Args:
        _ctx: Not used. Provided by click automatically.
        _param: Not used. Provided by click automatically.
        value: The string-value to check

    Raises:
        BadParameter: If the input value contains invalid characters.
    """

def validate_project_name(_ctx: click.Context, _param: click.Parameter, value: str) -> str:
    """Verifies that the input project name contains only letters, numbers, and dashes.

    Args:
        _ctx: Not used. Provided by click automatically.
        _param: Not used. Provided by click automatically.
        value: The string-value to check

    Raises:
        BadParameter: If the input value contains invalid characters.
    """

def validate_author_name(_ctx: click.Context, _param: click.Parameter, value: str) -> str:
    """Verifies that the input author name contains a valid human name and an optional GitHub username in parentheses.

    Args:
        _ctx: Not used. Provided by click automatically.
        _param: Not used. Provided by click automatically.
        value: The string-value to check

    Raises:
        BadParameter: If the input value does not match the expected format.
    """

def validate_email(_ctx: click.Context, _param: click.Parameter, value: str) -> str:
    """Verifies that the input email address contains only valid characters.

    Args:
        _ctx: Not used. Provided by click automatically.
        _param: Not used. Provided by click automatically.
        value: The string-value to check

    Raises:
        BadParameter: If the input value contains invalid characters.
    """

def validate_env_name(_ctx: click.Context, _param: click.Parameter, value: str) -> str:
    """Verifies that the input environment name contains only letters, numbers, and underscores.

    Args:
        _ctx: Not used. Provided by click automatically.
        _param: Not used. Provided by click automatically.
        value: The string-value to check

    Raises:
        BadParameter: If the input value contains invalid characters.
    """

def resolve_conda_environments_directory() -> Path:
    """Returns the path to the conda / mamba environments directory.

    Raises:
        RuntimeError: If conda is not installed and / or not initialized.
    """

def strip_versions(requirements: list[str]) -> list[str]:
    """Strips version specifiers from the package names in the input list of dependencies.

    This method is used to transform the list of packages with version specifiers into a list of names. In turn, this is
    used to force uv to always reinstall pip dependencies and the base project, without reinstalling transient
    dependencies. In turn, this maximizes the use of mamba/conda used for transient and non-pip dependencies, assuming
    there is very likely an overlap between dependencies that can be installed with pip and conda for every
    project.

    Args:
        requirements: The list of strings that store dependency package names with version specifiers.

    Returns:
        The list of string package names without version specifiers.
    """

def resolve_environment_commands(
    project_root: Path, environment_name: str, python_version: str = "3.13"
) -> EnvironmentCommands:
    """Generates the list of conda and pip commands used to manipulate the project- and os-specific conda environment
    and packages it into EnvironmentCommands class.

    This function is a prerequisite for all environment-related cli commands, as it is used to resolve and generate
    all necessary commands in a project-, os- and engine(backend)-specific fashion.

    Args:
        project_root: The absolute path to the root directory of the processed project.
        environment_name: The base-name of the (project) conda environment.
        python_version: The Python version to use as part of the new environment creation process. This is also
            used during environment provisioning to modify the python version in the environment.

    Returns:
        EnvironmentCommands class instance that includes all resolved commands as class attributes.
    """

def environment_exists(commands: EnvironmentCommands) -> bool:
    """Checks whether the project-specific conda environment can be activated.

    This function is used by most environment-related cli commands to ensure the project-specific environment exists.
    In turn, knowing whether an environment exists is used to inform the behavior of multiple other functions, such
    as those used to carry out environment creation or removal.

    Args:
        commands: The EnvironmentCommands class instance that stores project-specific conda environment commands. The
            instance is configured by the resolve_environment_commands() function.

    Returns:
        True if the environment can be activated (and, implicitly, exists) and False if it cannot be activated.
    """

def cli() -> None:
    """This command-line interface exposes helper commands used to automate various project development and building
    steps."""

def process_typed_markers() -> None:
    """Crawls the library root directory and ensures that the 'py.typed' marker is found only at the highest level of
    the library hierarchy (the highest directory with __init__.py in it).

    This command is intended to be called as part of the stub-generation tox command ('tox -e stubs').

    Raises:
        RuntimeError: If root (highest) directory cannot be resolved for the project or library source code.
    """

def process_stubs() -> None:
    """Distributes the stub files from the /stubs directory to the appropriate level of the /src or
    src/library directory (depending on the type of the processed project).

    Notes:
        This command is intended to be called after the /stubs directory has been generated using tox stub-generation
        command ('tox -e stubs').

    Raises:
        RuntimeError: If root (highest) directory cannot be resolved for the project or library source code. If
        /stubs directory does not exist.
    """

def purge_stubs() -> None:
    """Removes all existing stub (.pyi) files from the library source code directory.

    This command is intended to be called as part of the tox linting task ('tox -e lint'). If stub files are present
    during linting, mypy (type-checker) preferentially processes stub files and ignores source code files. Removing the
    stubs before running mypy ensures it runs on the source code.

    Raises:
        RuntimeError: If root (highest) directory cannot be resolved for the project or library source code.
    """

def generate_recipe_folder() -> None:
    """Generates the /recipe directory inside project root directory.

    This command is intended to be called before using Grayskull via the tox recipe-generation task ('tox -e recipe')
    to generate the conda-forge recipe for the project. Since Grayskull does not generate output directories by itself,
    this task is 'outsourced' to this command instead.

    Raises:
        RuntimeError: If root (highest) directory cannot be resolved for the project.
    """

def acquire_pypi_token(replace_token: bool) -> None:
    """Ensures that a validly formatted PyPI API token is available from the .pypirc file stored in the root directory
    of the project.

    This command is intended to be called before the tox pip-uploading task ('tox -e upload') to ensure that twine is
    able to access the PyPI API token. If the token is available from the '.pypirc' file and appears valid, it is used.
    If the file or the API token is not available or the user provides 'replace-token' flag, the command recreates the
    file and prompts the user to provide a new token. The token is then added to the file for future (re)uses.

    Notes:
        The '.pypirc' file is added to gitignore, so the token will remain private unless gitignore is compromised.

        This function is currently not able to verify that the token works. Instead, it can only ensure the token
        is formatted in a PyPI-specified way (specifically, that it includes the pypi-prefix). If the token is not
        active or otherwise invalid, only a failed twine upload will be able to determine that.

    Raises:
        ValueError: If the token provided by the user is not valid.
        RuntimeError: If the user aborts the token acquisition process without providing a valid token.
    """

def install_project(environment_name: str) -> None:
    """Builds and installs the project into the specified conda environment.

    This command is primarily used to support project developing by compiling and installing the developed project into
    the environment to allow manual project testing. Since tests have to be written to use compiled package, rather than
    the source code to support tox testing, the project has to be rebuilt each time source code is changed, which is
    conveniently performed by this command.

    Raises:
        RuntimeError: If project installation fails. If project environment does not exist.
    """

def uninstall_project(environment_name: str) -> None:
    """Uninstalls the project library from the specified conda environment.

    This command is not used in most modern automation pipelines, but is kept for backward compatibility with legacy
    projects. Previously, it was used to remove the project from its conda environment before running tests, as
    installed projects used to interfere with tox re-building the wheels for testing.

    Notes:
        If the environment does not exist or is otherwise not accessible, the function returns without attempting to
        uninstall the project.

    Raises:
        RuntimeError: If any of the environment-manipulation subprocess calls fail.
    """

def create_env(environment_name: str, python_version: str) -> None:
    """Creates the project conda environment and installs project dependencies into the created environment.

    This command is intended to be called during initial project setup for new platforms (OSes) or when the environment
    needs to be hard-reset. For most runtimes, it is advised to import ('tox -e import') an existing .yml file if it is
    available. If you need to reset an already existing environment, it is advised to use the provision
    ('tox -e provision') command instead, which re-installs environment packages without deleting the environment
    itself.

    Raises:
        RuntimeError: If any environment creation steps fail for any reason.
    """

def remove_env(environment_name: str) -> None:
    """Removes (deletes) the specified conda environment if it exists.

    This command can be used to clean up local conda distribution when conda environment is no longer needed.
    Alternatively, this command can also be used to clear an existing environment before recreating it with create-env
    ('tox -e create') command. If your main goal is to reset the environment, however, it is recommended to use the
    'provision-env' ('tox -e provision') command instead, which removes and (re)installs all packages without altering
    the environment itself.

    Raises:
        RuntimeError: If environment removal fails for any reason.
    """

def provision_env(environment_name: str, python_version: str) -> None:
    """Removes all packages from the target conda environment (including python) and then re-installs project
    dependencies specified in pyproject.toml file.

    This command is intended to be called when the project has a configured environment referenced by IDEs and other
    tools. Instead of removing the environment, this acts as a 'soft' reset mechanism that actualizes environment
    contents without breaking any references.

    Raises:
        RuntimeError: If any environment modification steps fail for any reason.
    """

def import_env(environment_name: str) -> None:
    """Creates or updates an existing conda environment based on the operating-system-specific .yml file stored in
    /envs directory.

    If the .yml file does not exist, aborts processing with error. Generally, this command is preferred over
    'create-env' ('tox -e create') whenever a valid .yml file for the current platform is available.
    OS-specific .yml files are what the developers use and are guaranteed to work for all supported platforms.

    Raises:
        RuntimeError: If there is no .yml file for the desired base-name and OS-extension combination in the /envs/
        directory. If creation and update commands both fail for any reason.
    """

def export_env(environment_name: str) -> None:
    """Exports the requested conda environment as a .yml and as a spec.txt file to the /envs directory.

    This command is intended to be called as part of the pre-release checkout, before building the source distribution
    for the project (and releasing the new project version).

    Raises:
        RuntimeError: If the environment export process fails for any reason. If the conda environment to export does
        not exist.
    """

def rename_environments(new_name: str) -> None:
    """Iteratively renames environment files inside the 'envs' directory to use the provided name as the base-name.

    Notes:
        This function does not rename any existing conda environments. This behavior is intentional. It is advised to
        first export the environment via 'export-env' ('tox -e export'). Then to use 'remove-env' ('tox -e remove') to
        remove the existing environment, followed by this function to rename the .yml and spec.txt files. Finally,
        re-import the environment via 'import-env' ('tox -e import').

    """

def adopt_project(library_name: str, project_name: str, author_name: str, email: str, env_name: str) -> None:
    """Adopts a new project initialized from a standard Sun Lab template, by replacing placeholders in metadata and
    automation files with user-defined data.

    In addition to replacing placeholders inside a predefined set of files, this function also renames any files whose
    names match any of the markers. At this time, the function is used to set: project name, library name, development
    (conda) environment base-name, author name, and author email. In the future, more markers may be added as needed.

    Notes:
        Manual validation of all automation files is highly advised. This function is not intended to replace manual
        configuration, but only to expedite it in critical bottlenecks. It is very likely that your project will not
        work as expected without additional configuration.

    Raises:
        RuntimeError: If the adoption process fails for any reason.
    """
