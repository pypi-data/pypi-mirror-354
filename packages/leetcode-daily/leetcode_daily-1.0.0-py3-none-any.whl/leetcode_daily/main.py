from .leetcode import *
def main():
    data = get_daily_question()
    
    question_name = parse_question_name(data)
    question_link = parse_question_link(data)
    question_difficulty = parse_question_difficulty(data)
    question_content = parse_question_content(data)
    question_date = parse_question_date(data)

    print(f"Question Name: {question_name}")
    print(f"Link: {question_link}")
    print(f"Difficulty: {question_difficulty}")
    # print(f"Content: {question_content}")
    print(f"Date: {question_date}")

if __name__ == '__main__':
    main()