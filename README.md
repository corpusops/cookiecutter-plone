
DISCLAIMER - ABANDONED/UNMAINTAINED CODE / DO NOT USE
=======================================================
While this repository has been inactive for some time, this formal notice, issued on **December 10, 2024**, serves as the official declaration to clarify the situation. Consequently, this repository and all associated resources (including related projects, code, documentation, and distributed packages such as Docker images, PyPI packages, etc.) are now explicitly declared **unmaintained** and **abandoned**.

I would like to remind everyone that this project’s free license has always been based on the principle that the software is provided "AS-IS", without any warranty or expectation of liability or maintenance from the maintainer.
As such, it is used solely at the user's own risk, with no warranty or liability from the maintainer, including but not limited to any damages arising from its use.

Due to the enactment of the Cyber Resilience Act (EU Regulation 2024/2847), which significantly alters the regulatory framework, including penalties of up to €15M, combined with its demands for **unpaid** and **indefinite** liability, it has become untenable for me to continue maintaining all my Open Source Projects as a natural person.
The new regulations impose personal liability risks and create an unacceptable burden, regardless of my personal situation now or in the future, particularly when the work is done voluntarily and without compensation.

**No further technical support, updates (including security patches), or maintenance, of any kind, will be provided.**

These resources may remain online, but solely for public archiving, documentation, and educational purposes.

Users are strongly advised not to use these resources in any active or production-related projects, and to seek alternative solutions that comply with the new legal requirements (EU CRA).

**Using these resources outside of these contexts is strictly prohibited and is done at your own risk.**

This project has been transfered to Makina Corpus <freesoftware@makina-corpus.com> ( https://makina-corpus.com ). This project and its associated resources, including published resources related to this project (e.g., from PyPI, Docker Hub, GitHub, etc.), may be removed starting **March 15, 2025**, especially if the CRA’s risks remain disproportionate.

# Init a plone project

Idea is to create it with a wonderful python tool called
[cookiecutter](https://github.com/audreyr/cookiecutter)

##  Install prerequisites
```
if ! ( virtualenv --version 2>&1 >/dev/null );then echo "ERROR: install venv, on debian/ubuntu: apt install -y virtualenv,fi";fi
virtualenv --python=python3 ~/tools/cookiecutter
~/tools/cookiecutter/bin/pip install cookiecutter
```

## Create back project

- create on gitlab your project
- then locally (replace with your values)

    ```sh
    cd ~/.cookiecutters/cookiecutter-plone \
        && git fetch origin && git reset --hard origin/master \
        && cd -
    cookiecutter --no-input -f -o ~/out_dir \
        https://github.com/corpusops/cookiecutter-plone.git \
        name=foo \
        tld_domain=mydomain.com \
        git_server=git.foo.com \
        git_ns=bar \
        dev_port=40001 staging_port=40003 qa_host="" prod_port=40010
    cd ~/out_dir
    # review before commit
    # for relative checkout to work, we need remote objects locally
    git commit local -m "Add deploy"
    ```

- Read [cookiecutter.json](./cookiecutter.json) for all options
-  notable options behaviors:
    - ``use_submodule_for_deploy_code=``: copy deploy submodule inside
      project for a standalone deployment (no common deploy)
    - ``py_ver=X.Yy``: python version to use
    - ``(qa|staging)_host=``: will disable generation for this env
    - ``tests_(staging|tests)=``: will disable those specific tests in CI
    - ``registry_is_gitlab_registry=y``: act that registry is gitlab based
      and use token to register image against and
      autofill ``register_user`` and ``registry_password``.


## Fill ansible inventory

### Generate ssh deploy key
```ssh
cd local
ssh-keygen -t rsa -b 2048 -N '' -C deploy -f deploy
```

### Generate vaults password file
```sh
export CORPUSOPS_VAULT_PASSWORD=SuperVerySecretPassword
.ansible/scripts/setup_vaults.sh
```

- Also add that variable ``CORPUSOPS_VAULT_PASSWORD`` in the gitlab CI/CD variables
- You would certainly also add ``REGISTRY_USER`` & ``REGISTRY_PASSWORD``.

### Move vault templates to their encrypted counterparts
For each file which needs to be crypted
```sh
# to find them
find .ansible/inventory/group_vars/|grep encrypt
```

### Generate vaults
Also open and read both your project top ``README.md`` and the ``.ansible/README.md``

You need to
1. open in a editor:

    ```sh
    $EDITOR .ansible/inventory/group_vars/dev/default.movemetoencryptedvault.yml
    ```
2. In another window/shell, use Ansible vault to create/edit that file without the "encrypted" in the filename and
copy/paste/adapt the content

    ```sh
    .ansible/scripts/edit_vault.sh .ansible/inventory/group_vars/dev/default.yml
    ```
3. Delete the original file

    ```sh
    rm -f .ansible/inventory/group_vars/dev/default.movemetoencryptedvault.yml
    ```

- Wash, rince, repeat for each needing-to-be-encrypted vault.
- ⚠️Please note⚠️: that you will need to put the previously generated ssh deploy key in ``all/default.yml``

## Init dev and and test locally
```sh
./control.sh init  # init conf files
./control.sh build plone
./control.sh build  # will be faster as many images are based on plone
```

## Push to gitlab
- Push to gitlab and run the dev job until it succeeds
- Trigger the dev image release job until it succeeds


## Deploy manually
- Deploy manually one time to see everything is in place<br/>
  Remember:
    - Your local copy is synced as the working directory on target env (with exclusions, see playbooks)
    - The ``cops_plone_docker_tag`` controls which docker image is deployed.

    ```sh
    .ansible/scripts/call_ansible.sh .ansible/playbooks/deploy_key_setup.yml
    .ansible/scripts/call_ansible.sh -vvv .ansible/playbooks/ping.yml -l dev  # or staging
    .ansible/scripts/call_ansible.sh -vvv .ansible/playbooks/app.yml \
         -e "{cops_plone_docker_tag: dev}" -l dev  # or staging
    ```

## Update project
You can regenerate at a later time the project
```sh
local/regen.sh  # and verify new files and updates
```


## Credits
- Inspiration and bits from [plone.docker](https://github.com/plone/plone.docker)


