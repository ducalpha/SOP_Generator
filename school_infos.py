
school_infos = []

# convert each character to lower case, convert space to _, ignore commas
def normalize(name):
    name = name.lower()
    new_name = ""
    for c in name:
        if c.isalpha():
            new_name += c
        elif c.isspace():
            new_name += '_'
    return new_name

class SchoolInfo:
    def __init__(self, school_name_short, school_name_full, department, research_interests, school_strong_research_fields, phd_plan):
        self.school_name_short = school_name_short
        self.school_name_full = school_name_full
        self.department = department
        self.file_name_prefix = normalize(self.school_name_short + ' ' + self.department)  # stanford, ucb
        self.research_interests = research_interests
        self.school_strong_research_fields = school_strong_research_fields
        self.phd_plan = phd_plan
        self.conclusion = ""

    def generate_conclusion(self, conclusion_template, professor_list, short_name_with_the=False):
        school_name_short_form = self.school_name_short
        if short_name_with_the:
            school_name_short_form = 'the ' + school_name_short_form
        self.conclusion = conclusion_template.format(professor_list=professor_list, department=self.department, school_name_short=school_name_short_form,
                                                     school_name_full=self.school_name_full, school_strong_research_fields=self.school_strong_research_fields)
general_conclusion = \
    "I am impressed by {school_name_short}'s superior research quality and innovations in {school_strong_research_fields}. " \
    "I especially find the projects of {professor_list} incredibly exciting and fully aligned with my research interests. " \
    "For the above reasons, I sincerely want to join the {department} Ph.D. program at {school_name_full}."

practical_impl_and_theory_sentence = 'I am interested in practical implementations with in-depth analysis and strong theoretical backgrounds. '
previous_experience_sentence = "I have confidence that my previous experience in the energy efficiency and networking on mobile systems will be helpful to make further contributions to the field."

large_scale_networked_app_sentence = "I want to build robust and secure architectures and algorithms for large-scale networked applications. "

##### Distributed systems and networking #######
# UMich
UMICH_SHORT_NAME = 'University of Michigan'
COMPUTER_SCIENCE_AND_ENGINEERING = 'Computer Science and Engineering'
umich_phd_plan = \
    "I aspire to do research on improving the performance, efficiency, and security of computer networks, mobile systems, and cloud computing. " \
    + large_scale_networked_app_sentence \
    + practical_impl_and_theory_sentence + previous_experience_sentence
info = SchoolInfo(UMICH_SHORT_NAME, 'the University of Michigan', COMPUTER_SCIENCE_AND_ENGINEERING,
                  'operating systems, computer networks, and mobile computing', 'computer networks and operating systems', umich_phd_plan)
info.generate_conclusion(general_conclusion, 'Professors Z. Morley Mao, Jason Flinn, and Kang G. Shin')
school_infos.append(info)

