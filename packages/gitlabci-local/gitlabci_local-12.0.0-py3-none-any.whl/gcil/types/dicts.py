#!/usr/bin/env python3

# Standard libraries
from re import findall, match
from typing import Dict, Iterable, List, Optional, Union

# Dicts class, pylint: disable=too-few-public-methods
class Dicts:

    # Data type
    Data = Union[Dict[str, str], Iterable['Data']]

    # Finds type
    Finds = Optional[Union[Dict[str, str], List[str], str]]

    # Finder
    @staticmethod
    def find(data: Dict[str, str], path: str) -> Optional[Finds]:

        # Variables
        queries: List[str] = path.split('.')
        result: Dicts.Finds = data if queries else None

        # Iterate through queries
        for query in queries:

            # Parse query to key and index
            matches = match(r'([^\[]*)(\[.*\])+', query)
            if matches:
                key = matches.groups()[0]
                indexes = [
                    int(value) for value in findall(r'\[(-?\d+)\]*',
                                                    matches.groups()[1])
                ]
            else:
                key = query
                indexes = []

            # Extract key
            if key and result and isinstance(result, dict):
                result = result.get(key, None)

            # Extract index
            for index in indexes:
                if isinstance(result,
                              list) and result and -len(result) <= index < len(result):
                    result = result[index]
                else:
                    result = None

            # Empty node
            if not result:
                break

        # Result
        return result
