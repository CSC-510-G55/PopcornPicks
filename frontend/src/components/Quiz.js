import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../Quiz.css';

const API_BASE_URL = process.env.REACT_APP_API_URL;

const Quiz = () => {
	const navigate = useNavigate();
	const [quiz, setQuiz] = useState([]);
	const [userAnswers, setUserAnswers] = useState({});
	const [showResults, setShowResults] = useState(false);
	const [score, setScore] = useState(0);

	useEffect(() => {
		const fetchQuiz = async () => {
			try {
				const response = await axios.get(`${API_BASE_URL}/quiz`);
				setQuiz(response.data);
			} catch (error) {
				console.error('Quiz fetch error:', error);
			}
		};
		fetchQuiz();
	}, []);

	const handleAnswerChange = (questionId, answer) => {
		setUserAnswers((prevAnswers) => ({
			...prevAnswers,
			[questionId]: answer
		}));
		console.log(userAnswers);
	};

	const handleSubmit = async () => {
		try {
			const answersPayload = {
				answers: Object.entries(userAnswers).map(([questionId, answer]) => ({
					question_id: questionId,
					answer: answer
				}))
			};

			const response = await axios.post(`${API_BASE_URL}/quiz`, answersPayload, {
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (response.status === 200) {
				setScore(response.data.score);
				setShowResults(true);
			}
		} catch (error) {
			console.error('Quiz submission error:', error);
		}
	};

	return (
		<div className='quiz-page'>
			{showResults ? (
				<div className='results-container bg-dark text-center'>
					<h1 className='result px-5 py-5 text-white'>Quiz Results</h1>
					<p className='score px-5'>
						You scored {score} out of {quiz.length}
					</p>
					<button className='btn btn-primary mb-5' onClick={() => navigate('/landing')}>
						Go back to landing page
					</button>
				</div>
			) : (
				<div className='quiz-container bg-dark text-center'>
					<h1 className='pt-5'>Quiz</h1>
					{quiz.map((question, index) => (
						<div key={question._id || index} className='question-container my-5'>
							<p className='question px-5 text-align-left text-white'>{question.question}</p>
							<div className='answers-container px-5 width-100'>
								{question.answers.map((answer, idx) => (
									<label key={idx} className='answer-option px-2'>
										<input
											type='radio'
											name={`question-${question._id || index}`} // Use _id for unique name per question
											value={answer}
											onChange={() => handleAnswerChange(question._id, answer)} // Pass _id as identifier
											checked={userAnswers[question._id] === answer} // Check if answer is selected
										/>
										{answer}
									</label>
								))}
							</div>
						</div>
					))}
					<button className='btn btn-primary mb-5' onClick={handleSubmit}>
						Submit
					</button>
				</div>
			)}
		</div>
	);
};

export default Quiz;
