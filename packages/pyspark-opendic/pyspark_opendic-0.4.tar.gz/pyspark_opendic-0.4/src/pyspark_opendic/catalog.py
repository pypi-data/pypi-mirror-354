import json
import re
import textwrap
from typing import Any
import ast
from pyspark.sql.types import IntegerType, StringType, FloatType, DoubleType
import pandas as pd
import requests
from pydantic import ValidationError
from pyspark.sql import SparkSession
from pyspark.sql.catalog import Catalog

from pyspark_opendic.client import OpenDicClient
from pyspark_opendic.model.openapi_models import (
    CreatePlatformMappingRequest,
    CreateUdoRequest,
    DefineUdoRequest,
    PlatformMapping,
    Statement,
    Udo,
)
from pyspark_opendic.patterns.opendic_patterns import OpenDicPatterns
from pyspark_opendic.prettyResponse import PrettyResponse


class OpenDicCatalog(Catalog):
    def __init__(self, sparkSession: SparkSession, api_url: str):
        self.sparkSession = sparkSession

        self.credentials = sparkSession.conf.get("spark.sql.catalog.polaris.credential")
        if self.credentials is None:
            raise ValueError("spark.sql.catalog.polaris.credential is not set")
        self.api_url = api_url
        self.client = OpenDicClient(api_url, self.credentials)
        self.opendic_patterns = OpenDicPatterns.compiled_patterns()

    def sql(self, sql_text: str):
        sql_cleaned = sql_text.strip()
        
        for command_type, pattern in self.opendic_patterns:
            match = pattern.match(sql_cleaned)
            if match:
                return self._handle_opendic_command(command_type, match, sql_text)

        # Fallback to native Spark SQL if no OpenDic match
        return self.sparkSession.sql(sql_text)

    def _handle_opendic_command(self, command_type: str, match: re.Match, sql_text: str):
        try:
            # Syntax: CREATE [OR REPLACE] [TEMPORARY] OPEN <object_type> <name> [IF NOT EXISTS] [AS <alias>] [PROPS { <properties> }]
            if command_type == "create":
                object_type = match.group("object_type")
                name = match.group("name")
                alias = match.group("alias")
                properties = match.group("properties")

                # Parse props as JSON - this serves as a basic syntax check on the JSON input and default to None so we can catch Pydantic Error
                create_props: dict[str, str] = json.loads(properties) if properties else None

                # Build Udo and CreateUdoRequest Pydantic models
                udo_object = Udo(type=object_type, name=name, alias=alias, props=create_props)
                create_request = CreateUdoRequest(udo=udo_object)

                # Serialize to JSON
                payload = create_request.model_dump()

                # Send Request
                response = self.client.post(f"/objects/{object_type}", payload)

                return self.pretty_print_result({"success": "Object created successfully", "response": response})
           
            elif command_type == "create_batch":
                object_type = match.group("object_type")
                properties_list = json.loads(match.group("properties"))  # Already a list of dicts

                udo_objects: list[dict[str, Any]] = []
                for item in properties_list:
                    name = item.pop("name")
                    udo_object = Udo(type=object_type, name=name, props=item).model_dump()
                    udo_objects.append(udo_object)

                response = self.client.post(f"/objects/{object_type}/batch", udo_objects)
                return self.pretty_print_result({"success": "Batch created", "response": response})

            # Syntax: ALTER OPEN <object_type> <name> [PROPS { <properties> }]
            elif command_type == "alter":
                object_type = match.group("object_type")
                name = match.group("name")
                properties = match.group("properties")

                alter_props: dict[str, str] = json.loads(properties) if properties else None

                # Build Udo and CreateUdoRequest Pydantic models            
                udo_object = Udo(type=object_type, name=name, props=alter_props)
                alter_request = CreateUdoRequest(udo=udo_object)

                # Serialize to JSON
                payload = alter_request.model_dump()

                # Send Request
                response = self.client.put(f"/objects/{object_type}/{name}", payload)

                return self.pretty_print_result({"success": "Object altered successfully", "response": response})

            # Syntax: SHOW OPEN TYPES
            elif command_type == "show_types":
                response = self.client.get("/objects")
                return self.pretty_print_result({"success": "Object types retrieved successfully", "response": response})

            # Syntax: SHOW OPEN PLATFORMS
            elif command_type == "show_platforms_all":
                response = self.client.get("/platforms")
                return self.pretty_print_result({"success": "Platforms retrieved successfully", "response": response})

            # Syntax: SHOW OPEN MAPPINGS FOR <platform>
            elif command_type == "show_mappings_for_platform":
                platform = match.group("platform")
                response = self.client.get(f"/platforms/{platform}")
                return self.pretty_print_result({"success": "Mappings for platform retrieved successfully", "response": response})

            # Syntax: DROP OPEN MAPPING[S] FOR <platform>
            elif command_type == "drop_mapping_for_platform":
                platform = match.group("platform")
                response = self.client.delete(f"/platforms/{platform}")
                return self.pretty_print_result({"success": "Platform's mappings dropped successfully", "response": response})

            # Syntax: SHOW OPEN <object_type>[s]
            elif command_type == "show":
                object_type = match.group("object_type")
                response = self.client.get(f"/objects/{object_type}")
                return self.pretty_print_result({"success": "Objects retrieved successfully", "response": response})

            # Syntax: SHOW OPEN MAPPING <object_type> PLATFORM <platform>
            elif command_type == "show_mapping_for_object_and_platform":
                object_type = match.group("object_type")
                platform = match.group("platform")
                response = self.client.get(f"/objects/{object_type}/platforms/{platform}")
                return self.pretty_print_result({"success": "Mapping retrieved successfully", "response": response})

            # Syntax: SHOW OPEN PLATFORMS FOR <object_type>
            elif command_type == "show_platforms_for_object":
                object_type = match.group("object_type")
                response = self.client.get(f"/objects/{object_type}/platforms")
                return self.pretty_print_result({"success": "Platforms retrieved successfully", "response": response})

            # Syntax: SYNC OPEN <object_type> FOR <platform>
            elif command_type == "sync":
                object_type = match.group("object_type")
                platform: str = match.group("platform").lower()
                response = self.client.get(f"/objects/{object_type}/platforms/{platform}/pull")
                statements = [Statement.model_validate(item) for item in response]
                return self.dump_handler(statements)
            
            # Syntax: SYNC OPEN OBJECTS FOR <platform>
            elif command_type == "sync_all":
                platform: str = match.group("platform").lower()
                response = self.client.get(f"/platforms/{platform}/pull")
                statements = [Statement.model_validate(item) for item in response]
                return self.dump_handler(statements)

            # Syntax: DEFINE OPEN <udoType> PROPS { <properties> }
            elif command_type == "define":
                udoType = match.group("udoType")
                properties = match.group("properties")
                define_props: dict[str, str] = json.loads(properties) if properties else None
                define_request = DefineUdoRequest(udoType=udoType, properties=define_props)
                self.validate_data_type(define_props)
                payload = define_request.model_dump()
                response = self.client.post("/objects", payload)
                return self.pretty_print_result({"success": "Object defined successfully", "response": response})

            # Syntax: DROP OPEN <object_type>
            elif command_type == "drop":
                object_type = match.group("object_type")
                response = self.client.delete(f"/objects/{object_type}")
                return self.pretty_print_result({"success": "Object dropped successfully", "response": response})

            # Syntax: ADD OPEN MAPPING <object_type> PLATFORM <platform> SYNTAX { ... } PROPS { ... }
            elif command_type == "add_mapping":
                object_type = match.group("object_type")
                platform = match.group("platform")
                syntax = match.group("syntax").strip()
                properties = match.group("props")

                # Remove outer quotes if present - this is a workaround for the fact that the regex captures the outer quotes (or everything inside curly braces)
                if syntax.startswith('"') and syntax.endswith('"'):
                    syntax = syntax[1:-1]
                # Props is expected to be a JSON-encoded dict of dicts (e.g., "args": {"propType": "map", ...})
                object_dump_map: dict[str, dict[str, Any]] = json.loads(properties)

                mapping_request = CreatePlatformMappingRequest(
                    platformMapping=PlatformMapping(
                        typeName=object_type,
                        platformName=platform,
                        syntax=syntax.strip(),
                        objectDumpMap=object_dump_map,
                    )
                )
                response = self.client.post(f"/objects/{object_type}/platforms/{platform}", mapping_request.model_dump())
                return self.pretty_print_result({"success": "Mapping added successfully", "response": response})

        except json.JSONDecodeError as e:
            return self.pretty_print_result({
                "error": "Invalid JSON syntax in properties",
                "details": {"sql": "", "exception_message": str(e)}
            })
        except requests.exceptions.HTTPError as e:
            # Check if httpcode is 401
            if e.response.status_code == 401:
                self.client.refresh_oauth_token(self.credentials)
                self.sql(sql_text)
            else:
                return self.pretty_print_result({
                    "error": "HTTP Error",
                    "details": str(e),
                    "Catalog Response": e.response.json() if e.response else None}
                )
        except ValidationError as e:
            return self.pretty_print_result({
                "error": "Validation error",
                "exception message": str(e)
            })
        except ValueError as e:
            return self.pretty_print_result({
                "error": "Invalid type for DEFINE statement",
                "exception message": str(e)
            })


    # Helper method to extract SQL statements from Polaris response and execute
    def dump_handler(self, response: list[Statement]):
        """
        Extracts SQL statements from the Polaris response and executes them using Spark.

        Args:
            response (list): List of Statement objects.

        Returns:
            dict: Execution result with status.
        """
        if not response:
            return self.pretty_print_result({"error": "No statements found in response"})

        execution_results = []

        for statement in response:
            sql_text = statement.definition

            # Normalizes indentation (keep relative indents! - should work with the initial indentation of the SQL statement we discussed)
            formatted_sql = textwrap.dedent(sql_text).strip()

            if self.is_create_function(formatted_sql):
                try:
                    self.register_sql_function(formatted_sql)
                    execution_results.append({"sql": formatted_sql, "status": "function registered"})
                    continue
                except Exception as e:
                    execution_results.append({"sql": formatted_sql, "status": "failed", "error": str(e)})
                    continue

            try:
                # Execute the SQL statement using Spark
                self.sparkSession.sql(formatted_sql)
                execution_results.append({"sql": formatted_sql, "status": "executed"})
            except Exception as e:
                execution_results.append({"sql": formatted_sql, "status": "failed", "error": str(e)})

        return self.pretty_print_result({"executions": execution_results})

    def validate_data_type(self, props: dict[str, str]) -> dict[str, str]:
        """
        Validate the data type against a predefined set of valid types.

        Args:
            proerties (dict): The properties dictionary to validate.

        Returns:
            dict: A dictionary with the validation result.
        """
        # The same set of valid data types as in the OpenDic API - UserDefinedEntitySchema (+ int and double)
        valid_data_types = {
            "string",
            "number",
            "boolean",
            "float",
            "date",
            "array",
            "list",
            "map",
            "object",
            "variant",
            "int",
            "double",
        }

        for key, value in props.items():
            if value.lower() not in valid_data_types:
                raise ValueError(f"Invalid data type '{value}' for key '{key}'")

        return {"success": "Data types validated successfully"}

    def pretty_print_result(self, result: dict):
        """
        Pretty print the result in a readable format.
        """
        pd.set_option("display.width", None)  # Auto-detect terminal width
        pd.set_option("display.max_colwidth", None)  # Show full content of each cell
        pd.set_option("display.max_rows", None)  # Show all rows
        pd.set_option("display.expand_frame_repr", False)  # Don't wrap to multiple lines

        response = result.get("response")

        # Polaris-spec-compliant "good" responses, so objects or lists of objects
        if isinstance(response, list) and all(isinstance(item, dict) for item in response):
            return pd.DataFrame(response)

        elif isinstance(response, dict):
            return pd.DataFrame([response])

        # Everything else — errors, messages, etc.
        return PrettyResponse(result)
    
    def is_create_function(self, sql_text: str) -> bool:
        return bool(re.match(
            r"^CREATE\s+FUNCTION\s+\w+\(.*?\)\s+RETURNS\s+\w+\s+LANGUAGE\s+SQL\s+AS\s+'RETURN\s+.+?';?$",
            sql_text, re.IGNORECASE
        ))

    def register_sql_function(self, sql_text: str):
        pattern = r"""
            CREATE\s+FUNCTION\s+(\w+)\s*\((\w+)\s+(\w+)\)\s+
            RETURNS\s+(\w+)\s+
            LANGUAGE\s+SQL\s+
            AS\s+'RETURN\s+(.+?)';
        """
        match = re.match(pattern, sql_text, re.IGNORECASE | re.VERBOSE)
        if not match:
            raise ValueError("Invalid CREATE FUNCTION syntax.")

        func_name, arg_name, arg_type, return_type, expression = match.groups()

        # Build Python function
        fn_code = f"def {func_name}({arg_name}): return {expression.strip()}"
        local_ns = {}
        exec(fn_code, {}, local_ns)

        type_map = {
            "INT": IntegerType(),
            "STRING": StringType(),
            "FLOAT": FloatType(),
            "DOUBLE": DoubleType()
        }

        return_type_obj = type_map.get(return_type.upper())
        if not return_type_obj:
            raise ValueError(f"Unsupported return type: {return_type}")

        self.sparkSession.udf.register(func_name, local_ns[func_name], return_type_obj)
