# Initialise your development environment

All following commands must be run only once at project installation.


## First clone

```sh
git clone --recursive {{cookiecutter.git_project_url}}
{%if cookiecutter.use_submodule_for_deploy_code-%}git submodule init # only the fist time
git submodule update --recursive{%endif%}
```

## Before using any ansible command: a note on sudo
If your user is ``sudoer`` but is asking for you to input a password before elavating privileges,
you will need to add ``--ask-sudo-pass`` and maybe ``--become`` to any of the following ``ansible alike`` commands.


## Install docker and docker compose

if you are under debian/ubuntu/mint/centos you can do the following:

```sh
.ansible/scripts/download_corpusops.sh
.ansible/scripts/setup_corpusops.sh
local/*/bin/cops_apply_role --become \
    local/*/*/corpusops.roles/services_virt_docker/role.yml
```

... or follow official procedures for
  [docker](https://docs.docker.com/install/#releases) and
  [docker-compose](https://docs.docker.com/compose/install/).

## Configuration

Use the wrapper to init configuration files from their ``.dist`` counterpart
and adapt them to your needs.

```bash
./control.sh init
```

## Login to the app docker registry

You need to login to our docker registry to be able to use it:


```bash
docker login {{cookiecutter.docker_registry}}  # use your gitlab user
```

{%- if cookiecutter.registry_is_gitlab_registry %}
**⚠️ See also ⚠️** the
    [project docker registry]({{cookiecutter.git_project_url}}/container_registry)
{%- else %}
**⚠️ See also ⚠️** the makinacorpus doc in the docs/tools/dockerregistry section.
{%- endif%}

# Use your development environment

## Update submodules

Never forget to grab and update regulary the project submodules:

```sh
git pull{% if cookiecutter.use_submodule_for_deploy_code
%}
git submodule init # only the fist time
git submodule update --recursive{%endif%}
```

## Control.sh helper

You may use the stack entry point helper which has some neat helpers but feel
free to use docker command if you know what your are doing.

```bash
./control.sh usage # Show all available commands
```

## Start the stack

After a last verification of the files, to run with docker, just type:

```bash
# First time you download the app, or sometime to refresh the image
./control.sh pull # Call the docker compose pull command
./control.sh up # Should be launched once each time you want to start the stack
```

## Launch app in foreground

```bash
./control.sh fg
```

**⚠️ Remember ⚠️** to use `./control.sh up` to start the stack before.

## Where is the admin password
in  ``docker.env``, see ``PLONE__ADMIN`` and ``PLONE__ADMIN_PASSWORD``.

## Create the site

Open a browser at address http://localhost:8080

Lookup admin password inside ./docker.env file.

Create a website named "Plone"

## Start a shell inside the {{cookiecutter.app_type}} container

- for user shell

    ```sh
    ./control.sh usershell
    ```
- for root shell

    ```sh
    ./control.sh shell
    ```

**⚠️ Remember ⚠️** to use `./control.sh up` to start the stack before.

## Run plain docker-compose commands

- Please remember that the ``CONTROL_COMPOSE_FILES`` env var controls which docker-compose configs are use (list of space separated files), by default it uses the dev set.

    ```sh
    ./control.sh dcompose <ARGS>
    ```

## Rebuild/Refresh local docker image in dev

```sh
control.sh buildimages
```

**⚠️ Remember ⚠️** to use `./control.sh up` to start the stack before.

## Run tests

```sh
./control.sh tests
# also consider: linting|coverage
```

**⚠️ Remember ⚠️** to use `./control.sh up` to start the stack before.

## File permissions
If you get annoying file permissions problems on your host in development, you can use the following routine to (re)allow your host
user to use files in your working directory


```sh
./control.sh open_perms_valve
```

## Docker volumes

Your application extensivly use docker volumes. From times to times you may
need to erase them (eg: burn the db to start from fresh)

```sh
docker volume ls  # hint: |grep \$app
docker volume rm $id
```


## Reuning a precached image in dev to accelerate rebuilds
Once you have build once your image, you have two options to reuse your image as a base to future builds, mainly to accelerate buildout successive runs.

- Solution1: Use the current image as an incremental build: Put in your .env

    ```sh
    PLONE_BASE_IMAGE={{ cookiecutter.docker_image }}:latest-dev
    ```

- Solution2: Use a specific tag: Put in your .env

    ```sh
    PLONE_BASE_IMAGE=a tag
    # this <a_tag> will be done after issuing: docker tag registry.makina-corpus.net/mirabell/chanel:latest-dev a_tag
    ```

## Integrating an IDE
- <strong>DO NOT START YET YOUR IDE</strong>
- Add to your .env and re-run ``./control.sh build plone``

    ```sh
    WITH VISUALCODE=1
    #  or
    WITH_PYCHARM=1
    # note that you can also set the version to install (see .env.dist)
    ```

- Start the stack, but specially stop the app container as you will
  have to separatly launch it wired to your ide

    ```sh
    ./control.sh up
    ./control.sh down plone
    ```


### Get the completion and the code resolving for bundled dependencies wich are inside the container

- Whenever you rebuild the image, you need to refresh the files for your IDE to complete bundle dependencies

    ```sh
    ./control.sh get_container_code
    ```
### Using pycharm
- Only now launch pycharm and configure a project on this working directory
- Whenever you open your pycharm project:
    - **remember to exclude the local source folders inside the local/code/omelette**
    - Add local/code/omelette to sources
    - Add local/code/venv/lib/python*/site-packages to sources

#### Make a break, insert a PDB and attach the session on Pycharm
- The docker container will connect to your running pycharm process, using a network tcp connection, eg on port ``12345``.
- ``12345`` can be changed but of course adapt the commands, this port must be reachable from within the container.
- Linux only: This iptables rule can be more restrictive if you know and you want to but as the following it will allow unfiltered connections on port ``12345``.

    ```sh
    iptables -I INPUT  -p tcp -m tcp --dport 12345 -j ACCEPT
    ```

- Ensure you added ``WITH_PYCHARM`` in your ``.env`` and that ``PYCHARM_VERSION`` is tied to your PYCHARM installation and start from a fresh build if it was not (pip will mess to update it correctly, sorry).
- Wherever you have the need to break, insert in your code the following snippet:

    ```python
    import pydevd_pycharm;pydevd_pycharm.settrace('host.docker.internal', port=12345, stdoutToServer=True, stderrToServer=True)
    ```
    - if ``host.docker.internal`` does not work for you, you can replace it by the local IP of your machine.
- Remember this rules to insert your breakpoint:  If the file reside on your host, you can directly insert it, but on the other side, you will need to run a usershell session and debug from there.<br/>
  Eg: if  you want to put a pdb in ``parts/omelette/Products/CMFPlone/__init__.py``
    - <strong>DO NOT DO IT in ``local/code/parts/omelette/Products/CMFPlone/__init__.py`` </strong>
    - do:

        ```sh
        ./control.sh down plone
        services_ports=1 ./control.sh usershell
        apt install -y vim
        vim parts/omelette/Products/CMFPlone/__init__.py
        # insert: import pydevd_pycharm;pydevd_pycharm.settrace('host.docker.internal', port=12345, stdoutToServer=True, stderrToServer=True)
        ./bin/instance fg
        ```
    - With pycharm and your configured debugging session, attach to the session


### Using VSCode
- You must launch VSCode using ``./control.sh vscode`` as vscode needs to have the ``PYTHONPATH`` variable preset to make linters work

    ```sh
    ./control.sh vscode
    ```
    - In other words, this add ``local/**/omelette`` & ``local/**/site-packages`` to vscode sys.path.


Additionnaly, adding this to ``.vscode/settings.json`` would help to give you a smooth editing experience

  ```json
  {
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/.git/subtree-cache/**": true,
        "**/node_modules/*/**": true,
        "**/local/*/**": true,
        "**/local/code/venv/lib/**/site-packages/**": false,
        "**/local/code/omelette/**": false

      }
  }
  ```

#### Debugging with VSCode
- [vendor documentation link](https://code.visualstudio.com/docs/python/debugging#_remote-debugging)
- The docker container will connect to your running VSCode process, using a network tcp connection, eg on port ``5678``.
- ``5678`` can be changed but of course adapt the commands, this port must be reachable from within the container and in the ``docker-compose-dev.yml`` file.
- Ensure you added ``WITH_VSCODE`` in your ``.env`` and that ``VSCODE_VERSION`` is tied to your VSCODE installation and start from a fresh build if it was not (pip will mess to update it correctly, sorry).
- Wherever you have the need to break, insert in your code the following snippet after imports (and certainly before wherever you want your import):

    ```python
    import ptvsd;ptvsd.enable_attach(address=('0.0.0.0', 5678), redirect_output=True);ptvsd.wait_for_attach()
    ```
- Remember this rules to insert your breakpoint:  If the file reside on your host, you can directly insert it, but on the other side, you will need to run a usershell session and debug from there.<br/>
  Eg: if  you want to put a pdb in ``parts/omelette/Products/CMFPlone/__init__.py``
    - <strong>DO NOT DO IT in ``local/code/parts/omelette/Products/CMFPlone/__init__.py`` </strong>
    - do:

        ```sh
        ./control.sh down plone
        services_ports=1 ./control.sh usershell
        apt install -y vim
        vim parts/omelette/Products/CMFPlone/__init__.py
        # insert: import ptvsd;ptvsd.enable_attach(address=('0.0.0.0', 5678), redirect_output=True);ptvsd.wait_for_attach()
        ./bin/instance fg
        ```
- toggle a breakpoint on the left side of your text editor on VSCode.
- Switch to Debug View in VS Code, select the Python: Attach configuration, and select the settings (gear) icon to open launch.json to that configuration.<br/>
  Duplicate the remote attach part and edit it as the following

  ```json
  {
    "name": "Python Docker Attach",
    "type": "python",
    "request": "attach",
    "pathMappings": [
      {
        "localRoot": "${workspaceFolder}",
        "remoteRoot": "/code"
      }
    ],
    "port": 5678,
    "host": "localhost"
  }
  ```
- With VSCode and your configured debugging session, attach to the session and it should work


## Do not use Unified installer buildout cache
Add ``PLONE_UI_BYPASS=1`` to your .env

## Doc for deployment on environments
- [See here](./docs/README.md)
