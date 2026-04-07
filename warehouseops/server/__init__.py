# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Warehouseops environment server components."""

try:
    from .warehouseops_environment import WarehouseopsEnvironment
except (ImportError, ModuleNotFoundError):
    try:
        from warehouseops.server.warehouseops_environment import WarehouseopsEnvironment
    except (ImportError, ModuleNotFoundError):
        from server.warehouseops_environment import WarehouseopsEnvironment

__all__ = ["WarehouseopsEnvironment"]
