import requests
import time


class CodeforcesAPI:
    def __init__(self):
        pass

    def api_response(self, url, params=None):
        try:
            tries = 0
            sleep_time = 1
            while tries < 5:
                tries += 1
                resp = requests.get(url)
                response = {}
                if resp.status_code == 503:
                    response['status'] = "FAILED"
                    response['comment'] = "limit exceeded"
                else:
                    response = resp.json()

                if response['status'] == 'FAILED' and 'limit exceeded' in response['comment'].lower():
                    print("Unable to get response from codeforces, trying again")
                    time.sleep(sleep_time)
                else:
                    return response
                sleep_time*=1.5
            return response
        except Exception as e:
            return None

    def get_user_submissions(self, handle):
        url = f"https://codeforces.com/api/user.status?handle={handle}"
        response = self.api_response(url)
        if not response:
            return [False, "CF API Error"]
        if response['status'] != 'OK':
            return [False, response['comment']]
        try:
            data = []
            for x in response['result']:
                y = x['problem']
                problem = {}

                problem["handle"] = handle

                if "rating" in y:
                    problem["problem_rating"] = y["rating"]
                else:
                    problem["problem_rating"] = None

                if "contestId" in y:
                    problem["contest_id"] = y["contestId"]
                else:
                    problem["contest_id"] = None

                if "index" in y:
                    problem["problem_index"] = y["index"]
                else:
                    problem["problem_index"] = None

                if "sub_time" in x:
                    problem["sub_time"] = x["creationTimeSeconds"]
                else:
                    problem["sub_time"] = None

                if 'verdict' in x:
                    problem['verdict'] = x['verdict']
                else:
                    problem['verdict'] = None

                data.append(problem)
            return [True, data]
        except Exception as e:
            print('hereis exception')
            return [False, str(e)]
