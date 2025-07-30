"""
This file provides information of how to build and configure Eigen3 packet:
https://gitlab.com/libeigen/eigen.git
"""

import os

from edpm.engine.generators.steps import CmakePrefixPath
from edpm.engine.composed_recipe import ComposedRecipe


class EigenRecipe(ComposedRecipe):
    """Provides data for building and installing Eicgen3 framework"""

    def __init__(self, config):

        # Default values for the recipe
        self.default_config = {
            'fetch': 'git',
            'make': 'cmake',
            'branch': '3.4.0',
            'url': 'https://gitlab.com/libeigen/eigen.git'
        }
        super().__init__(name='eigen3', config=config)


    @staticmethod
    def gen_env(data):
        """Generates environments to be set"""
        yield CmakePrefixPath(os.path.join(data['install_path'], 'share/eigen3/cmake/'))

