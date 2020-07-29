prompt = '''Input: list files
Output: ls -l

Input: Count files in a directory
Output: ls -l | wc -l

Input: Disk space used by home directory
Output: du ~

Input: Replace foo with bar in all .py files
Output: sed -i .bak -- 's/foo/bar/g' *.py

Input: Delete the models subdirectory
Output: rm -rf ./models'''

template = '''

Input: {}
Output:'''

import os, click, openai

while True:
    request = input(click.style("nlsh> ", "red"), bold=True)
    prompt += template.format(request)
    result = openai.Completion.create(
        model="davinci", prompt=prompt, stop="\n", max_tokens=100, temperature=0.0
    )
    command = result.choices[0]['text']
    prompt += command
    print(command)
