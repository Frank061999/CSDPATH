import json
import pymysql, jwt, bcrypt, datetime, pymysql.cursors
from http.cookies import SimpleCookie
from pymysql.err import IntegrityError
db_config = {
    'host': 'database-1.cvwoaic8ob2d.us-west-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'dbpassword',
    'database': 'csdpath',
    'cursorclass': pymysql.cursors.DictCursor
}
cors_headers = {
    'Access-Control-Allow-Origin': 'https://csdpath.s3.us-west-1.amazonaws.com',
    'Access-Control-Allow-Headers': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT',
    'Access-Control-Allow-Methods': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    'Access-Control-Allow-Credentials': 'true'
}
INVALID_REQUEST_RESPONSE = {
    'statusCode': 400,
    'headers': cors_headers,
    'body': f"Error: invalid request payload: "
}
cursor = None
connection = None

def lambda_handler(event, context):

    global cursor, connection
    # TODO Authenticate
    try:
        cookie_string = event['headers']['cookie']
    except KeyError:
        return {
            'statusCode' : 401,
            'headers' : cors_headers,
            'body' :"Error: Token not found"
        }
    try:
        body = json.loads(event['body'])
        action = body['action']
    except KeyError:
        return INVALID_REQUEST_RESPONSE
    cookie = SimpleCookie()
    cookie.load(cookie_string)
    token = cookie['login_token'].value
    try:
        token_payload = jwt.decode(token,'supersecretkey',algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {
            'statusCode' : 401,
            'headers' : cors_headers,
            'body' :"Error: Token has expired"
        }
    except jwt.InvalidTokenError:
        return {
            'statusCode' : 401,
            'headers' : cors_headers,
            'body' : "Error: Invalid token"
        }
    role = token_payload['role']
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
    
    except pymysql.Error as e:
        print(f"Initialization error: {e}")
      
    
    if action == 'AddCourse':
        return AddCourse(body)
    elif action == 'AddPreReqRelation':
        return AddPreReqRelation(body)
    elif action == 'ModifyCourse':
        return ModifyCourse(body)
    elif action == 'PutCourseInNewQuarter':
        return PutCourseInNewQuarter(body)
    elif action == 'RemovePreReqRelation':
        return RemovePreReqRelation(body)
    elif action == 'RemoveCourseFromQuarter':
        return RemoveCourseFromQuarter(body)
    elif action == 'AddUser':
        if token_payload['role'] in ('admin'):
            return AddUser(body)
        else:
            return {
                'statusCode' : 403,
                'headers' : cors_headers,
                'body' : "Error: Only admin can add users"
            }
    elif action == 'RemoveUser':
        if token_payload['role'] in ('admin'):
            return RemoveUser(body)
        else:
            return {
                'statusCode' : 403,
                'headers' : cors_headers,
                'body' : "Error: Only admin can remove users"
            }
    else:
        return {
                'statusCode' : 400,
                'headers' : cors_headers,
                'body' : "Error: Invalid Action"
        }
    connection.close()
    
    
def AddCourse(event):
    setting_program_and_quarter = True
    
    try:
        # INPUT:
        course_name = event['course_name']
        course_credits = event['course_credits']
        course_code = event['course_code']
        program_name = event['program_name']
        quarter_no = event['quarter_no']
        if program_name == "" or quarter_no == "":
            setting_program_and_quarter = False
            if not (program_name == "" and quarter_no == ""): # either both should be empty or both should be full.
                return INVALID_REQUEST_RESPONSE
    except KeyError as ke:
        return INVALID_REQUEST_RESPONSE
    if not course_name or not course_credits or not course_code:
        return INVALID_REQUEST_RESPONSE
    try:
        create_class = "INSERT INTO classes (class_code,class_name,credits) VALUES (%s,%s,%s)"
        cursor.execute(create_class, (course_code,course_name,course_credits))
        cursor.execute("SELECT * FROM classes WHERE class_code = %s",course_code);
        result = cursor.fetchone()
        if setting_program_and_quarter:
            set_program_quarter = f"""
            INSERT INTO programs_classes_quarters (program_id,quarter_no,course_id)
                VALUES (
                    (SELECT program_id FROM programs WHERE program_name = %s),
                    %s,
                    {result['class_id']}
                )
            """
            cursor.execute(set_program_quarter,(program_name,quarter_no))
            select_q = """
                        SELECT class_id, class_code, class_name, quarter_no, program_name
                        FROM classes
                        JOIN programs_classes_quarters pcq on pcq.course_id = classes.class_id
                        JOIN programs using (program_id)
                        WHERE class_code = %s
            """
            cursor.execute(select_q,course_code)
            result.update(cursor.fetchone())
        connection.commit()
        return {
            'statusCode' : 200,
            'headers' : cors_headers,
            'body': json.dumps({'message':'Insertion Successful','inserted row':result})
        } 
            
    except IntegrityError as e:
        if(e.args[0]==1062):
            return {
                'statusCode' : 409,
                'headers' : cors_headers,
                'body': 'Duplicate Row'
            }
        if(e.args[0]==1048):
            return {
                'statusCode' : 400,
                'headers' : cors_headers,
                'body': 'Invalid Program name'
            }
        else:
            return {
                'statusCode' : 500,
                'headers' : cors_headers,
                'body': str(e)
            }

def AddPreReqRelation(event):
    # body = json.loads(event['body'])
    # course_code = body.get('course_code')
    # course_name = body.get('course_name')
    # course_credits = body.get('course_credits')
    try:
        # INPUT:
        course_id = event['course_id']
        pre_req_course_id = event['pre_req_course_id']
    except KeyError as ke:
        return INVALID_REQUEST_RESPONSE
    if not course_id or not pre_req_course_id:
        return INVALID_REQUEST_RESPONSE
    try:
        # Check for circular dependency
        cursor.execute("""
                WITH RECURSIVE PrerequisitePath AS (
                    SELECT class_id, prerequisite_by_class_id
                    FROM prerequisites
                    WHERE class_id = %s
                    
                    UNION ALL
                    
                    SELECT p.class_id, p.prerequisite_by_class_id
                    FROM prerequisites p
                    JOIN PrerequisitePath pp ON p.class_id = pp.prerequisite_by_class_id
                )
                SELECT *
                FROM PrerequisitePath
                WHERE prerequisite_by_class_id = %s;
            """, (pre_req_course_id, course_id))

        result = cursor.fetchone()
        
        if result:
            # Circular dependency detected
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': 'Circular dependency detected'
            }
        insertion = "INSERT INTO prerequisites (class_id, prerequisite_by_class_id) VALUES (%s,%s)"
        cursor.execute(insertion,(course_id, pre_req_course_id))
        connection.commit()
        select = """
                SELECT
                    (SELECT class_name FROM classes WHERE class_id = p.class_id) AS class,
                    (SELECT class_name FROM classes WHERE class_id = p.prerequisite_by_class_id) AS prerequisite
                FROM
                    prerequisites p
                WHERE
                    class_id = %s AND prerequisite_by_class_id = %s		
        """
        cursor.execute(select,(course_id, pre_req_course_id))
        result = cursor.fetchone()
        return {
            'statusCode' : 200,
            'headers' : cors_headers,
            'body': f'Insertion Successful, Inserted row: {result}'
        } 
            
    except IntegrityError as e:
        if(e.args[0]==1452):
            return {
                'statusCode' : 400,
                'headers' : cors_headers,
                'body': 'Invalid id'
            }
        else:
            return {
                'statusCode' : 500,
                'headers' : cors_headers,
                'body': str(e)
            }
    
def ModifyCourse(event):
    # body = json.loads(event['body'])
    # course_code = body.get('course_code')
    # course_name = body.get('course_name')
    # course_credits = body.get('course_credits')
    try:
        # INPUT:
        course_id = event['course_id']
        course_code = event['course_code']
        course_name = event['course_name']
        credits = event['credits']
    except KeyError as ke:
        return INVALID_REQUEST_RESPONSE
    if not course_id or not course_code or not course_name or not credits:
        return INVALID_REQUEST_RESPONSE
    try:
        update_query = 'UPDATE classes SET class_code = %s, class_name = %s, credits = %s WHERE class_id = %s'
        cursor.execute(update_query, (course_code,course_name,credits,course_id))
        if cursor.rowcount == 0:
            return {
                'statusCode' : 404,
                'headers' : cors_headers,
                'body': "ERROR: Course with the provided ID was not found"
            }
        connection.commit()
        cursor.execute("SELECT * from classes where class_id = %s",course_id)
        result = cursor.fetchone()
        return {
            'statusCode' : 200,
            'headers' : cors_headers,
            'body': f'Update Successful, Updated row: {result}'
        } 
            
    except IntegrityError as e:
        return {
            'statusCode' : 500,
            'headers' : cors_headers,
            'body': str(e)
        }
        
def PutCourseInNewQuarter(event):
    # body = json.loads(event['body'])
    # course_id = body.get('course_id')
    # program_name = body.get('program_name')
    # quarter_no = body.get('quarter_no')
    try:
        # INPUT:
        course_id = event['course_id']
        program_name = event['program_name']
        quarter_no = event['quarter_no']
    except KeyError as ke:
        return INVALID_REQUEST_RESPONSE
    if not course_id or not program_name or not quarter_no:
        return INVALID_REQUEST_RESPONSE
    try:
        
        cursor.execute("SELECT * FROM classes WHERE class_id = %s",course_id);
        course_row = cursor.fetchone()
        if not course_row:
            return {
                'statusCode' : 404,
                'headers' : cors_headers,
                'body' :"Error: Course not found"
            }
        
        set_program_quarter = f"""
        INSERT INTO programs_classes_quarters (program_id,quarter_no,course_id)
            VALUES (
                (SELECT program_id FROM programs WHERE program_name = %s),
                %s,
                {course_id}
            )
        """
        cursor.execute(set_program_quarter,(program_name,quarter_no))
        select_q = """
                    SELECT class_id, class_code, class_name, quarter_no, program_name
                    FROM classes
                    JOIN programs_classes_quarters pcq on pcq.course_id = classes.class_id
                    JOIN programs using (program_id)
                    WHERE class_id = %s
        """
        cursor.execute(select_q,course_id)
        result = cursor.fetchone()
        connection.commit()
        return {
            'statusCode' : 200,
            'headers' : cors_headers,
            'body': f'Program_Quarter association successful, Inserted row: {result}'
        } 
            
    except IntegrityError as e:
        if(e.args[0]==1062):
            return {
                'statusCode' : 409,
                'headers' : cors_headers,
                'body': 'Duplicate Row'
            }
        else:
            return {
                'statusCode' : 500,
                'headers' : cors_headers,
                'body': str(e)
            }
            
def RemovePreReqRelation(event):
        # body = json.loads(event['body'])
    # course_code = body.get('course_code')
    # course_name = body.get('course_name')
    # course_credits = body.get('course_credits')
    try:
        # INPUT:
        course_id = event['course_id']
        pre_req_course_id = event['pre_req_course_id']
    except KeyError as ke:
        return INVALID_REQUEST_RESPONSE
    if not course_id or not pre_req_course_id:
        return INVALID_REQUEST_RESPONSE
    try:
        cursor.execute("DELETE FROM prerequisites WHERE class_id = %s and prerequisite_by_class_id = %s",(course_id, pre_req_course_id))
        if cursor.rowcount == 1:
            connection.commit()
            return {
                'statusCode' : 200,
                'headers' : cors_headers,
                'body': 'Deletion successful'
            }
        else:
            return {
                'statusCode' : 409,
                'headers' : cors_headers,
                'body': 'Deletion failed, no matching pre requisite relation found'
            }
    except IntegrityError as e:
        return {
            'statusCode' : 500,
            'headers' : cors_headers,
            'body': str(e)
        }

def RemoveCourseFromQuarter(event):
    # body = json.loads(event['body'])
    # course_id = body.get('course_id')
    # program_name = body.get('program_name')
    # quarter_no = body.get('quarter_no')
    try:
        # INPUT:
        course_id = event['course_id']
        program_name = event['program_name']
        quarter_no = event['quarter_no']
    except KeyError as ke:
        return INVALID_REQUEST_RESPONSE
    if not course_id or not program_name or not quarter_no:
        return INVALID_REQUEST_RESPONSE
    try:
        # Find all courses that have this as a prerequisite
        cursor.execute("SELECT program_id FROM programs WHERE program_name = %s", program_name)
        program_id = cursor.fetchone()['program_id']
        if not program_id:
            return {
                'statusCode' : 404,
                'headers' : cors_headers,
                'body' :"Error: Program not found"
            }
        cursor.execute(f"""
                SELECT
                    (SELECT class_name FROM classes WHERE class_id = p.class_id) AS class,
                    quarter_no,
                    %s as program_name
                FROM
                    prerequisites p
                JOIN
                    programs_classes_quarters pcq
                ON pcq.course_id = p.class_id
                WHERE
                    p.prerequisite_by_class_id = %s
                        AND
                    pcq.program_id = %s
        
        """
        ,(program_name,course_id,program_id));
        course_rows = cursor.fetchall()
        if not course_rows:
            cursor.execute("DELETE FROM programs_classes_quarters WHERE program_id = %s AND quarter_no = %s AND course_id = %s", (program_id,quarter_no,course_id))
            if cursor.rowcount == 1:
                connection.commit()
                return {
                'statusCode' : 200,
                'headers' : cors_headers,
                'body' :f"Deletion successful: Deleted from quarter: {quarter_no}, and program: {program_name}, course_id:{course_id}"
            }
            else:
                return {
                    'statusCode' : 409,
                    'headers' : cors_headers,
                    'body': 'Association not deleted: Record not found'
                }
        else:
            return {
                'statusCode':409,
                'headers': cors_headers,
                'body' : json.dumps({'message':'Dependency detected','Dependents':json.dumps(course_rows)})
                }
        
            
    except IntegrityError as e:
            return {
                'statusCode' : 500,
                'headers' : cors_headers,
                'body': str(e)
            }
            
input = {'action':'RemoveCourseFromQuarter','course_id' : 29,'program_name' : 'BAS','quarter_no':9}	
def AddUser(event):
    try:
        username = event['username']
        password = event['password']
    except KeyError:
        return INVALID_REQUEST_RESPONSE
    salt = bcrypt.gensalt(rounds=8)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    try:
        cursor.execute(f"""
        INSERT INTO
        users (username, password_hash, salt, role_id)
        VALUES (%s,%s,%s,(SELECT role_id FROM roles WHERE role_description = 'user'))
        """, (username, hashed.decode('utf-8'), salt.decode('utf-8')))
    except IntegrityError as e:
        if(e.args[0]==1062):
           return {
               'statusCode' : 409,
               'headers' : cors_headers,
               'body': 'Duplicate username'
           }
        else:
            return {
               'statusCode' : 500,
               'headers' : cors_headers,
               'body': f'ERROR: {str(e)}'
           }
    connection.commit()
    return {
                'statusCode' : 200,
                'headers' : cors_headers,
                'body' :f"User added sucessfully: '{username}'"
            }
       
    
def RemoveUser(event):
    try:
        username = event['username']
    except KeyError:
        return INVALID_REQUEST_RESPONSE
    if username == 'admin':
        return {
            'statusCode': 403,
            'headers': cors_headers,
            'body': 'Can\'t remove admin'
        }
    try:
        cursor.execute("""
        DELETE FROM users WHERE username = %s
        """, (username,))
        if cursor.rowcount == 0:
            return {
                'statusCode': 404,
                'headers': cors_headers,
                'body': 'User not found'
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': f'ERROR: {str(e)}'
        }

    connection.commit()
    return {
        'statusCode': 200,
        'headers': cors_headers,
        'body': f"User removed successfully: '{username}'"
    }
