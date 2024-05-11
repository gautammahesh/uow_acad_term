from abc import ABC, abstractmethod
import datetime

class Course:
    def __init__(self, course_code,  course_name, credit):
        self.__course_code = course_code
        self.__course_name = course_name
        self.__credit = credit

    def get_course_code(self):
        return self.__course_code
    
    def get_credits(self):
        return self.__credit

    def __str__(self):
        return f"Code: {self.__course_code} || Name: {self.__course_name} || Credit: {self.__credit}"
    
class Student:
    def __init__(self, student_id,  student_name):
        self.__student_id = student_id
        self.__student_name = student_name

    def get_student_id(self):
        return self.__student_id

    def __str__(self):
        return f"Student ID: {self.__student_id} || Student Name: {self.__student_name}"
    
# ===========================================================================================================

class Result(ABC):
    def __init__(self, student,  course):
        self.__student = student
        self.__course = course
        # self.__course_cred = course_credit

    # Add a method to calculate the total overall score for the course
    def calculate_total_score(self):
        # Get the overall score for the current result
        overall_score = self.get_score()

        # If the current result is an instance of both PracticalResult and CourseResult
        if isinstance(self, PracticalResult) and isinstance(self, CourseResult):
            # Calculate the total score by adding the scores from both practical and course
            overall_score += self.get_practical_score() + self.get_course_score()
    
        return overall_score

    @abstractmethod
    def get_score(self):
        pass

    def get_grade(self):
        if self.calculate_total_score() >= 80: 
            # Points: 4
            return "A"  
        elif self.calculate_total_score() >= 70 and self.calculate_total_score() <= 79:
            # Points: 3
            return "B"  
        elif self.calculate_total_score() >= 60 and self.calculate_total_score() <= 69:
            # Points: 2
            return "C"  
        elif self.calculate_total_score() >= 50 and self.calculate_total_score() <= 59:
            # Points: 1
            return "D"  
        else:
            # Points: 0
            return "F"  
        
    def get_points(self):
        if self.get_grade() == "A":
            return 4
        elif self.get_grade() == "B":
            return 3
        elif self.get_grade() == "C":
            return 2
        elif self.get_grade() == "D":
            return 1
        else:
            return 0
        
    def get_gpa(self, results):
        for result in results:
            print("From get_gpa", result)

        total_credit_points = 0
        total_credits = 0
        for result in results:
            total_credit_points += result._Result__course.get_credits() * result.get_points()
            total_credits += result._Result__course.get_credits()
        if total_credits == 0:
            print("No credits found.")
            return
        gpa = total_credit_points / total_credits
        print("GPA:", gpa)
            
      
      
        
    def __str__(self):
        return f"Student ID = {self.__student.get_student_id()} || Course Code: {self.__course.get_course_code()} || Score: {self.calculate_total_score()} || Grade: {self.get_grade()}"

   
# ===========================================================================================================
    # dont forget to remove points, credits
    # they are only for testing purpose
class PracticalResult(Result):
    def __init__(self, student, course, p_score1, p_score2, p_score3):
        super().__init__(student,  course)
        self.__p_score1 = p_score1
        self.__p_score2 = p_score2
        self.__p_score3 = p_score3

    def get_score(self):
        return (self.__p_score1 + self.__p_score2 + self.__p_score3)/3

    def __str__(self):
        return f"Student ID = {self._Result__student.get_student_id()} || Course Code: {self._Result__course.get_course_code()} || Credits: {self._Result__course.get_credits()} || Practical 1: {self.__p_score1} || Practical 2: {self.__p_score2} || Practical 3: {self.__p_score3} || Overall Score: {self.get_score()} ||  Grade: {self.get_grade()} || Points: {self.get_points()}"

    
    # dont forget to remove points, credits
    # they are only for testing purpose
class CourseResult(Result):
    def __init__(self, student, course, cw_score, ex_score ) :
        super().__init__(student, course)
        self._cw_score = cw_score
        self._ex_score = ex_score

    def get_score(self):
        return (self._cw_score * 0.4) + (self._ex_score * 0.6)

    def __str__(self):
          return f"Student ID = {self._Result__student.get_student_id()} || Course Code: {self._Result__course.get_course_code()} || Credits: {self._Result__course.get_credits()} || Corse Score: {self._cw_score} || Exam Score: {self._ex_score} || Overall Score: {self.get_score()} || Grade: {self.get_grade()} || Points: {self.get_points()}"
       
# ===========================================================================================================

class AcadTerm:
    def __init__(self, term, start_date, end_date):
        self.__term = term
        self.__start_date = start_date
        self.__end_date = end_date
        self.__results = []
         
    def add_result(self, result):
        for rslt in self.__results:
            if result._Result__student.get_student_id() == rslt._Result__student.get_student_id() and result._Result__course.get_course_code() == rslt._Result__course.get_course_code():
                print("Result already exists in academic term.")
                return False
        self.__results.append(result)
        return True

    def remove_result(self, result):
        for rslt in self.__results:
            if result._Result__student.get_student_id() == rslt._Result__student.get_student_id() and result._Result__course.get_course_code() == rslt._Result__course.get_course_code():
                self.__results.remove(rslt)
                return True
        print("Result does not exist in academic term.")
        return False

    def get_result(self): 
        get_all_result = ""
        for result in self.__results:
            get_all_result += f"Results: {result}\n"
        return get_all_result
        
    def get_result_summary(self):
        passes = 0
        failures = 0
        for result in self.__results:
            if result.get_grade() == "A" or result.get_grade() == "B" or result.get_grade() == "C" or result.get_grade() == "D":
                passes += 1
            else:
                failures += 1
        return f"Term: {self.__term} || Number of Passes: {passes} || Number of failures: {failures}"
    
    def search_result(self):
        while True:
            searcher = input("Enter Student ID / Course Code (or type 'done' to finish): ")
            if searcher.lower() == 'done':
                break
            result_found = False
            # result_arr = []
            for result in self.__results:
                if isinstance(result, PracticalResult) or isinstance(result, CourseResult):
                    if searcher == result._Result__student.get_student_id() or searcher == result._Result__course.get_course_code(): 
                        if not result_found:
                            print("Result Found:")
                            result_found = True
                        print(result)
                        # result_arr.append(result)
            # result.get_gpa(result_arr)
            if not result_found:
                print("Result not found. Please Try again...")

    def search_gpa(self):
        while True:
            searcher = input("Enter Student Id to get GPA (or type 'done' to finish): ")
            if searcher.lower() == 'done':
                break
            result_found = False
            result_arr = []
            for result in self.__results:
                if isinstance(result, PracticalResult) or isinstance(result, CourseResult):
                    if searcher == result._Result__student.get_student_id(): 
                        if not result_found:
                            print("Result Found....Obtaining GPA")
                            result_found = True
                        print(result)
                        result_arr.append(result)
            result.get_gpa(result_arr)
            if not result_found:
                print("Result not found. Please Try again...")
    
    def __str__(self):
        return f"Term: {self.__term} || Start: {self.__start_date} || End: {self.__end_date}"

def test1():
    # AcadTerm.search_result(result)
    # to see working of course and student info

    print("Student class")
    student1 = Student("103" , "Loren")
    student2 = Student("108", "Koda")
    print(student1)
    print(student2,"\n")

    print("Course class")
    course1 = Course("2011", "Mathematic python", 6)
    course2 = Course("3067", "Computer Science", 6)
    print(course1)
    print(course2,"\n")

    print("Practical result class")
    practiclResult1 = PracticalResult(student1, course1, 80, 74, 65)
    practiclResult2 = PracticalResult(student2, course1, 28, 30, 47)
    print(practiclResult1)
    print(practiclResult2,"\n")

    print("Course result class")
    courseResult1 = CourseResult(student2, course2, 82,94)
    courseResult2 = CourseResult(student1, course2, 42,29)

    print(courseResult1)
    print(courseResult2,"\n")

    print("AcadTerm class")
    term1 = AcadTerm("2024 Q1", "2024-01-01", "2024-05-31")
    print(term1,"\n")

    term1.add_result(practiclResult1)
    term1.add_result(courseResult1)
    term1.add_result(practiclResult2)
    term1.add_result(courseResult2)
    # term1.remove_result(courseResult1)
    # term1.remove_result(courseResult1)
    # term1.add_result(practiclResult1)


    print("Results added....")
    print("Summary:")
    print(term1.get_result_summary(),"\n")

    print("Testing get_result method:")
    print(term1.get_result())
    

    print("\nTesting search_result:")
    term1.search_result()
    print("\n")

    print("\nTesting search_GPA:")
    term1.search_gpa()

def main():
    test1()
main()
