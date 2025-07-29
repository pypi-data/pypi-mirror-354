"""TypeSig instances represent particular type signatures. The 'fast' method
provides a performant validation of a tuple of objects. The 'flex' method
attempts to cast each object in a tuple to the expected type. The latter is
substantially slower than the former."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..text import typeMsg
from ..waitaminute import CastMismatch, HashMismatch
from .casting import AbstractCast, Cast
from .zeroton import THIS
from . import PreClass

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, TypeAlias, Union, Iterator

  Types: TypeAlias = list[type]
  Casts: TypeAlias = tuple[AbstractCast, ...]
  TypeCasts: TypeAlias = dict[type, AbstractCast]
  Hash: TypeAlias = Union[PreClass, type]


class TypeSig:
  """TypeSig instances represent particular type signatures. The 'fast'
  method provides a performant validation of a tuple of objects. The
  'flex' method attempts to cast each object in a tuple to the expected
  type. The latter is substantially slower than the former."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private variables
  __raw_types__ = None
  __type_casts__ = None
  __hash_value__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getCasts(self, ) -> Casts:
    """Get the casts for the types."""
    out = []
    for type_ in self.__raw_types__:
      if type_ is THIS:
        raise RuntimeError('THIS not yet replaced!')
      out.append(Cast(type_))
    return (*out,)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *types: Any) -> None:
    """Initialize the TypeSig instance."""
    if len(types) == 1:
      if isinstance(types[0], tuple):
        types = types[0]
    self.__raw_types__ = types

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PYTHON API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self, ) -> Iterator[type]:
    """
    Implementation of iteration
    """
    yield from (self.__raw_types__ or ())

  def __hash__(self, ) -> int:
    """Forwards the hash to the hash of the types. If the replaceTHIS
    method has not been called, this will raise RuntimeError."""
    if self.__hash_value__ is None:
      return hash(self.__raw_types__)
    return self.__hash_value__

  def __eq__(self, other: object) -> bool:
    """Check if the other object is a TypeSig and has the same types."""
    cls = type(self)
    if not isinstance(other, cls):
      return self == cls(other)
    return True if hash(self) == hash(other) else False

  def __len__(self, ) -> int:
    """Get the length of the types."""
    return len(self.__raw_types__)

  def __str__(self, ) -> str:
    """String representation reflects the types. """
    typeStr = ', '.join([t.__name__ for t in self.__raw_types__])
    info = """%s: [%s]""" % (type(self).__name__, typeStr)
    return info

  def __repr__(self, ) -> str:
    """Code representation reflects the types. """
    typeStr = ', '.join([t.__name__ for t in self.__raw_types__])
    info = """%s(%s)""" % (type(self).__name__, typeStr)
    return info

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def replaceTHIS(self, cls: Hash) -> None:
    """Replace the 'THIS' type with the class."""
    newTypes = []
    for type_ in self.__raw_types__:
      if type_ is THIS or isinstance(type_, PreClass):
        newTypes.append(cls)
        continue
      newTypes.append(type_)
    self.__raw_types__ = (*newTypes,)
    self.__hash_value__ = hash(self.__raw_types__)

  def fast(self, *args) -> tuple:
    """Check if the types of the arguments match the types in the
    signature."""
    if len(args) == len(self):
      if hash(self) == hash((*[type(arg) for arg in args],)):
        return (*args,)
    raise HashMismatch(self, *args)

  def flex(self, *args) -> tuple:
    """Cast the arguments to the types in the signature."""
    if len(args) != len(self):
      if len(args) == 1:
        if isinstance(args[0], (list, tuple)):
          return self.fast(*args[0])
      raise HashMismatch(self, *args)
    casts = self.getCasts()
    types = self.__raw_types__
    out = []
    for arg, type_, cast in zip(args, types, casts):
      if not isinstance(type_, type):
        raise TypeError(typeMsg('type_', type_, type))
      try:
        if isinstance(arg, type_):
          out.append(arg)
        else:
          out.append(cast(arg))
      except CastMismatch:
        continue
      except RecursionError:
        continue
    return (*out,)
