import requests

LEETCODE_BASE_URL = 'https://leetcode.com'

def get_daily_question():
    url = 'https://leetcode.com/graphql'
    query = '''
    query {
    activeDailyCodingChallengeQuestion {
        date
        userStatus
        link
        question {
        title
        titleSlug
        difficulty
        content
        }
    }
    }
    '''

    response = requests.post(url, json={'query': query})
    data = response.json()
    return data['data']

# helpers to parse json response
def parse_question_name(data):
    return data['activeDailyCodingChallengeQuestion']['question']['title']

def parse_question_link(data):
    return LEETCODE_BASE_URL + data['activeDailyCodingChallengeQuestion']['link']

def parse_question_difficulty(data):
    return data['activeDailyCodingChallengeQuestion']['question']['difficulty']

def parse_question_content(data):
    return data['activeDailyCodingChallengeQuestion']['question']['content']

def parse_question_date(data):
    return data['activeDailyCodingChallengeQuestion']['date']