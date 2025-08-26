# Software Project Checker Winter 2025

## Introduction Into JACK and Checkers
At FRA UAS, we are collaborating on a learning tool called JACK, designed to support students in practicing and mastering a wide range of exercises. In JACK, instructors can create exercises of various types, including multiple-choice questions, dropdown selections, text fields, and even more complex tasks involving graphs and tree structures. Once the exercises are created, students can practice with them to deepen their knowledge and prepare for exams.

What makes JACK particularly powerful is its ability to provide detailed feedback. Instead of simply indicating whether an answer is “correct” or “wrong,” JACK allows instructors to define rules that automatically evaluate the student’s submission and provide feedback about what was done incorrectly or where a mistake may have occurred. This approach works very well for simpler exercises, such as multiple-choice questions. For example, a rule can easily detect whether the correct box was selected and, if the student selects a wrong option—or multiple wrong options—JACK can generate predefined, tailored feedback explaining the errors.

However, as we move to more complex exercises, such as tasks involving graphs or tree structures, rule-based evaluation becomes insufficient. For instance, if a student is asked to delete a node in a binary search tree, which is a exercise type we have invented in JACK, evaluating their submission with simple rules is too complex and not support by JACK internally. In these cases, JACK relies on checkers, which we will be developing this semester.

A checker is a microservice, packaged as a Docker container, designed to evaluate complex tasks programmatically. Normally, when a student submits an exercise, JACK evaluates it using the predefined rules and provides immediate feedback. For complex exercises, however, the submission is sent to a checker. The checker receives a request containing both the exercise definition and the student’s submission. It can then programmatically unpack the request, solve the exercise itself, and compare its solution to the student’s submission. This process allows JACK to provide detailed feedback and, if necessary, supply the correct solution to help students learn effectively.

This semester, you will be developing one of these checkers for priority queue or avl tree exercises depending on the group, contributing directly to the evaluation of complex exercises in JACK. But before diving into development, we will go through the workflow and implementation step by step to ensure a solid understanding of how checkers operate.




TODO
- Short intro into the project (Why are you doing this? --> JACK)
- Step-by-step guide (Start with 00_Python_Installation, etc.)
- Description of Milestones
- Contact opportunities (E-Mail)




## Milestones
We will have two Milestones in this semester. One roughly at the halfway point and one at the end.

### Milestone 1
When?

### Milestone 2