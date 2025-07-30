from qualitics.Checks.base import BaseCheck
from qualitics.Query_builder.PSQL_queries import QueryBuilder
from typing import List, Dict, Optional
import re
import datetime
import spacy
nlp = spacy.load("en_core_web_sm")

class PiiChecker(BaseCheck):

    def _generate_regex_from_examples(self, examples: List[str]):
        """
        Dynamically creates regex from examples using common patterns.
        Handles emails, phones, IDs, etc. intelligently.
        """
        try:
            if not examples:
                raise ValueError("At least one example is required")

            first_example = examples[0]
            
            # Email detection
            if "@" in first_example and "." in first_example.split("@")[-1]:
                return re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b")
            
            # Phone number detection
            elif any(c.isdigit() for c in first_example.replace(" ", "")):
                digits = re.sub(r"[^\d]", "", first_example)
                if 10 <= len(digits) <= 15:
                    return re.compile(r"\b[\d\+\(\)\- ]{7,20}\b")
            
            # Generic ID pattern (e.g., A12345B)
            elif any(c.isalpha() for c in first_example) and any(c.isdigit() for c in first_example):
                return re.compile(r"\b([A-Za-z]\d+[A-Za-z]?|\d+[A-Za-z][A-Za-z\d]*)\b")
            
            # Fallback: Create regex with character classes
            else:
                pattern = []
                for char in first_example:
                    if char.isdigit():
                        pattern.append(r"\d")
                    elif char.isalpha():
                        pattern.append(r"[A-Za-z]")
                    else:
                        pattern.append(re.escape(char))
                return re.compile("".join(pattern))
        except Exception as e:
            print(e)
            raise e

    def run(self, check_id, alerting_enabled):
        """
        Hybrid detection:
        1. Check column name hints
        2. Use static patterns
        3. Fallback to dynamic regex from examples
        4. Use spacy for checking person/org/address types of PII data
        """
        try:
            PII_PATTERNS = {
            "email": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
            "phone": re.compile(r"\b(\+?\d{1,3}[\s-]?)?\(?\d{3,5}\)?[\s-]?\d{3,5}[\s-]?\d{3,5}\b"),
            "id": re.compile(r"\b([A-Za-z]\d+[A-Za-z]?|\d+[A-Za-z][A-Za-z\d]*)\b")
            }
            results = []
            database = self.config['database']
            table = self.config['table']
            schema = self.config['schema']
            for column in self.config['columns']:
                column_name_match = 0
                static_pattern_match = 0
                user_example_match = 0
                column_name = column.get('name')
                pii_type = column.get('type')
                sample_data = column.get('sample_data')

                # 1. Check column name hints (e.g., "email" in "user_email")
                if column_name:
                    for allowed_pii, regex in PII_PATTERNS.items():
                        if allowed_pii in column_name.lower():
                            print(f"Column {column_name} has been marked as potentially having PII data due to its naming.")
                            column_name_match = 1

                # 2. Check static patterns
                if pii_type:
                    query = QueryBuilder.pii_check_query(database, schema, table, column_name)
                    rows = self.connector.run_query(query)
                    for batch in self.connector.run_query_batch(query):
                        pii_found = []
                        for pattern_name, regex in PII_PATTERNS.items():
                            if pattern_name == pii_type:
                                for row in batch:
                                    value = row.get(column_name)
                                    if row and regex.search(value):
                                        pii_found.append(value)
                                        print(f"Column {column_name} has PII data matching regex pattern against the type defined in config!")
                                        break
                        static_pattern_match = 1 if pii_found else 0

                if column_name_match + static_pattern_match == 2:
                    print(f"2 out of 3 checks for PII data in column {column_name} has been positive, marking this column as having PII data!")
                    results.append({
                                "check_name": "pii_check",
                                "table": table,
                                "column": column_name,
                                "pii_type": pii_type,
                                "check_status": "fail",
                                "alert_status" : alerting_enabled,
                                "matches": pii_found[:5],
                                "checked_at": datetime.datetime.now().isoformat(),
                                "run_id": check_id
                            })
                    continue
                    
                # 3. Dynamic pattern from user examples (if no static match)
                if sample_data:
                    print(f"Moving to dynamic regex pattern retrieval for {column_name} because either 'type' is not mentioned in config or both column name and static check did not show PII data..")
                    dynamic_regex = self._generate_regex_from_examples(sample_data)
                    query = QueryBuilder.pii_check_query(database, schema, table, column_name)
                    for batch in self.connector.run_query_batch(query):
                        pii_found = []
                        for row in batch:
                            value = row.get(column_name)
                            if row and dynamic_regex.search(value):
                                pii_found.append(value)
                                print(f"Column {column_name} has PII data matching dynamic regex pattern for the examples defined in config!")
                                break
                        user_example_match = 1 if pii_found else 0

                if column_name_match + static_pattern_match + user_example_match >= 2:
                    print(f"2 out of 3 checks for PII data in column {column_name} has been positive, marking this column as having PII data!")
                    results.append({
                                "check_name": "pii_check",
                                "table": table,
                                "column": column_name,
                                "pii_type": pii_type,
                                "check_status": "fail",
                                "alert_status" : alerting_enabled,
                                "matches": pii_found[:5],
                                "checked_at": datetime.datetime.now().isoformat(),
                                "run_id": check_id
                            })
                
                # 4. NLP-based entity detection as a last fallback
                if (sample_data is None and pii_type is None) or (column_name_match + static_pattern_match + user_example_match < 2):
                    if (sample_data is None and pii_type is None):
                        print(f"No sample data or type defined in config for col: {column_name}!")
                    else:
                        print(f"Column name hints/ Static & dynamic regex match did not detect any email/phone/id PII data in {column_name}!")
                    print(f"Running NLP-based PII detection for column {column_name} to check for named entities like Address, Nationality etc.")
                    query = QueryBuilder.pii_check_query(database, schema, table, column_name)
                    for batch in self.connector.run_query_batch(query):
                        pii_found = []
                        pii_types = set()
                        for row in batch:
                            value = row.get(column_name)
                            if value:
                                doc = nlp(str(value))
                                for ent in doc.ents:
                                    if ent.label_ in ["PERSON","NORP","ORG","GPE"]:
                                        pii_found.append(value)
                                        if ent.label_== "PERSON":
                                            pii_type = "Full name"
                                            pii_types.add(pii_type)
                                            print(f"NLP detected full names present in col: {column_name}")
                                        elif ent.label_== "NORP":
                                            pii_type = "Nationality/Religion/Political belief"
                                            pii_types.add(pii_type)
                                            print(f"NLP detected Nationality/Religion/Political belief present in col: {column_name}")
                                        elif ent.label_== "ORG":
                                            pii_type = "Company/Agency/Institution"
                                            pii_types.add(pii_type)
                                            print(f"NLP detected Company/Agency/Institution name present in col: {column_name}")
                                        elif ent.label_== "GPE":
                                            pii_type = "Address"
                                            pii_types.add(pii_type)
                                            print(f"NLP detected Addresses present in col: {column_name}")
                                        break  # Found one, no need to keep scanning this row
                        nlp_pii_match = 1 if pii_found else 0

                    if len(pii_types) == 1:
                        final_pii_type = pii_types.pop() 
                    elif len(pii_types) > 1:
                        final_pii_type = list(pii_types) 
                    else:
                        final_pii_type = None

                    if nlp_pii_match == 1:
                        print(f"NLP check detected PII data in col: {column_name}")
                        results.append({
                                    "check_name": "pii_check",
                                    "table": table,
                                    "column": column_name,
                                    "pii_type": final_pii_type,
                                    "check_status": "fail",
                                    "alert_status" : alerting_enabled,
                                    "matches": pii_found[:5],
                                    "checked_at": datetime.datetime.now().isoformat(),
                                    "run_id": check_id
                                })
                    else:
                        results.append({
                                    "check_name": "pii_check",
                                    "table": table,
                                    "column": column_name,
                                    "check_status": "pass",
                                    "alert_status" : alerting_enabled,
                                    "checked_at": datetime.datetime.now().isoformat(),
                                    "run_id": check_id
                                })
                
            return results
        except Exception as e:
            print(e)
            raise e