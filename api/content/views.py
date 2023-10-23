from rest_framework.response import Response
from rest_framework.decorators import api_view
from .controller import getQuestions, getCorrectAnswer
from ..constant.constant import err

@api_view(['GET'])
def intro(req):
    return Response("Manezco Test API Framework")


@api_view(['GET'])
def fetchQuestions(req):
    try:
        pk = req.query_params.get('question') if 'question' in req.query_params else None

        questions = getQuestions(pk)

        if 'rawdata' in questions: 
            questions.pop('rawdata')

        return Response(questions)
    except Exception as e:
        err['detail'] = e
        return Response(err)

@api_view(['GET'])
def fetchCorrectAnswer(req):
    try:
        if not 'question' in req.query_params or not 'selected' in req.query_params:
            return Response({
                "err": True,
                "code": 400,
                "message": "Please provide question and selected answer"
            })
        
        selected = req.query_params.getlist('selected')
        selected = [int(s) for s in selected]

        question_id = int(req.query_params.get('question')[0])
        
        correctAnswer = getCorrectAnswer(question_id, selected)

        return Response(correctAnswer)
    except Exception as e:
        err['detail'] = e.__str__()
        return Response(err)

