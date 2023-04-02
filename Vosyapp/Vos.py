from flask import Flask

from flask_restful import Api, Resource, reqparse

from sqlalchemy import create_engine, Column, Integer, String, JSON, Float, DateTime

from sqlalchemy.orm import sessionmaker

from datetime import datetime

app = Flask(__name__)

api = Api(app)

db_engine = create_engine('sqlite:///surveys.db')

Session = sessionmaker(bind=db_engine)

class Survey(Resource):

    def get(self):

        session = Session()

        surveys = session.query(SurveyModel).all()

        return {'surveys': [s.serialize() for s in surveys]}

    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('questionid', type=str, required=True)

        parser.add_argument('question', type=str, required=True)

        parser.add_argument('answers', type=str, required=True)

        parser.add_argument('opening_time', type=int, required=True)

        args = parser.parse_args()

        session = Session()

        survey = SurveyModel(

            questionid=args['questionid'],

            question=args['question'],

            answers=args['answers'],

            opening_time=args['opening_time'],

            status='opening',

            timestamp=datetime.now()

        )

        session.add(survey)

        session.commit()

        return survey.serialize(), 201

class SurveyDetail(Resource):

    def get(self, survey_id):

        session = Session()

        survey = session.query(SurveyModel).get(survey_id)

        if not survey:

            return {'message': 'Survey not found'}, 404

        return survey.serialize()

    def put(self, survey_id):

        parser = reqparse.RequestParser()

        parser.add_argument('question', type=str, required=True)

        parser.add_argument('answers', type=str, required=True)

        args = parser.parse_args()

        session = Session()

        survey = session.query(SurveyModel).get(survey_id)

        if not survey:

            return {'message': 'Survey not found'}, 404

        survey.question = args['question']

        survey.answers = args['answers']

        session.commit()

        return survey.serialize()

    def delete(self, survey_id):

        session = Session()

        survey = session.query(SurveyModel).get(survey_id)

        if not survey:

            return {'message': 'Survey not found'}, 404

        session.delete(survey)

        session.commit()

        return '', 204

class SurveyVote(Resource):

    def post(self, survey_id):

        parser = reqparse.RequestParser()

        parser.add_argument('vote', type=str, required=True)

        args = parser.parse_args()

        session = Session()

        survey = session.query(SurveyModel).get(survey_id)

        if not survey:

            return {'message': 'Survey not found'}, 404

        if survey.status != 'opening':

            return {'message': 'Survey is not currently open for voting'}, 400

        if args['vote'] not in survey.answers:

            return {'message': 'Invalid vote'}, 400

        vote = VoteModel(survey_id=survey_id, vote=args['vote'], timestamp=datetime.now())

        session.add(vote)

        session.commit()

        return '', 204

class SurveyClose(Resource):

    def post(self, survey_id):

        session = Session()

        survey = session.query(SurveyModel).get(survey_id)

        if not survey:

            return {'message': 'Survey not found'}, 404

        if survey.status != 'opening':

            return {'message': 'Survey is not currently open for voting'}, 400

        survey.status = 'closed'

        session.commit()

        return survey.serialize()

class SurveyCount

