import json
from http.cookies import SimpleCookie
import pymysql, jwt, bcrypt, datetime
db_config = {
	'host': 'database-1.cvwoaic8ob2d.us-west-1.rds.amazonaws.com',
	'user': 'admin',
	'password': 'dbpassword',
	'database': 'csdpath',
}
cors_headers = {
    'Access-Control-Allow-Origin': 'https://csdpath.s3.us-west-1.amazonaws.com',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT',
    'Access-Control-Allow-Credentials': 'true'
}

def lambda_handler(event, context):
	
	# cookie = event['headers']['cookie']
	
	try:
		cursor = pymysql.connect(**db_config).cursor()
	except pymysql.Error as e:
		return {
	'statusCode' : 500,
	'headers' : cors_headers,
	'body': e
	}
	try:
		body = json.loads(event['body'])
		username = body.get('username')
		password = body.get('password')
	except Exception as ke:
		return {
			'statusCode' : 400,
			'headers' : cors_headers,
			'body': 'Bad payload'
		}
	# username = event['username']
	# password = event['password']
	try:
		sql = """
				SELECT 
				    users.id, 
				    users.password_hash, 
				    users.salt, 
				    roles.role_description AS role 
				FROM 
				    users 
				JOIN 
				    roles ON users.role_id = roles.role_id 
				WHERE 
					 users.username = %s;
		"""
		cursor.execute(sql, (username,))
		result = cursor.fetchone()
		if not result:
			return {
			'statusCode' : 401,
			'headers' : cors_headers,
			'body': 'Invalid Credentials'
		} 
		id = result[0]
		password_hash = result[1]
		salt = result[2]
		role = result[3]
	except pymysql.Error as e:
		return {
			'statusCode' : 500,
			'headers' : cors_headers,
			'body': e
		}
	expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
	payload = {'username':f'{username}','role':f'{role}','exp':expiration}
	if password_hash == bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8'):
		token = jwt.encode(payload, 'supersecretkey', algorithm='HS256')
		
		return {
			'statusCode' : 200,
			'headers' : {
				**cors_headers,
				'Set-Cookie': f"login_token={token}; Max-Age=1800; Domain=dnihzli5l8.execute-api.us-west-1.amazonaws.com; Path=/default; SameSite=None; HttpOnly; Secure;"
			},
			'body': json.dumps({'message':'Login Successful!','cp':None,'event':event})
		}
	else:
		return {
			'statusCode' : 400,
			'headers' : cors_headers,
			'body': json.dumps({'Error':'Invalid Credentials'})
			}
