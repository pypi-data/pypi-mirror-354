import os
import pytest

from edpm.engine.api import EdpmApi
from edpm.engine.generators.environment_generator import EnvironmentGenerator
from edpm.engine.generators.cmake_generator import CmakeGenerator
from edpm.engine.planfile import PlanFile

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_TMP_DIR = os.path.join(TEST_DIR, "tmp")

BASH_IN_PATH = os.path.join(TEST_TMP_DIR, "env_bash_in.sh")
BASH_OUT_PATH = os.path.join(TEST_TMP_DIR, "env_bash_out.sh")
CSH_IN_PATH = os.path.join(TEST_TMP_DIR, "env_csh_in.csh")
CSH_OUT_PATH = os.path.join(TEST_TMP_DIR, "env_csh_out.csh")


@pytest.fixture
def setup_test_environment():
    """Sets up a temporary directory and sample 'in' files with placeholders."""
    os.makedirs(TEST_TMP_DIR, exist_ok=True)

    # Create an initial env_bash_in file with a placeholder
    with open(BASH_IN_PATH, "w") as f:
        f.write("# Initial content (bash)\n# {{{EDPM-CONTENT}}}\n# End content\n")

    # Create an initial env_csh_in file with a placeholder
    with open(CSH_IN_PATH, "w") as f:
        f.write("# Initial content (csh)\n# {{{EDPM-CONTENT}}}\n# End content\n")

    yield  # Tests run

    # Cleanup
    for path in [BASH_IN_PATH, BASH_OUT_PATH, CSH_IN_PATH, CSH_OUT_PATH]:
        if os.path.exists(path):
            os.remove(path)
    try:
        os.rmdir(TEST_TMP_DIR)
    except OSError:
        pass


def _make_minimal_api():
    """Returns an EdpmApi with a minimal in-memory plan + lock, no actual disk files."""
    api = EdpmApi(plan_file="in-memory-plan.yaml", lock_file="in-memory-lock.yaml")
    raw_data = {
        "global": {
            "config": {},
            "environment": [
                {"set": {"MY_VAR": "some_value"}}
            ]
        },
        "packages": []
    }
    from edpm.engine.planfile import PlanFile
    api.plan = PlanFile(raw_data)
    api.lock.data = {
        "top_dir": "/fake/top_dir",
        "packages": {}
    }
    return api


def test_env_save_with_in_out_files(setup_test_environment):
    """
    If 'in' files exist with the EDPM placeholder, verify merging environment lines.
    """
    api = _make_minimal_api()
    api.plan.data["global"]["config"].update({
        "env_bash_in": BASH_IN_PATH,
        "env_bash_out": BASH_OUT_PATH,
        "env_csh_in": CSH_IN_PATH,
        "env_csh_out": CSH_OUT_PATH
    })

    env_gen = EnvironmentGenerator(plan=api.plan, lock=api.lock, recipe_manager=api.recipe_manager)
    # Merge for bash
    env_gen.save_environment_with_infile("bash", BASH_IN_PATH, BASH_OUT_PATH)
    # Merge for csh
    env_gen.save_environment_with_infile("csh", CSH_IN_PATH, CSH_OUT_PATH)

    with open(BASH_OUT_PATH, "r") as f:
        content = f.read()
        assert "# Initial content (bash)" in content
        assert "export MY_VAR=\"some_value\"" in content

    with open(CSH_OUT_PATH, "r") as f:
        content = f.read()
        assert "# Initial content (csh)" in content
        assert "setenv MY_VAR \"some_value\"" in content


def test_env_save_without_in_files(setup_test_environment):
    """
    If no 'in' files are defined, we want to generate environment scripts from scratch.
    We'll pass in None (instead of empty string) to skip merging logic.
    """
    api = _make_minimal_api()
    env_gen = EnvironmentGenerator(plan=api.plan, lock=api.lock, recipe_manager=api.recipe_manager)

    # Instead of "", pass None to avoid FileNotFoundError
    env_gen.save_environment_with_infile("bash", None, BASH_OUT_PATH)
    env_gen.save_environment_with_infile("csh", None, CSH_OUT_PATH)

    with open(BASH_OUT_PATH) as f:
        content = f.read()
        assert "#!/usr/bin/env bash" in content
        assert "export MY_VAR=\"some_value\"" in content

    with open(CSH_OUT_PATH) as f:
        content = f.read()
        assert "#!/usr/bin/env csh" in content
        assert "setenv MY_VAR \"some_value\"" in content


def test_cmake_toolchain_in_out(setup_test_environment):
    """
    1) Create minimal plan, set cmake_toolchain_in/out in global config.
    2) Save toolchain with placeholders.
    3) Confirm final file merges + includes EDPM's 'Automatically generated' lines.
    """
    cm_in = os.path.join(TEST_TMP_DIR, "cmake_toolchain_in.cmake")
    cm_out = os.path.join(TEST_TMP_DIR, "cmake_toolchain_out.cmake")
    with open(cm_in, "w") as f:
        f.write("# Initial CMake content\n# {{{EDPM-CONTENT}}}\n")

    api = _make_minimal_api()
    api.plan.data["global"]["config"].update({
        "cmake_toolchain_in": cm_in,
        "cmake_toolchain_out": cm_out
    })

    cm_gen = CmakeGenerator(plan=api.plan, lock=api.lock, recipe_manager=api.recipe_manager)
    cm_gen.save_toolchain_with_infile(cm_in, cm_out)

    with open(cm_out) as f:
        content = f.read()
        assert "# Initial CMake content" in content
        # The new generator at least writes a comment header
        assert "# Automatically generated by EDPM" in content


def test_cmake_presets_in_out(setup_test_environment):
    """
    1) Minimal plan, set cmake_presets_in/out
    2) Save presets
    3) Confirm final JSON merges
    """
    import json

    cm_in = os.path.join(TEST_TMP_DIR, "cmake_presets_in.json")
    cm_out = os.path.join(TEST_TMP_DIR, "cmake_presets_out.json")
    initial_json = '{"version": 3, "configurePresets": [{"name":"base"}]}'
    with open(cm_in, "w") as f:
        f.write(initial_json)

    api = _make_minimal_api()
    api.plan.data["global"]["config"].update({
        "cmake_presets_in": cm_in,
        "cmake_presets_out": cm_out
    })

    cm_gen = CmakeGenerator(plan=api.plan, lock=api.lock, recipe_manager=api.recipe_manager)
    cm_gen.save_presets_with_infile(cm_in, cm_out)

    # Quick substring check is still fine:
    with open(cm_out) as f:
        content = f.read()
        # We still confirm "version": 3 is there
        assert '"version": 3' in content

    # Now parse the JSON properly:
    with open(cm_out, "r") as f:
        data = json.load(f)

    # We expect 'version' = 3
    assert data["version"] == 3

    # Confirm that "base" is among the preset names
    presets = data.get("configurePresets", [])
    preset_names = [p.get("name", "") for p in presets]
    assert "base" in preset_names, f"Expected 'base' in {preset_names}"

    # If you want to ensure the generator added an “edpm” preset:
    # assert "edpm" in preset_names

