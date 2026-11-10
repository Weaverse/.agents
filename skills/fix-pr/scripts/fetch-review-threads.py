#!/usr/bin/env python3
"""Read live inline threads without changing a PR. Requires authenticated gh."""
import argparse
import json
import re
import subprocess
import sys

THREADS = """
query($owner: String!, $repo: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      headRefOid
      reviewThreads(first: 100, after: $cursor) {
        nodes {
          id isResolved isOutdated path line
          comments(first: 100) {
            nodes { id url body createdAt originalCommit { oid } commit { oid } }
            pageInfo { hasNextPage endCursor }
          }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}
"""
COMMENTS = """
query($id: ID!, $cursor: String) {
  node(id: $id) {
    ... on PullRequestReviewThread {
      comments(first: 100, after: $cursor) {
        nodes { id url body createdAt originalCommit { oid } commit { oid } }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}
"""
HEAD = """
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) { pullRequest(number: $number) { headRefOid } }
}
"""


def graphql(query, **variables):
    command = ['gh', 'api', 'graphql', '-f', 'query=' + query]
    for key, value in variables.items():
        if value is not None:
            command.extend(['-F' if isinstance(value, int) else '-f', f'{key}={value}'])
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    payload = json.loads(result.stdout)
    if payload.get('errors') or not payload.get('data'):
        raise ValueError('GraphQL returned errors or no data; no partial result emitted')
    return payload['data']


def next_cursor(connection, seen):
    info = connection['pageInfo']
    if not info['hasNextPage']:
        return None
    cursor = info['endCursor']
    if not cursor or cursor in seen:
        raise ValueError('Missing or repeated pagination cursor')
    seen.add(cursor)
    return cursor


def collect(owner, repo, number):
    variables = dict(owner=owner, repo=repo, number=number)
    cursor, head = None, None
    seen, threads = set(), []
    while True:
        pr = graphql(THREADS, **variables, cursor=cursor)['repository']['pullRequest']
        if not pr:
            raise ValueError('PR not found or not accessible')
        if head is not None and head != pr['headRefOid']:
            raise ValueError('PR head changed during collection; rerun on a stable head')
        head = pr['headRefOid']
        connection = pr['reviewThreads']
        for thread in connection['nodes']:
            if thread['isResolved'] or thread['isOutdated']:
                continue
            comments = thread.pop('comments')
            nodes = list(comments['nodes'])
            comment_seen = set()
            comment_cursor = next_cursor(comments, comment_seen)
            while comment_cursor:
                comments = graphql(COMMENTS, id=thread['id'], cursor=comment_cursor)['node']['comments']
                nodes.extend(comments['nodes'])
                comment_cursor = next_cursor(comments, comment_seen)
            for comment in nodes:
                original = comment.pop('originalCommit')
                current = comment.pop('commit')
                comment['original_commit_id'] = original['oid'] if original else None
                comment['commit_id'] = current['oid'] if current else None
            thread['comments'] = nodes
            threads.append(thread)
        cursor = next_cursor(connection, seen)
        if cursor is None:
            break
    latest = graphql(HEAD, **variables)['repository']['pullRequest']['headRefOid']
    if latest != head:
        raise ValueError('PR head changed during collection; rerun on a stable head')
    return dict(repository=f'{owner}/{repo}', number=number, head=head, threads=threads)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', help='OWNER/REPO')
    parser.add_argument('number', type=int)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repository) or args.number < 1:
        parser.error('Expected OWNER/REPO and a positive PR number')
    try:
        result = collect(*args.repository.split('/'), args.number)
    except (OSError, subprocess.CalledProcessError, ValueError, KeyError, TypeError) as error:
        print(f'Review collection failed ({type(error).__name__}); no result emitted', file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
