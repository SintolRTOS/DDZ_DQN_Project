# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 20:07:27 2019

@author: wangjingyi
"""

import sys
sys.path.append("..")

from ddzmachine import environment
import ddzmachine.colors as colors
import collections
import six
import enum
import numpy as np
from ddzmachine.ddztable import DDZTable
from gym import spaces

class FeatureType(enum.Enum):
  SCALAR = 1
  CATEGORICAL = 2


class Feature(collections.namedtuple(
    "Feature", ["index", "name", "layer_set", "full_name", "scale", "type",
                "palette", "clip"])):
  """Define properties of a feature layer.

  Attributes:
    index: Index of this layer into the set of layers.
    name: The name of the layer within the set.
    layer_set: Which set of feature layers to look at in the observation proto.
    full_name: The full name including for visualization.
    scale: Max value (+1) of this layer, used to scale the values.
    type: A FeatureType for scalar vs categorical.
    palette: A color palette for rendering.
    clip: Whether to clip the values for coloring.
  """
  __slots__ = ()

  dtypes = {
      1: np.uint8,
      8: np.uint8,
      16: np.uint16,
      32: np.int32,
  }


class ScreenFeatures(collections.namedtuple("ScreenFeatures", [
    "height_map", "visibility_map", "creep", "power", "player_id",
    "player_relative", "unit_type", "selected", "unit_hit_points",
    "unit_hit_points_ratio", "unit_energy", "unit_energy_ratio", "unit_shields",
    "unit_shields_ratio", "unit_density", "unit_density_aa", "effects"])):
  """The set of screen feature layers."""
  __slots__ = ()

  def __new__(cls, **kwargs):
    feats = {}
    for name, (scale, type_, palette, clip) in six.iteritems(kwargs):
      feats[name] = Feature(
          index=ScreenFeatures._fields.index(name),
          name=name,
          layer_set="renders",
          full_name="screen " + name,
          scale=scale,
          type=type_,
          palette=palette(scale) if callable(palette) else palette,
          clip=clip)
    return super(ScreenFeatures, cls).__new__(cls, **feats)


class MinimapFeatures(collections.namedtuple("MinimapFeatures", [
    "height_map", "visibility_map", "creep", "camera", "player_id",
    "player_relative", "selected"])):
  """The set of minimap feature layers."""
  __slots__ = ()

  def __new__(cls, **kwargs):
    feats = {}
    for name, (scale, type_, palette) in six.iteritems(kwargs):
      feats[name] = Feature(
          index=MinimapFeatures._fields.index(name),
          name=name,
          layer_set="minimap_renders",
          full_name="minimap " + name,
          scale=scale,
          type=type_,
          palette=palette(scale) if callable(palette) else palette,
          clip=False)
    return super(MinimapFeatures, cls).__new__(cls, **feats)

SCREEN_FEATURES = ScreenFeatures(
    height_map=(256, FeatureType.SCALAR, colors.winter, False),
    visibility_map=(4, FeatureType.CATEGORICAL,
                    colors.VISIBILITY_PALETTE, False),
    creep=(2, FeatureType.CATEGORICAL, colors.CREEP_PALETTE, False),
    power=(2, FeatureType.CATEGORICAL, colors.POWER_PALETTE, False),
    player_id=(17, FeatureType.CATEGORICAL,
               colors.PLAYER_ABSOLUTE_PALETTE, False),
    player_relative=(5, FeatureType.CATEGORICAL,
                     colors.PLAYER_RELATIVE_PALETTE, False),
    unit_type=(1850, FeatureType.CATEGORICAL, colors.unit_type, False),
    selected=(2, FeatureType.CATEGORICAL, colors.SELECTED_PALETTE, False),
    unit_hit_points=(1600, FeatureType.SCALAR, colors.hot, True),
    unit_hit_points_ratio=(256, FeatureType.SCALAR, colors.hot, False),
    unit_energy=(1000, FeatureType.SCALAR, colors.hot, True),
    unit_energy_ratio=(256, FeatureType.SCALAR, colors.hot, False),
    unit_shields=(1000, FeatureType.SCALAR, colors.hot, True),
    unit_shields_ratio=(256, FeatureType.SCALAR, colors.hot, False),
    unit_density=(16, FeatureType.SCALAR, colors.hot, True),
    unit_density_aa=(256, FeatureType.SCALAR, colors.hot, False),
    effects=(16, FeatureType.CATEGORICAL, colors.effects, False),
)

MINIMAP_FEATURES = MinimapFeatures(
    height_map=(256, FeatureType.SCALAR, colors.winter),
    visibility_map=(4, FeatureType.CATEGORICAL, colors.VISIBILITY_PALETTE),
    creep=(2, FeatureType.CATEGORICAL, colors.CREEP_PALETTE),
    camera=(2, FeatureType.CATEGORICAL, colors.CAMERA_PALETTE),
    player_id=(17, FeatureType.CATEGORICAL, colors.PLAYER_ABSOLUTE_PALETTE),
    player_relative=(5, FeatureType.CATEGORICAL,
                     colors.PLAYER_RELATIVE_PALETTE),
    selected=(2, FeatureType.CATEGORICAL, colors.winter),
)

#选择策略0
ACTION_LOGIC_TYPE_ONE = 0
#选择策略1
ACTION_LOGIC_TYPE_TWO = 1
#选择策略2
ACTION_LOGIC_TYPE_THREE = 2
#选择策略3
ACTION_LOGIC_TYPE_FOUR = 3
#放弃出牌策略
ACTION_LOGIC_TYPE_CANCEL = 4
#选择策略的最大数量
ACTION_LOGIC_COUNT = 5

#特征矩阵宽度
FEATURE_MATIRX_HEIGHT = 6
#特征矩阵高度
FEATURE_MATRIX_WIDTH = 2
#特征矩阵深度
FEATURE_MATRIX_DEPTH = 20


class DDZEnv(environment.Base):
    """it's the ddz environment
    it's the class for support the information of RL interface
    """
    def __init__(self,
                 process_id,
                 table_id,
                 land_user,
                 train_user,
                 ddztable):
        """ create a ddz env.
        the process_id is the server process id value.
        the table_id is the ddz table's id value.
        the land_user is the position of the lander.
        the ddztable is the instance of the ddz's table
        """
        self.process_id = process_id
        self.table_id = table_id
        self.land_user = land_user
        self.train_user = train_user
        self.ddztable = ddztable
        self.observation_space = spaces.Box(low=0, high=255, shape=(FEATURE_MATIRX_HEIGHT, FEATURE_MATRIX_WIDTH, FEATURE_MATRIX_DEPTH), dtype=np.uint8)
        self._action_set = [ACTION_LOGIC_TYPE_ONE,ACTION_LOGIC_TYPE_TWO,ACTION_LOGIC_TYPE_THREE,ACTION_LOGIC_TYPE_FOUR,ACTION_LOGIC_TYPE_CANCEL]
        self.action_space = spaces.Discrete(len(self._action_set))
        self.out_card_list = []
    
    
    
    def observation_spec(self):
        """The observation spec for the ddz game environment.

        Returns:
          The dict of observation names to their tensor shapes. Shapes with a 0 can
          vary in length, for example the number of valid actions depends on which
          units you have selected.
        """
        return self.observation_space
    
    def action_spec(self):
        """Look at Features for full specs."""
        return self.action_space
    
    def get_obs(self):
        """with the ddzinfo obvervation information to be geted"""
        _obs = np.zeros((FEATURE_MATIRX_HEIGHT, FEATURE_MATRIX_WIDTH, FEATURE_MATRIX_DEPTH), dtype=np.uint8)
        if self.ddztable is not None and self.ddztable.started():
            self.out_card_list = self.ddztable.get_observation(_obs).copy()
        return _obs
    
    
    def reset(self):
        """Start a new episode."""
        if self.out_card_list is not None:
            self.out_card_list.clear()
        self.table_id = self.ddztable.gettableid()
        return self.get_obs()
    
    def render(self):
        return True
    
    def step(self, a):
        """Apply actions, step the world forward, and return observations."""
        done = False
        _obs = None
        reward = 0
        if self.ddztable.started() is False:
            done = True
        action = self._action_set[a]
        action_type = ACTION_LOGIC_TYPE_CANCEL
        out_card_result = None
        if self.out_card_list is not None:
            count = len(self.out_card_list)
            if action >= count:
                action_type = ACTION_LOGIC_TYPE_CANCEL
            else:
                action_type = action
        if action_type == ACTION_LOGIC_TYPE_ONE:
            out_card_result = self.out_card_list[0]
        elif action_type == ACTION_LOGIC_TYPE_TWO:
            out_card_result = self.out_card_list[1]
        elif action_type == ACTION_LOGIC_TYPE_THREE:
            out_card_result = self.out_card_list[2]
        elif action_type == ACTION_LOGIC_TYPE_FOUR:
            out_card_result = self.out_card_list[3]
        reward = self.do_action(action_type,out_card_result)
        _obs = self.get_obs()
        return _obs,reward,done,self.ddztable.started()
    
    def do_action(self,action_type,out_card_result):
        while True:
            if self.ddztable.wait():
                break
        reward = self.ddztable.get_train_reward()
        return reward
    
    def model_callback(self,local_vars,global_vars):
        
        return False

#env = DDZEnv(0,0,0,0,0)
#obs = env.observation_spec()
#print(str(obs))