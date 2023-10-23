from base.models import Question, PossibleAnswer, Lesson
from .serializers import QuestionSerializer
from random import randrange

def getPossibleAnswer(question_id):
    answers = [{"id": a.id, "possible_answer": a.possible_answer} for a in PossibleAnswer.objects.filter(question_id=question_id)]
  
    return answers

def getLesson(id):
    lesson = [l.title for l in Lesson.objects.filter(pk=id)][0]
    
    return lesson

def getQuestions(pk):
    l1 = [randrange(1, 5, 1), randrange(1, 5, 1)]
    while l1[1] == l1[0]:
        l1[1] = randrange(1, 5, 1)

    
    l2 = [randrange(6, 10, 1), randrange(6, 10, 1)]
    while l2[1] == l2[0]:
        l2[1] = randrange(6, 10, 1)

    questions = None
    if pk == None or pk == '':
        questions = Question.objects.filter(pk__in=[*l1, *l2])
    else:
        if type(pk) != int:
            return {
                "err": True,
                "code": 400,
                "message": "Question must be a positive number" 
            }
        
        questions = Question.objects.filter(pk=pk)

    serializer = QuestionSerializer(questions, many="True")

    for serial in serializer.data:
        serial['possible_answers'] = getPossibleAnswer(question_id=serial['id'])
        serial['lesson_name'] = getLesson(id=serial['lesson_id'])

    return {
        "err": False,
        "code": 200,
        "data": serializer.data,
    }

def calculateScore(answer, expected, is_multiple):
    score = 10
    worth = score / len(expected)
    stype = 'z'

    if not is_multiple:
        if len(answer) != len(expected) or answer[0] != expected[0]:
            stype = 'd'
        else: 
            stype = 'y'

        return 10 if answer[0] == expected[0] else 0, stype

    countok = 0
    for ans in answer:
        if ans != '' and ans in expected:
            countok = countok + 1
            stype = 'b'
    

    penalty = False
    if len(answer) > len(expected) and countok == len(expected):
        penalty = True
        stype = 'c'
    
    if countok == 0:
        stype = 'a'
        
    if len(answer) == len(expected) and countok == len(expected):
        stype =  'z'  

    return ((countok * worth) if len(expected) >= countok else 0) - (2 if penalty else 0), stype


def getCorrectAnswer(question_id, answer):
    if sum([type(i) == int and i > 0 for i in answer]) != len(answer):
        return {
            "err": True,
            "code": 400,
            "message": "Answers must be a positive number" 
        }
    
    if type(question_id) != int:
        return {
            "err": True,
            "code": 400,
            "message": "Question must be a positive number" 
        }

    question = getQuestions(question_id)['data'][0]
    
    correctanswers = [a.id for a in PossibleAnswer.objects.filter(question_id=question_id, is_correct=True)]
    correctanswerstext = [a.possible_answer for a in PossibleAnswer.objects.filter(question_id=question_id, is_correct=True)]
    score, stype = calculateScore(answer, correctanswers, is_multiple=question['is_multiple'])
    message = {
        'a': f"None of your answers are correct. The answers should be [{', '.join(str(r) for r in correctanswerstext)}]",
        'b': f"Part of your answers are correct. The answers should be [{', '.join(str(r) for r in correctanswerstext)}]",
        'c': f"You have selected answers that are incorrect, penalty applied. The answers should be [{', '.join(str(r) for r in correctanswerstext)}]",
        'd': f"You are incorrect! The answers is {correctanswerstext[0]}",
        'y': f"You are correct! The answers is {correctanswerstext[0]}",
        'z': f"You are correct! The answers are [{', '.join(str(r) for r in correctanswerstext)}]"
    }[stype]

    return {
        "err": False,
        "code": 200,
        "message": message,
        "data": {
            "score": score
        }
    }

