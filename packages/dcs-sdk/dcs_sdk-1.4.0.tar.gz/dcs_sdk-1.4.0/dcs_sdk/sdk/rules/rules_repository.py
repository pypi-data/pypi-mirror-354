#  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import copy
from typing import Optional
from uuid import UUID

from loguru import logger

from dcs_sdk.sdk.rules.rules_mappping import get_rules_to_func_mapping


# CENTRALIZED REPO FOR ALL THE RULES
# RULE NAME -> ALL ITS PROPERTIES
class RulesRepository:
    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    def __init__(self):
        self.rules = {}
        self.rules_mapping = get_rules_to_func_mapping()
        self.value_rules = []
        self.schema_rules = {}

    def register(self, id: UUID, rule_dict: dict):
        """
        Registers a rule in the centralized repository.
        Supports both 'schema' and 'value' rules.

        - For value rules: transformation is a string template
        - For schema rules: transformation is a function name (to be resolved)
        """
        rule_type = rule_dict.get("type")

        if not rule_type:
            return

        if rule_type == "schema_override":
            func_name = rule_dict.get("transformation")
            if func_name:
                func = self.rules_mapping.get(func_name)
                if not func:
                    raise ValueError(f"Function '{func_name}' not found in registry")
                rule_dict["function"] = func
                rule_dict["function_name"] = func_name

        self.rules[id] = rule_dict

    def register_schema_rules(self, schema_rules: list):
        self.schema_rules = schema_rules

    def register_value_rules(self, value_rules: list):
        self.value_rules = value_rules

    def get(self, id: UUID) -> Optional[dict]:
        return self.rules.get(id)

    def apply_schema_rules(self, src_col: dict, tgt_col: dict) -> tuple[bool, str | None]:
        """
        Performs baseline schema checks and overrides them if corresponding rules are configured.
        Returns (True, None) if all checks pass.
        Returns (False, reason) if any check fails.
        """

        schema_rule_function_mapping = {}
        for schema_rule in self.schema_rules:
            rule_obj = self.get(schema_rule)
            if rule_obj:
                func_name = rule_obj.get("function_name")
                params = rule_obj.get("params")
                function = rule_obj.get("function")
                schema_rule_function_mapping[func_name] = {"params": params, "func": function}

        def is_rule_allowed(rule_name: str, fallback_check: bool) -> bool:
            if rule_name not in schema_rule_function_mapping:
                return fallback_check
            rule_obj = schema_rule_function_mapping[rule_name]
            func = rule_obj.get("func")
            params = rule_obj.get("params")
            return func(src_col, tgt_col, params) if func else fallback_check

        if src_col["data_type"].lower() != tgt_col["data_type"].lower():
            if not is_rule_allowed("allow_equivalent_data_types", False):
                return False, f"Data type mismatch"

        if src_col.get("character_maximum_length") != tgt_col.get("character_maximum_length"):
            if not is_rule_allowed("ignore_column_length_difference", False):
                return False, f"Length mismatch"

        if src_col.get("numeric_precision") != tgt_col.get("numeric_precision"):
            if not is_rule_allowed("ignore_numeric_precision_difference", False):
                return False, f"Numeric precision mismatch"

        if src_col.get("numeric_scale") != tgt_col.get("numeric_scale"):
            if not is_rule_allowed("ignore_numeric_scale_difference", False):
                return False, f"Numeric scale mismatch"

        if src_col.get("datetime_precision") != tgt_col.get("datetime_precision"):
            if not is_rule_allowed("ignore_datetime_precision_difference", False):
                return False, f"Datetime precision mismatch"

        return True, None
