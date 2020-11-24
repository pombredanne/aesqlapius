-- def nothing() -> None: ...
SELECT;

-- def single_dict() -> Single[Dict]: ...
SELECT 0 AS a, 'a' AS b;

-- def single_list() -> Single[List]: ...
SELECT 0 AS a, 'a' AS b;

-- def single_tuple() -> Single[Tuple]: ...
SELECT 0 AS a, 'a' AS b;

-- def iterator_dict() -> Iterator[Dict]: ...
SELECT a, chr(ascii('a') + a) AS b FROM generate_series(0, 2) a;

-- def iterator_list() -> Iterator[List]: ...
SELECT a, chr(ascii('a') + a) AS b FROM generate_series(0, 2) a;

-- def iterator_tuple() -> Iterator[Tuple]: ...
SELECT a, chr(ascii('a') + a) AS b FROM generate_series(0, 2) a;

-- def list_dict() -> List[Dict]: ...
SELECT a, chr(ascii('a') + a) AS b FROM generate_series(0, 2) a;

-- def list_list() -> List[List]: ...
SELECT a, chr(ascii('a') + a) AS b FROM generate_series(0, 2) a;

-- def list_tuple() -> List[Tuple]: ...
SELECT a, chr(ascii('a') + a) AS b FROM generate_series(0, 2) a;
