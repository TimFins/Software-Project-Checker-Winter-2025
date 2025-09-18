# Software Project Checker Winter 2025

## Introduction Into JACK and Checkers

At FRA-UAS, we are collaborating on a learning tool called JACK, designed to support students in practicing and mastering a wide range of exercises. In JACK, instructors can create exercises of various types, including multiple-choice questions, dropdown selections, text fields, and even more complex tasks involving graphs and tree structures. Once the exercises are created, students can practice with them to deepen their knowledge and prepare for exams.

What makes JACK particularly powerful is its ability to provide detailed feedback. Instead of simply indicating whether an answer is "correct" or "wrong," JACK allows instructors to define rules that automatically evaluate the student's submission and provide feedback about what was done incorrectly or where a mistake may have occurred. This approach works very well for simpler exercises, such as multiple-choice questions. For example, a rule can easily detect whether the correct box was selected and, if the student selects a wrong option--or multiple wrong options--JACK can generate predefined, tailored feedback explaining the errors.

However, as we move to more complex exercises, such as tasks involving graphs or tree structures, rule-based evaluation becomes insufficient. For instance, if a student is asked to delete a node in a binary search tree, which is a exercise type we have invented in JACK, evaluating their submission with simple rules is too complex and not supported by JACK internally. In these cases, JACK relies on checkers, which we will be developing this semester.

A checker is a microservice, packaged as a Docker container, designed to evaluate complex tasks programmatically. Normally, when a student submits an exercise, JACK evaluates it using the predefined rules and provides immediate feedback. For complex exercises, however, the submission is sent to a checker. The checker receives a request containing both the exercise definition and the student's submission. It can then programmatically unpack the request, solve the exercise itself, and compare its solution to the student's submission. This process allows JACK to provide detailed feedback and, if necessary, supply the correct solution to help students learn effectively.

This semester, you will be developing one of these checkers for priority queue or AVL tree exercises depending on the group, contributing directly to the evaluation of complex exercises in JACK. But before diving into development, we will go through the workflow and implementation step by step to ensure a solid understanding of how checkers operate.

## Plan

We have created this repository to contain the most important information for you to successfully participate in this project.

This repository contains the required information and source code. Each directory contains a `README.md`, which tells you what you should do in each directory.

We would like you to work on the contents of this repository in this order:

- `00_Python_Installation`: Install Python and the required dependencies. (**~XXh**)
- `01_Python_Introduction`: Get started with Python if you are not familiar with it. (**~XXh**)
- `02_Example_List_Sorting_Evaluation`: Check out a simple example project, where we show you how such an evaluation service works, so that you get an idea of how you could implement one yourself. (**~XXh**)
- `03_Insomnia_Installation`: Get to know how to use Insomnia, which is a piece of software for being able to organize HTTP requests, which we would highly recommend you to test your evaluation service. (**~XXh**)
- `04_Test_BST_RBT_Checker`: Try out the evaluation service, which we have created last semester for binary search trees and red-black trees. Get a feeling for what kind of feedback such an evaluation service could produce. (**~XXh**)
- `05_AVL_Tree`/`05_Priority_Queue` (_Depending on your topic_): Look at the source code and explanation of the topics you have to create an evaluation service for. You have to adapt the source code for the class you are supposed to use. (**~XXh**)
- `06_AVL_Tree_Checker`/`06_Priority_Queue_Checker` (_Depending on your topic_): Contains documentation for what inputs your evaluation service receives and in what format. Also contains documentation of the classes, which you need to use to implement the evaluation service. (**~XXh**)
- `checker`: This is the actual source code, where you will develop your service. All previous directories are just additional material. This directory is where all the development takes place and all resources are located.

## Meetings

At the start, we want to do a weekly meeting with each team, where we get updated on progress and current plans. The goal of those meetings is for us to be sure that you can continue working without any uncertainties that need to be resolved.

Each meeting is only for one team, and an appointment will be discussed with each team individually.

## Milestones

We will have two Milestones this semester. One roughly at the halfway point and one at the end of the project. The presentations will be given not just in front of us and your direct team members, but also the other participants working on other checker.

### Milestone 1

The first milestone will consist of a presentation of roughly **10 minutes per person**. We are currently aiming for a presentation date in the week **27.10.2025 - 02.11.2025**. The exact time and date will be determined later.

In said presentation we want to see the general concepts you have thought of for this project. Here are just some examples of what we mean by concepts:

- How do you adjust the score?
    - Do you calculate the correctness percentage and give points according to that?
    - Do you start with a score of 100 and deduct points for each mistake?
    - Maybe even another approach?
- Weighting of tasks/errors?
    - Are some errors treated more harshly or more leniently?
- Do you consider follow-up errors in some way?
- Do you define a cut-off point, where you say, that the student's submission is so convoluted, that it would not be beneficial for the student to show detailed feedback?

We would also like you to highlight popular mistakes that students could make and how you want to address them.

We just want to make sure that you are on the right path and can keep on working. For that, we would welcome a rough plan, like what to work on next, and so on.

### Milestone 2 Contents

The second milestone will be the final presentation, which takes place at the very last appointment of our project, which should be in the week **08.12.2025 - 14.12.2025**.

There we want to see your final work product. So please present anything which you may find useful for us or the other project participants to know.

We would like to see some examples, where you show an exercise, the student's submission and explain what feedback that student would receive.

You could also explain how you structured your service and how you organized the codebase.

When showing code snippets or similar, please keep in mind that it should be easy to see during the presentation. Keep a readable font size in mind and try to omit UI components, which have nothing to do with what you want to show (e.g., Editor menus).

### Deliverables

#### GitHub Contributions/Diary

In order to be able to have your lecturer grade every one of you **individually**, we need to know what each person's responsibilities were and what they worked on. For this, there are two options. Our preferred option would be that everyone uses GitHub, and we track individual contributions via GitHub commits. Alternatively, those who do not wish to use GitHub must instead maintain a detailed spreadsheet, where they track their contributions for every week and send it to us at the end of the project. We would rather avoid that, but we do leave this option available for those not wanting to use GitHub. **Without GitHub commits (or alternatively a diary), your lecturer cannot properly grade your contributions to the code!**

#### Presentation Slides

For both presentations, we would like to get your presentation slides beforehand, so that we can prepare. We will likely want you to send us your presentation slides the week before each presentation. But more information will follow once we have a time and date for the presentations themselves.

We want a single person from your group to send us the presentation slides **as PDF** per E-Mail and put all other team members into CC.

#### Codebase

Before the final presentation, we want you to send us your codebase, which will also be graded.

Please make sure to send us your final version, where all pending changes were applied. Please download the repository as a ZIP file and just send it to us like this. Please also do not forget to export your Insomnia test cases into a YAML file and include it into the project if you were using Insomnia for testing. You can just replace the requests file in the directory `/checker` with your updated version including additional requests.

While we do not require a separate code documentation document, we want you to document every important function using [Docstrings](https://peps.python.org/pep-0257/) explaining what the purpose of said function is and providing [type hints](https://peps.python.org/pep-0484/) for parameters and return values where appropriate. Here is an example:

```python
def get_missing_values(student_values: list[int], required_values: list[int]) -> set[int]:
    """Determine the set of values, which should be present in the student's submission but are missing instead.
    """
    ...
```

We want a single person of your group to send us the codebase **as a single ZIP file** per E-Mail at the end of the project and put all other team members into CC.

## Contact Opportunities

If you have any questions, then please go ahead and send us an E-Mail. Here are our E-Mail addresses:
- Tim Finmans: tim.finmans@stud.fra-uas.de
- Edward Späth: edward.spaeth@stud.fra-uas.de

Please send each E-Mail to both of us by putting both of us in the recipient field or putting one of us as the recipient and the other one into CC.
