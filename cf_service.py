from cf_api import CodeforcesAPI
import grpc
import submission_pb2
import submission_pb2_grpc
from concurrent import futures

class CodeforcesService(submission_pb2_grpc.CodeforcesService):
    def __init__(self):
        self.cfApi = CodeforcesAPI()

    def GetSubmissions(self, request, context):
        status, submissions = self.cfApi.get_user_submissions(request.handle)
        
        if not status:
            print(submissions)
            if submissions == "CF API Error":
                for i in range(1):
                    yield submission_pb2.SubmissionReply(
                        status="CF API Error"
                    )
            elif submissions == f"handle: User with handle {request.handle} not found":
                for i in range(1):
                    yield submission_pb2.SubmissionReply(
                        status="User not found"
                    )
            else:
                for i in range(1):
                    yield submission_pb2.SubmissionReply(
                        status="Unknown error"
                    )
        else:
            print("Sending submissions")
            for submission in submissions:
                yield submission_pb2.SubmissionReply(
                    handle=submission["handle"],
                    contest_id=submission["contest_id"],
                    problem_index=submission["problem_index"],
                    sub_time=submission["sub_time"],
                    verdict=submission["verdict"],
                    problem_rating = submission["problem_rating"],
                    status="OK"
                )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    submission_pb2_grpc.add_CodeforcesServiceServicer_to_server(
        CodeforcesService(), server)

    addr = "localhost:8090"
    print(f"Codeforces service is listening on {addr}")
    server.add_insecure_port(addr)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
