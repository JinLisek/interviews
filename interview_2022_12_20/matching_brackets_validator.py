from .brackets_definitions import BracketsDefinition


class MatchingBracketValidator:
    def __init__(self, bracket_definitions: list[BracketsDefinition]) -> None:
        self.__closing_to_opening = {b.closing: b.opening for b in bracket_definitions}
        self.__bracket_stack: list[str] = []

    def do_brackets_match(self, txt: str) -> bool:
        for bracket in txt:
            if self._is_opening_bracket(bracket=bracket):
                self.__bracket_stack.append(bracket)
                continue
            if not self.__bracket_stack:
                return False
            if self.__bracket_stack.pop() != self.__closing_to_opening[bracket]:
                return False

        return not self.__bracket_stack

    def _is_opening_bracket(self, bracket: str) -> bool:
        return bracket in self.__closing_to_opening.values()
