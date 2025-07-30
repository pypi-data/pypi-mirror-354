import os
import sys

if __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from serato_tools.smart_crate import SmartCrate

if __name__ == "__main__":
    for p in os.listdir(SmartCrate.DIR_PATH):
        crate = SmartCrate(os.path.join(SmartCrate.DIR_PATH, p))
        crate.print()

        def modify_rule(rule: SmartCrate.Rule):
            if rule.field != SmartCrate.RULE_FIELD["grouping"]:
                return rule
            print(rule.get_value(SmartCrate.Fields.RULE_VALUE_TEXT))
            rule.set_value(SmartCrate.Fields.RULE_VALUE_TEXT, "UNTr")
            return rule

        crate.modify_rules(modify_rule)
        crate.save()
