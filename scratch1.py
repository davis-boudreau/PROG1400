from abc import ABC, abstractmethod
from typing import List, Optional

# =========================
# Base Abstract Class (UML: abstract class «Person»)
# =========================
class Person(ABC):
    """
    Represents a person in the system.
    UML: Abstract class with attributes: name:String, id:String
    """
    def __init__(self, name: str, id_: str):
        # Encapsulation: underscore indicates "protected" by convention
        self._name = name
        self._id = id_

    @property
    def name(self) -> str:
        """Encapsulated read access."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value:
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def id(self) -> str:
        """Typically read-only; no setter to preserve integrity."""
        return self._id

    @abstractmethod
    def get_role(self) -> str:
        """
        Polymorphic operation defined in UML (operation to be implemented by subclasses).
        """
        pass

    # Example of polymorphism-ready behavior
    @abstractmethod
    def summary(self) -> str:
        """
        Return a short text describing the person. Overridden by subclasses.
        """
        pass


# =========================
# Concrete Subclass (UML: «Student» inherits «Person»)
# =========================
class Student(Person):
    """
    Student with program and (encapsulated) GPA.
    UML: attributes: program:String, gpa:float
    """
    def __init__(self, name: str, id_: str, program: str, gpa: float = 0.0):
        super().__init__(name, id_)
        self.program = program
        self.__gpa = gpa  # Encapsulation: name-mangled private attribute

    @property
    def gpa(self) -> float:
        """Encapsulated read access to private GPA."""
        return self.__gpa

    @gpa.setter
    def gpa(self, value: float) -> None:
        if not (0.0 <= value <= 4.3):
            raise ValueError("GPA must be between 0.0 and 4.3.")
        self.__gpa = value

    def get_role(self) -> str:
        return "Student"

    def summary(self) -> str:
        return f"{self.get_role()}: {self.name} (#{self.id}) — Program: {self.program}, GPA: {self.gpa:.2f}"


# =========================
# Concrete Subclass (UML: «Instructor» inherits «Person»)
# =========================
class Instructor(Person):
    """
    Instructor with title and department.
    UML: attributes: title:String, department:String
    """
    def __init__(self, name: str, id_: str, title: str, department: str):
        super().__init__(name, id_)
        self.title = title
        self.department = department

    def get_role(self) -> str:
        return "Instructor"

    def summary(self) -> str:
        return f"{self.get_role()}: {self.title} {self.name} (#{self.id}) — Dept: {self.department}"


# =========================
# Support Class for Composition (UML: «Course»)
# =========================
class Course:
    """
    Course that aggregates Students and references an Instructor.
    UML: attributes: code:String, name:String
         relationships: Course 1..1 — teaches — 0..* Student (enrollment)
                        Course 1..1 — is taught by — 1 Instructor (association)
    """
    def __init__(self, code: str, name: str, instructor: Optional[Instructor] = None):
        self.code = code
        self.name = name
        self._instructor: Optional[Instructor] = instructor
        self._students: List[Student] = []  # Composition-like ownership of enrollments

    # Encapsulation via controlled methods
    def assign_instructor(self, instructor: Instructor) -> None:
        self._instructor = instructor

    def add_student(self, student: Student) -> None:
        if student in self._students:
            raise ValueError(f"Student {student.id} already enrolled.")
        self._students.append(student)

    def remove_student(self, student: Student) -> None:
        self._students.remove(student)

    @property
    def instructor(self) -> Optional[Instructor]:
        return self._instructor

    @property
    def students(self) -> List[Student]:
        # Return a shallow copy to protect internal list (encapsulation)
        return list(self._students)

    def roster(self) -> str:
        instr = self._instructor.summary() if self._instructor else "No instructor assigned."
        learners = "\n  ".join(s.summary() for s in self._students) or "No students enrolled."
        return f"Course {self.code} — {self.name}\nInstructor: {instr}\nStudents:\n  {learners}"


# =========================
# Polymorphism in Action (duck typing)
# =========================
def print_person_card(person: Person) -> None:
    """
    Demonstrates polymorphism: works with any subclass of Person.
    UML: operation taking base type demonstrates LSP/polymorphism.
    """
    # .summary() is polymorphic—subclasses provide their own behavior
    print(person.summary())


# =========================
# Example usage (can be treated as "unit test" or demo; not required by UML)
# =========================
if __name__ == "__main__":
    # Create instances based on UML types
    s1 = Student(name="Alex Green", id_="S1001", program="Computer Science", gpa=3.7)
    s2 = Student(name="Priya Singh", id_="S1002", program="Mathematics", gpa=3.9)

    i1 = Instructor(name="Dr. Rivera", id_="I2001", title="Prof.", department="Engineering")

    c1 = Course(code="ENGR200", name="Software Design")
    c1.assign_instructor(i1)
    c1.add_student(s1)
    c1.add_student(s2)

    # Polymorphism: both are Persons with different overridden summaries
    print_person_card(s1)
    print_person_card(i1)

    # Encapsulation demo: GPA validation via setter
    try:
        s1.gpa = 4.5  # raises ValueError
    except ValueError as e:
        print(f"[Validation] {e}")

    # Show course roster (composition + encapsulation)
    print("\n--- Course Roster ---")
    print(c1.roster())