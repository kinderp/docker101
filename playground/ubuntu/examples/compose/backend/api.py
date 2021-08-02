from flask import Flask, request
import mysql.connector

import json

from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST


class DBManager:
    def __init__(
            self,
            database=DB_NAME, host=DB_HOST, user=DB_USER,
            password=DB_PASSWORD
            ):
        self.connection = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database,
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()

    def check_user_id(self, node_id):
        q = f"SELECT COUNT(idNode) AS id_exist FROM node_tree WHERE idNode = {node_id}"
        self.cursor.execute(q)
        id_exist = dict(
                zip(self.cursor.column_names, self.cursor.fetchone())
        ).get('id_exist', 0)
        if not id_exist:
            return False, "Invalid node id"
        else:
            return True, None

    def get_data(self, node_id, language, search_keyword, page_num, page_size):
        if page_num:
            offset = (int(page_num)-1)*int(page_size)
            add_limit = f"LIMIT {page_size} OFFSET {offset}"
        else:
            offset = 0
            add_limit = ""

        q = f"""
        WITH traverse AS (

                SELECT Child.idNode, Child.iLeft, Child.iRight, Parent.idNode AS idNodeParent, Child.level AS level
                FROM node_tree AS Child
                JOIN node_tree AS Parent ON (
                    Child.level = Parent.level + 1
                    AND Child.iLeft > Parent.iLeft
                    AND Child.iRight < Parent.iRight
                    -- AND Parent.level >= 1
                )
            -- UNION ALL
            -- SELECT node_tree.idNode, node_tree.iLeft, node_tree.iRight, 0, 1 FROM node_tree WHERE idNode=5
        ),
        grouped_by_parent AS (SELECT traverse.idNodeParent,
        COUNT(traverse.idNode) as numChildrens FROM traverse GROUP BY traverse.idNodeParent),
        final AS (
        SELECT traverse.idNode, Names.NodeName, traverse.idNodeParent AS parent, traverse.level, IFNULL(grouped_by_parent.numChildrens,0) FROM traverse
        JOIN node_tree_names AS Names ON traverse.idNode = Names.idNode AND Names.language = '{language}' AND Names.nodeName LIKE '%{search_keyword}%'
        LEFT JOIN grouped_by_parent ON traverse.idNode = grouped_by_parent.idNodeParent
        ORDER BY level) SELECT * FROM final WHERE parent = {node_id}
        {add_limit}
        """
        self.cursor.execute(q)
        nodes = []
        for row in self.cursor:
            node_id, node_name, node_parent_id, node_level, node_num_childrens = row
            print(row)
            tmp = {
                'node_id': node_id,
                'name': node_name,
                'children_count': node_num_childrens,
            }
            nodes.append(tmp)
        return nodes


class InputParams:
    node_id = {
                "name": 'node_id',
                "required": True,
                "error": [
                            "Missing mandatory param `node_id`",
                            "Invalid value for param `node_id`"
                ],
                "validate": lambda x: True if x else False

    }
    language = {
                "name": 'language',
                "required": True,
                "error": [
                            "Missing mandatory param `language`",
                            "Invalid value for param `language`"
                ],
                "validate": lambda x: True if x else False
    }
    search_keyword = {
                "name": 'search_keyword',
                "required": False,
                "error": [
                            "Missing mandatory param `search_keyword`",
                            "Invalid value for param `search_keyword`"
                ],
                "validate": lambda x: True
    }
    page_num = {
                "name": 'page_num',
                "required": False,
                "error": [
                    "Missing mandatory param `page_num`",
                    "Invalid page number requested, `page_num` field should be > 0"
                ],
                "validate": lambda x: True if int(x) > 0 else False
    }
    page_size = {
                "name": 'page_size',
                "required": False,
                "error": [
                    "Missing mandatory param `page_size`",
                    "Invalid page size requested",
                ],
                "validate": lambda x: True if int(x) > 0 else False
    }


class Utils:
    @classmethod
    def build_response(cls, nodes=[], error="", status=200):
        return json.dumps({
                'nodes': nodes,
                'error': error,
        }), status

    @classmethod
    def _check(cls, value=None,  **kwargs):
        required = kwargs.get('required')
        if required and not value:
            return False, kwargs.get('error')[0]
        validate_function = kwargs.get("validate")
        return validate_function(value), kwargs.get('error')[1]

    @classmethod
    def validate(cls, **kwargs):
        for param_name, param_value in kwargs.items():
            input_param_utils = getattr(InputParams, param_name)
            response, error = cls._check(
                    **input_param_utils, value=param_value
            )
            if not response:
                return response, error
        return True, None


server = Flask(__name__)
conn = None


@server.route('/fetch')
def fetch():
    data_input = {
        'node_id': request.args.get('node_id', None),                # required
        'language': request.args.get('language', None),              # required
        'search_keyword': request.args.get('search_keyword', ''),    # optional
        'page_num': request.args.get('page_num', 1),                 # optional
        'page_size': request.args.get('page_size', 1000),            # optional
    }

    is_valid, error_msg = Utils.validate(**data_input)
    if not is_valid:
        return Utils.build_response(nodes=[], error=error_msg, status=400)

    global conn
    if not conn:
        conn = DBManager()

    id_is_valid, error_msg = conn.check_user_id(data_input.get('node_id'))
    if not id_is_valid:
        return Utils.build_response(nodes=[], error=error_msg, status=400)

    return Utils.build_response(nodes=conn.get_data(**data_input), status=200)


if __name__ == '__main__':
    server.run()
