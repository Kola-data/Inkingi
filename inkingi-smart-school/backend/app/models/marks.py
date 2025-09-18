from sqlalchemy import Column, String, Float, ForeignKey, Integer, Date, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import TenantModel


class Assignment(TenantModel):
    __tablename__ = "assignments"
    
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id"), nullable=False)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    total_marks = Column(Float, nullable=False)
    weight = Column(Float, default=1.0, nullable=False)  # Weight in final grade
    due_date = Column(Date, nullable=True)
    
    # Relationships
    course = relationship("Course", back_populates="assignments")
    term = relationship("Term", back_populates="assignments")
    marks = relationship("AssignmentMark", back_populates="assignment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Assignment {self.title}>"


class Exam(TenantModel):
    __tablename__ = "exams"
    
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id"), nullable=False)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    
    name = Column(String(200), nullable=False)  # e.g., "Mid-term Exam", "Final Exam"
    exam_date = Column(Date, nullable=False)
    total_marks = Column(Float, nullable=False)
    weight = Column(Float, default=1.0, nullable=False)  # Weight in final grade
    duration_minutes = Column(Integer, nullable=True)
    
    # Relationships
    course = relationship("Course", back_populates="exams")
    term = relationship("Term", back_populates="exams")
    marks = relationship("ExamMark", back_populates="exam", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Exam {self.name}>"


class AssignmentMark(TenantModel):
    __tablename__ = "assignment_marks"
    __table_args__ = (
        UniqueConstraint("assignment_id", "student_id", name="uq_assignment_student"),
    )
    
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignments.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    
    marks_obtained = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)  # Computed: (marks_obtained/total_marks) * 100
    grade = Column(String(5), nullable=True)  # e.g., "A", "B+", "C"
    remarks = Column(Text, nullable=True)
    marked_by = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=True)
    marked_at = Column(Date, nullable=True)
    
    # Relationships
    assignment = relationship("Assignment", back_populates="marks")
    student = relationship("Student", back_populates="assignment_marks")
    
    def __repr__(self):
        return f"<AssignmentMark {self.student_id} - {self.marks_obtained}>"


class ExamMark(TenantModel):
    __tablename__ = "exam_marks"
    __table_args__ = (
        UniqueConstraint("exam_id", "student_id", name="uq_exam_student"),
    )
    
    exam_id = Column(UUID(as_uuid=True), ForeignKey("exams.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    
    marks_obtained = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)  # Computed: (marks_obtained/total_marks) * 100
    grade = Column(String(5), nullable=True)  # e.g., "A", "B+", "C"
    remarks = Column(Text, nullable=True)
    marked_by = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=True)
    marked_at = Column(Date, nullable=True)
    
    # Relationships
    exam = relationship("Exam", back_populates="marks")
    student = relationship("Student", back_populates="exam_marks")
    
    def __repr__(self):
        return f"<ExamMark {self.student_id} - {self.marks_obtained}>"


class ReportCard(TenantModel):
    __tablename__ = "report_cards"
    __table_args__ = (
        UniqueConstraint("student_id", "term_id", "class_id", name="uq_report_card"),
    )
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id"), nullable=False)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    
    # Aggregated scores
    total_marks = Column(Float, nullable=False)
    average_marks = Column(Float, nullable=False)
    position = Column(Integer, nullable=True)  # Position in class
    out_of = Column(Integer, nullable=True)  # Total students in class
    
    # Performance summary (JSON)
    subjects_summary = Column(String, nullable=True)  # JSON with subject-wise performance
    
    # Teacher's remarks
    class_teacher_remarks = Column(Text, nullable=True)
    head_teacher_remarks = Column(Text, nullable=True)
    
    # Status
    is_published = Column(String, default="false", nullable=False)
    published_at = Column(Date, nullable=True)
    
    # Relationships
    student = relationship("Student", back_populates="report_cards")
    term = relationship("Term", back_populates="report_cards")
    
    def __repr__(self):
        return f"<ReportCard {self.student_id} - Term {self.term_id}>"