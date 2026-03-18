REQUESTS_PER_MATCH = 4


def estimate_requests(matches):

    total = len(matches) * REQUESTS_PER_MATCH

    print("\nEstimated API requests:", total)

    return total