import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


#testes unitários do commit 2:

# 1 e 2. validação de points
def test_question_points_below_min():
    with pytest.raises(Exception):
        Question(title="Q1", points=0)


def test_question_points_above_max():
    with pytest.raises(Exception):
        Question(title="Q1", points=101)


# 3 e 4. validação de texto da choice
def test_add_choice_empty_text():
    question = Question(title="Q1")
    with pytest.raises(Exception):
        question.add_choice("", False)


def test_add_choice_text_too_long():
    question = Question(title="Q1")
    with pytest.raises(Exception):
        question.add_choice("x" * 101, False)


# 5. ids sequenciais
def test_add_choice_sequential_ids():
    question = Question(title="Q1")
    choice1 = question.add_choice("A", False)
    choice2 = question.add_choice("B", False)
    choice3 = question.add_choice("C", False)

    assert choice1.id == 1
    assert choice2.id == 2
    assert choice3.id == 3


# 6 e 7. remoção
def test_remove_choice_by_id_success():
    question = Question(title="Q1")
    choice1 = question.add_choice("A", False)
    choice2 = question.add_choice("B", False)

    question.remove_choice_by_id(choice1.id)

    assert len(question.choices) == 1
    assert question.choices[0].id == choice2.id


def test_remove_choice_by_id_invalid():
    question = Question(title="Q1")
    question.add_choice("A", False)

    with pytest.raises(Exception):
        question.remove_choice_by_id(12345)


# 8. limpar lista
def test_remove_all_choices():
    question = Question(title="Q1")
    question.add_choice("A", False)
    question.add_choice("B", True)

    question.remove_all_choices()

    assert len(question.choices) == 0


# 9. marcar corretas
def test_set_correct_choices():
    question = Question(title="Q1")
    choice1 = question.add_choice("A", False)
    choice2 = question.add_choice("B", False)
    choice3 = question.add_choice("C", False)

    question.set_correct_choices([choice1.id, choice3.id])

    assert question.choices[0].is_correct is True
    assert question.choices[1].is_correct is False
    assert question.choices[2].is_correct is True


# 10. retornar apenas ids corretos
def test_correct_selected_choices():
    question = Question(title="Q1", max_selections=3)
    choice1 = question.add_choice("A", True)
    choice2 = question.add_choice("B", False)
    choice3 = question.add_choice("C", True)

    selected = [choice1.id, choice2.id, choice3.id]
    result = question.correct_selected_choices(selected)

    assert result == [choice1.id, choice3.id] 



@pytest.fixture
def sample_question():
    question = Question(title="Capital de Minas Gerais?", max_selections=2)

    c1 = question.add_choice("Belo Horizonte", True)
    c2 = question.add_choice("Rio de Janeiro", False)
    c3 = question.add_choice("São Paulo", True)

    return question 

def test_sample_question_has_three_choices(sample_question):
    assert len(sample_question.choices) == 3

def test_correct_selected_choices_exceeds_max(sample_question):
    selected_ids = [choice.id for choice in sample_question.choices]

    with pytest.raises(Exception):
        sample_question.correct_selected_choices(selected_ids)