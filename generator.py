import sys
import os
import glob
import shutil
from subprocess import call
from shutil import copyfile
from school_infos import *

# Style: https://google.github.io/styleguide/pyguide.html#Naming
MAIN_FILE_NAME = 'Duc.SOP.tex'
VARIABLES_FILE_NAME = 'variables.tex'
COMMON_CONTENT_FILE_NAME = 'common_content.tex'
COMMON_INTRO_FILE_NAME = 'common_intro.tex'
PHD_PLAN_FILE_NAME = 'phd_plan.tex'
CONCLUSION_FILE_NAME = 'conclusion.tex'
TEMPLATE_DIR_PATH = 'template'
OUTPUT_DIR_NAME = 'output'
ALL_BIB_FILE_NAME = 'all.bib'

def get_template_file_path(template_file_name):
    return TEMPLATE_DIR_PATH + os.sep + template_file_name

class SchoolSpecificPdfGenerator:
    def __init__(self, school_info):
        self.school_info = school_info
        self.specific_variables_file_name = self.create_specific_file_name_with_prefix(VARIABLES_FILE_NAME)
        self.specific_phd_plan_file_name = self.create_specific_file_name_with_prefix(PHD_PLAN_FILE_NAME)
        self.specific_conclusion_file_name = self.create_specific_file_name_with_prefix(CONCLUSION_FILE_NAME)
        self.specific_main_file_name = self.create_specific_file_name_with_prefix(MAIN_FILE_NAME)

    # Duc.SOP depends on comment_content, and specific variables and phd_plan_and_conclusion
    def generate_pdf(self):
        self.copy_file_name_from_template_to_output(COMMON_INTRO_FILE_NAME)
        self.copy_file_name_from_template_to_output(ALL_BIB_FILE_NAME)
        self.copy_file_name_from_template_to_output(COMMON_CONTENT_FILE_NAME)
        self.create_specific_variables()
        self.create_specific_phd_plan()
        self.create_specific_conclusion()
        self.create_specific_main_file()
        self.generate_specific_pdf()

    def generate_specific_pdf(self):
        os.chdir(OUTPUT_DIR_NAME)

        pdflatex_cmd = 'pdflatex.exe -synctex=1 -interaction=nonstopmode ' + self.specific_main_file_name
        print pdflatex_cmd
        call(pdflatex_cmd.split(' '))

        # generating bbl needs aux which is created by pdflatex
        bibtex_cmd = 'bibtex.exe ' + os.path.splitext(self.specific_main_file_name)[0]
        print bibtex_cmd
        call(bibtex_cmd.split(' '))

        call(pdflatex_cmd.split(' '))

        os.chdir('..')

    def copy_file_name_from_template_to_output(self, file_name):
        output_common_content_path = self.add_output_path(file_name)
        template_common_content_path = get_template_file_path(file_name)
        copyfile(template_common_content_path, output_common_content_path)

    def create_specific_file_name_with_prefix(self, file_name):
        return self.school_info.file_name_prefix + '_' + file_name

    def add_output_path(self, filename):
        return OUTPUT_DIR_NAME + os.sep + filename

    def create_specific_variables(self):
        specific_variables_file_path = self.add_output_path(self.specific_variables_file_name)
        with open(specific_variables_file_path, "wt") as fout:
            fout.write('\\renewcommand{\\schoolnameshort}{' + self.school_info.school_name_short + '}\n')
            fout.write('\\renewcommand{\\department}{' + self.school_info.department + '}\n')
            fout.write('\\renewcommand{\\researchinterests}{' + self.school_info.research_interests + '}\n')

    def create_specific_phd_plan(self):
        self.create_specific_file_with_content(self.specific_phd_plan_file_name, self.school_info.phd_plan)

    def create_specific_conclusion(self):
        self.create_specific_file_with_content(self.specific_conclusion_file_name, self.school_info.conclusion)

    def create_specific_file_with_content(self, specific_file_name, content):
        specific_phd_plan_and_conclusion_file_path = self.add_output_path(specific_file_name)
        with open(specific_phd_plan_and_conclusion_file_path, "wt") as fout:
            fout.write(content)

    # change template include file names into specific file names in the template file
    def create_specific_main_file(self):
        specific_main_file_path = self.add_output_path(self.specific_main_file_name)
        template_main_file_path = get_template_file_path(MAIN_FILE_NAME)
        with open(specific_main_file_path, "wt") as fout:
            with open(template_main_file_path, "rt") as fin:
                for line in fin:
                    if line == '\\input{variables}\n':
                        fout.write('\\input{' + self.specific_variables_file_name + '}\n')
                    elif line == '\input{phd_plan}\n':
                        fout.write('\\input{' + self.specific_phd_plan_file_name + '}\n')
                    elif line == '\input{conclusion}\n':
                        fout.write('\\input{' + self.specific_conclusion_file_name + '}\n')
                    else:
                        fout.write(line)

def delete_files_with_ext_in_dir(dir_name, extension):
    filelist = [f for f in os.listdir(dir_name) if f.endswith(os.extsep + extension)]
    for file in filelist:
        delete_path = dir_name + os.sep + file
        print 'Delete ' + delete_path
        os.remove(delete_path)

if __name__ == "__main__":
    delete_files_with_ext_in_dir(OUTPUT_DIR_NAME, "pdf")

    applied_schools = [
        (UMICH_SHORT_NAME, COMPUTER_SCIENCE_AND_ENGINEERING)
    ]

    for school_info in school_infos:
        if (school_info.school_name_short, school_info.department) in applied_schools:
            generator = SchoolSpecificPdfGenerator(school_info)
            generator.generate_pdf()

    # delete the files which were not generated
    generated_file_names = [f for f in os.listdir(OUTPUT_DIR_NAME) if f.endswith(os.extsep + 'pdf')]
    existing_files_in_current_dir = [f for f in os.listdir('.') if f.endswith(os.extsep + 'pdf')]
    for f in existing_files_in_current_dir:
        if f not in generated_file_names:
            delete_path = '.' + os.sep + f
            print 'Delete ' + delete_path
            os.remove(delete_path)

    # copy all generated pdf files to current dir
    files = glob.iglob(os.path.join(OUTPUT_DIR_NAME, "*.pdf"))
    for f in files:
        if os.path.isfile(f):
            shutil.copy2(f, '.')
