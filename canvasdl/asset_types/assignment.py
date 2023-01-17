from dataclasses import dataclass
from datetime import datetime
from typing import Any

import dateutil.parser

from ..asset_types import SaveItem
from ..asset_types.canvas import Asset
from ..utils import calendar, time
from .course import Course


@dataclass
class Assignment(Asset, SaveItem):
    created_at: str
    created_at_date: datetime
    updated_at: str
    updated_at_date: datetime
    lock_at: str | None
    unlock_at: str | None
    description: str | None
    due_at: str | None
    points_possible: float
    grading_type: Any
    assignment_group_id: int
    grading_standard_id: int | None
    peer_reviews: Any
    automatic_peer_reviews: Any
    position: int
    grade_group_students_individually: Any
    anonymous_peer_reviews: Any
    group_category_id: Any
    post_to_sis: Any
    moderated_grading: Any
    omit_from_final_grade: Any
    intra_group_peer_reviews: Any
    anonymous_instructor_annotations: Any
    anonymous_grading: Any
    graders_anonymous_to_graders: Any
    grader_count: Any
    grader_comments_visible_to_graders: Any
    final_grader_id: Any
    grader_names_visible_to_final_grader: Any
    allowed_attempts: Any
    annotatable_attachment_id: Any
    secure_params: Any
    lti_context_id: Any
    course_id: Any
    name: Any
    submission_types: Any
    has_submitted_submissions: Any
    due_date_required: Any
    max_name_length: Any
    in_closed_grading_period: Any
    graded_submissions_exist: Any
    is_quiz_assignment: Any
    can_duplicate: Any
    original_course_id: Any
    original_assignment_id: Any
    original_lti_resource_link_id: Any
    original_assignment_name: Any
    original_quiz_id: Any
    workflow_state: Any
    important_dates: Any
    muted: bool
    html_url: str
    published: bool
    only_visible_to_overrides: Any
    locked_for_user: bool
    submissions_download_url: Any
    post_manually: Any
    anonymize_students: Any
    require_lockdown_browser: Any
    due_at_date: datetime = None
    unlock_at_date: datetime = None
    lock_at_date: datetime = None
    allowed_extensions: Any = None
    quiz_id: int = None
    anonymous_submissions: bool = False
    lock_explanation: Any = None
    lock_info: Any = None

    course: Course = None

    def save(self):
        if self.due_at:
            due = dateutil.parser.parse(self.due_at)
            message = self.course.assignment_name(self.name)
            calendar.add_todo(message, date=due)

    @property
    def display_title(self):
        time_str = time.export_time(self.due_at) if self.due_at else ""
        return f"{self.name} ({time_str})"

    @property
    def save_id(self):
        return self.id
