# This script add's a correct submission that a user has made.

import os
import json
import sys
from shutil import copyfile
from constants import *

# Constants
readme_json = "README.json"
readme_md = "README.md"
template_json = "data/README.json"
template_submission_json = "data/Submissions.json"
template_readme = "data/README.md"
contest_prefix = "Contest-"

"""
First we will check if the contest for the problem exists.
If No, we will create a folder by the contest name and add a README.json there.
If there exists a folder, we will modify the README.json and create a new README.md.
"""
def add_submission(user_id, problem_id) :
    # Problem-Id's will be like 1729-A or 122-B
    print user_id, problem_id
    contest_id, problem_name = problem_id.split("-")

    readme_json_path = contest_prefix+contest_id + "/" + readme_json

    # Checking whether folder exists.
    if not os.path.isdir(contest_prefix+contest_id) :
        os.mkdir(contest_prefix+contest_id)

        # We will copy a template json
        copyfile(template_json, readme_json_path)

    contest_data = {}
    with open(readme_json_path, "r") as readme_json_file :
        contest_data = json.load(readme_json_file)

    new_user = True
    index = 0
    for item in contest_data["submissions"] :
        if item["user-id"] == user_id :
            new_user = False
            if problem_id in item["problems-solved"] :
                pass
            else :
                item["problems-solved"].append(problem_id)
                item["score"] += 1
            contest_data["submissions"][index] = item
    if new_user :
        with open(template_submission_json, "r") as template_submission_json_file :
            template_submission = json.load(template_submission_json_file)
            template_submission["user-id"] = user_id
            template_submission["problems-solved"] = [problem_id]
            template_submission["score"] = 1
            contest_data["submissions"].append(template_submission)


    with open(readme_json_path, "w") as readme_json_file :
        json.dump(contest_data, readme_json_file, indent=4)

    json_to_readme(contest_id, contest_data)


def create_table_from_submissions(submissions) :
    cols = ""
    table_body = ""

    cols += TH.format(data="User")
    cols += TH.format(data="Problems Solved")
    cols += TH.format(data="Score")

    table_header_row = TR.format(cols=cols)

    for sub in submissions :
        # TODO: Convert this to a lin which redirects to the problem itself.
        problems_solved = ", ".join(sub["problems-solved"]) # This is how we obtain the problems solved string

        cols = ""
        cols += TD.format(data=ANCHOR.format(href=GITHUB_USER_URL.format(user_id=sub["user-id"]), data=sub["user-id"]))# We add the user-id
        cols += TD.format(data=problems_solved) # We add the problems solved by the user
        cols += TD.format(data=sub["score"]) # We add the score

        table_body += TR.format(cols=cols)
    table = TABLE.format(rows=table_header_row+table_body)

    return table


# This function converts the JSON data to a pretty looking README.
def json_to_readme(contest_id, contest_data) :
    # We will read from the template README.md and populate the json
    with open(template_readme, "r") as template_readme_file :
        content = template_readme_file.read()
        score_table = create_table_from_submissions(contest_data["submissions"])
        content = content.format(contest_id=contest_id, score_table=score_table)
        with open(contest_prefix + contest_id + ".md", "w") as readme_file :
            readme_file.write(content)

if __name__ == "__main__" :
    add_submission(sys.argv[1], sys.argv[2])
