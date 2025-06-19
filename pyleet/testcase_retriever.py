"""
Module for retrieving test cases from LeetCode using their GraphQL API.
"""

import json
import re
import requests
from typing import List, Tuple, Optional, Union, Any


class LeetCodeAPIError(Exception):
    """Exception raised when LeetCode API requests fail."""
    pass


class TestCaseRetriever:
    """
    Class for retrieving test cases from LeetCode problems.
    """

    GRAPHQL_URL = "https://leetcode.com/graphql"

    # GraphQL query to get problem details including test cases
    QUESTION_QUERY = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            title
            titleSlug
            content
            difficulty
            exampleTestcases
            sampleTestCase
            metaData
            isPaidOnly
            hints
            topicTags {
                name
                slug
            }
        }
    }
    """

    def __init__(self):
        self.session = requests.Session()
        # Set headers to mimic a browser request
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/json',
            'Referer': 'https://leetcode.com/',
        })

    def get_problem_by_id(self, problem_id: int) -> Optional[str]:
        """
        Get the title slug for a problem by its ID.

        Args:
            problem_id (int): The LeetCode problem ID

        Returns:
            str: The title slug of the problem, or None if not found
        """
        # Query to get problem list and find by ID
        query = """
        query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
            problemsetQuestionList: questionList(
                categorySlug: $categorySlug
                limit: $limit
                skip: $skip
                filters: $filters
            ) {
                total: totalNum
                questions: data {
                    questionId
                    titleSlug
                }
            }
        }
        """

        variables = {
            "categorySlug": "",
            "limit": 3000,  # Get a large number to ensure we find the problem
            "skip": 0,
            "filters": {}
        }

        try:
            response = self.session.post(
                self.GRAPHQL_URL,
                json={"query": query, "variables": variables},
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            if 'errors' in data:
                raise LeetCodeAPIError(f"GraphQL errors: {data['errors']}")

            questions = data.get('data', {}).get(
                'problemsetQuestionList', {}).get('questions', [])

            for question in questions:
                if question.get('questionId') == str(problem_id):
                    return question.get('titleSlug')

            return None

        except requests.RequestException as e:
            raise LeetCodeAPIError(f"Failed to fetch problem list: {e}")

    def get_question_data(self, title_slug: str) -> dict:
        """
        Get detailed question data from LeetCode GraphQL API.

        Args:
            title_slug (str): The title slug of the problem (e.g., "two-sum")

        Returns:
            dict: Question data from LeetCode API

        Raises:
            LeetCodeAPIError: If the API request fails
        """
        variables = {"titleSlug": title_slug}

        try:
            response = self.session.post(
                self.GRAPHQL_URL,
                json={"query": self.QUESTION_QUERY, "variables": variables},
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            if 'errors' in data:
                raise LeetCodeAPIError(f"GraphQL errors: {data['errors']}")

            question_data = data.get('data', {}).get('question')
            if not question_data:
                raise LeetCodeAPIError(f"Problem '{title_slug}' not found")

            return question_data

        except requests.RequestException as e:
            raise LeetCodeAPIError(f"Failed to fetch question data: {e}")

    def parse_test_cases(self, question_data: dict) -> List[Tuple[Any, Any]]:
        """
        Parse test cases from LeetCode question data.

        Args:
            question_data (dict): Question data from LeetCode API

        Returns:
            List[Tuple[Any, Any]]: List of (input, expected_output) tuples
        """
        test_cases = []

        # Get example test cases
        example_testcases = question_data.get('exampleTestcases', '')
        sample_testcase = question_data.get('sampleTestCase', '')

        # Use exampleTestcases if available, otherwise fall back to sampleTestCase
        testcase_data = example_testcases or sample_testcase

        if not testcase_data:
            return test_cases

        # Parse metadata to understand the function signature
        metadata = question_data.get('metaData', '{}')
        try:
            meta = json.loads(metadata)
        except json.JSONDecodeError:
            meta = {}

        # Split test cases by lines and process them
        lines = [line.strip()
                 for line in testcase_data.strip().split('\n') if line.strip()]

        # Get parameter information
        params = meta.get('params', [])
        param_count = len(params)

        if param_count == 0:
            # If we can't determine parameter count, try to infer from the data
            return self._parse_generic_test_cases(lines)

        # LeetCode test case format is typically:
        # For each test case: input1, input2, ..., inputN (N = param_count)
        # But the expected outputs are not included in exampleTestcases
        # We need to extract them from the problem content or use sample cases

        # For now, let's parse what we have and try to infer the pattern
        # The format appears to be: input_param1, input_param2, ..., input_paramN repeated

        # Try to group inputs by parameter count
        test_case_groups = []
        i = 0
        while i + param_count <= len(lines):
            inputs = []
            try:
                for j in range(param_count):
                    input_val = self._parse_value(lines[i + j])
                    inputs.append(input_val)

                test_case_groups.append(inputs)
                i += param_count
            except:
                i += 1

        # Since LeetCode's exampleTestcases doesn't include expected outputs,
        # we need to extract them from the problem content
        content = question_data.get('content', '')
        expected_outputs = self._extract_expected_outputs_from_content(
            content, len(test_case_groups))

        # Combine inputs with expected outputs
        for i, inputs in enumerate(test_case_groups):
            if i < len(expected_outputs):
                expected = expected_outputs[i]

                # Format inputs based on parameter count
                if param_count == 1:
                    test_cases.append((inputs[0], expected))
                else:
                    test_cases.append((inputs, expected))

        return test_cases

    def _extract_expected_outputs_from_content(self, content: str, num_cases: int) -> List[Any]:
        """
        Extract expected outputs from the problem content HTML.

        Args:
            content (str): HTML content of the problem
            num_cases (int): Number of test cases to extract

        Returns:
            List[Any]: List of expected outputs
        """
        expected_outputs = []

        # Look for patterns like "Output: [0,1]" or "Output: 2" in the content
        output_patterns = [
            r'<strong>Output:</strong>\s*([^\n<]+)',
            r'Output:\s*([^\n<]+)',
            r'<strong>Output</strong>:\s*([^\n<]+)',
        ]

        for pattern in output_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                for match in matches[:num_cases]:
                    try:
                        # Clean up the match (remove HTML tags, extra whitespace)
                        clean_match = re.sub(r'<[^>]+>', '', match).strip()
                        expected = self._parse_value(clean_match)
                        expected_outputs.append(expected)
                    except:
                        continue

                if expected_outputs:
                    break

        return expected_outputs

    def _parse_generic_test_cases(self, lines: List[str]) -> List[Tuple[Any, Any]]:
        """
        Parse test cases when we can't determine the exact format.
        Assumes alternating input/output pattern.
        """
        test_cases = []

        # Try to pair lines as input/output
        for i in range(0, len(lines) - 1, 2):
            try:
                input_val = self._parse_value(lines[i])
                expected = self._parse_value(lines[i + 1])
                test_cases.append((input_val, expected))
            except:
                continue

        return test_cases

    def _parse_value(self, value_str: str) -> Any:
        """
        Parse a string value into appropriate Python type.

        Args:
            value_str (str): String representation of the value

        Returns:
            Any: Parsed Python value
        """
        value_str = value_str.strip()

        # Try to parse as JSON first
        try:
            return json.loads(value_str)
        except json.JSONDecodeError:
            pass

        # Handle special cases
        if value_str.lower() == 'null':
            return None
        elif value_str.lower() == 'true':
            return True
        elif value_str.lower() == 'false':
            return False

        # Try to parse as number
        try:
            if '.' in value_str:
                return float(value_str)
            else:
                return int(value_str)
        except ValueError:
            pass

        # Return as string if all else fails
        return value_str


def get_testcase(problem_id: Optional[int] = None,
                 title_slug: Optional[str] = None,
                 include_hidden: bool = False) -> List[Tuple[Any, Any]]:
    """
    Retrieve test cases from LeetCode for a given problem.

    Args:
        problem_id (int, optional): LeetCode problem ID (e.g., 1 for Two Sum)
        title_slug (str, optional): LeetCode problem title slug (e.g., "two-sum")
        include_hidden (bool): Whether to attempt to get hidden test cases (default: False)
                              Note: Hidden test cases are typically not available through public API

    Returns:
        List[Tuple[Any, Any]]: Test cases in Pyleet format [(input_args, expected_output), ...]

    Raises:
        ValueError: If neither problem_id nor title_slug is provided
        LeetCodeAPIError: If the API request fails or problem is not found

    Examples:
        # Get test cases by problem ID
        testcases = pyleet.get_testcase(problem_id=1)

        # Get test cases by title slug
        testcases = pyleet.get_testcase(title_slug="two-sum")

        # Use with pyleet.run()
        testcases = pyleet.get_testcase(problem_id=1)
        results = pyleet.run(testcases)
    """
    if not problem_id and not title_slug:
        raise ValueError("Either problem_id or title_slug must be provided")

    retriever = TestCaseRetriever()

    # Convert problem_id to title_slug if needed
    if problem_id and not title_slug:
        title_slug = retriever.get_problem_by_id(problem_id)
        if not title_slug:
            raise LeetCodeAPIError(f"Problem with ID {problem_id} not found")

    # Get question data
    question_data = retriever.get_question_data(title_slug)

    # Check if it's a paid-only problem
    if question_data.get('isPaidOnly', False):
        raise LeetCodeAPIError(
            f"Problem '{title_slug}' is only available to LeetCode Premium subscribers")

    # Parse and return test cases
    test_cases = retriever.parse_test_cases(question_data)

    if not test_cases:
        raise LeetCodeAPIError(
            f"No test cases found for problem '{title_slug}'")

    return test_cases
