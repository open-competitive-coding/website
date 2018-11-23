# This script add's a correct submission that a user has made.

import os
import json
from shutil import copyfile

# Constants
readme_json = "README.json"
template_json = "data/README.json"
template_submission_json = "data/Submissions.json"
template_readme = "data/README.md"

"""
First we will check if the contest for the problem exists.
If No, we will create a folder by the contest name and add a README.json there.
If there exists a folder, we will modify the README.json and create a new README.md.
"""
def add_submission(user_id, problem_id) :
    # Problem-Id's will be like 1729-A or 122-B
    contest_id, problem_name = problem_id.split("-")

    readme_json_path = contest_id + "/" + readme_json

    # Checking whether folder exists.
    if not os.path.isdir(contest_id) :
        os.mkdir(contest_id)

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
    table_header_row = """<tr><th>User</th><th>Problems Solved</th><th>Score</th></tr>"""
    table_body = ""
    for sub in submissions :
        problems_solved = ", ".join(sub["problems-solved"])
        table_body += "<tr><td>{user}</td><td>{problems_solved}</td><td>{score}</td></tr>".format(user=sub["user-id"],problems_solved=problems_solved,score=sub["score"])
    table = "<table>" + table_header_row + table_body + "</table>"
    return table


# This function converts the JSON data to a pretty looking README.
def json_to_readme(contest_id, contest_data) :
    # We will read from the template README.md and populate the json
    with open(template_readme, "r") as template_readme_file :
        content = template_readme_file.read()
        score_table = create_table_from_submissions(contest_data["submissions"])
        content = content.format(contest_id=contest_id, score_table=score_table)
        with open(contest_id + "/" + "README.md", "w") as readme_file :
            readme_file.write(content)

if __name__ == "__main__" :
    add_submission("rohith", "example-B")
