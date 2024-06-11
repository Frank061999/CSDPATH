import json
import pymysql

# Define your database connection details
db_config = {
    'host': 'database-1.cvwoaic8ob2d.us-west-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'dbpassword',
    'database': 'csdpath',
}
cors_headers = {
        'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
        'Access-Control-Allow-Headers': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT',
        'Access-Control-Allow-Methods': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
    }


def lambda_handler(event, context):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT class_id, class_code, class_name, quarter_no, program_name
            FROM classes
            JOIN programs_classes_quarters pcq on pcq.course_id = classes.class_id
            JOIN programs using (program_id)
            """)
        rows = cursor.fetchall()
        results = {}  # Initialize dictionary to store results

        for row in rows:
            class_id, class_code, class_name, quarter_no, program_name = row
            if class_code in results:
                results[class_code]['program_quarter'][program_name] = quarter_no
                continue
            course = {
                'class_id': class_id,
                'className': class_name,
                'program_quarter': {program_name:quarter_no},
                'preqs': [],
                'unblock': []
            }

            cursor.execute("""
                SELECT classes.class_code 
                FROM classes 
                JOIN prerequisites 
                ON classes.class_id = prerequisites.prerequisite_by_class_id 
                WHERE prerequisites.class_id = %s
            """, class_id)
            
            course['preqs'] = [prereq[0] for prereq in cursor.fetchall()]  
            
            cursor.execute("""
                SELECT classes.class_code 
                FROM classes 
                JOIN prerequisites 
                ON classes.class_id = prerequisites.class_id 
                WHERE prerequisites.prerequisite_by_class_id = %s
            """, class_id)
            
            course['unblock'] = [unblock[0] for unblock in cursor.fetchall()]    

            results[class_code] = course  


        return {
            'statusCode': 200,
            'headers' : cors_headers,
            'body': json.dumps(results)
        }
    

    except pymysql.Error as e:
        return {
            'statusCode': 500,
            'headers' : cors_headers,
            'body': f"Error connecting to MySQL: {e}"
        }
    finally:
        connection.close()
    
    
