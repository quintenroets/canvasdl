from ...asset_types.assignment import Assignment
from . import base


class Checker(base.Checker):
    @property
    def path(self):
        return super().path / "Assignments"

    def get_items(self):
        return self.api.get_assignments()

    def make_item(self, item):
        assignment = Assignment.from_response(item)
        assignment.course = self.course
        return assignment
