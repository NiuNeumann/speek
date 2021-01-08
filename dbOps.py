import psycopg2
from psycopg2 import sql


class Database:
	def __init__(self, config):
		self.database = config.DB_DATABASE
		self.user = config.DB_USER
		self.password = config.DB_PASSWORD
		self.host = config.DB_HOST
		self.port = config.DB_PORT
		self.conn = None

	def connect(self):
		if self.conn is None:
			try:
				self.conn = psycopg2.connect(
					database=self.database,
					user=self.user,
					password=self.password,
					host=self.host,
					port=self.port)
				print('Connection openend succefully')
			except psycopg2.DatabaseError as error:
				print ('Error while connecting to PostgreSQL', error)

	def get_tables(self):
		# returns a list with the names of all tables in the database
		self.connect()
		with self.conn.cursor() as cur:
			cur.execute(sql.SQL("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"))
			tables = []
			fetch = cur.fetchall()
			for x in range(len(fetch)):
				tables.append(fetch[x][0])
			cur.close()
			return tables

	def get_columns(self, table_name):
		# returns a list with the names of the columns of the table with table_name
		self.connect()
		with self.conn.cursor() as cur:
			cur.execute(sql.SQL("SELECT column_name FROM information_schema.columns WHERE table_name = %s"),
				[table_name])
			columns = []
			fetch = cur.fetchall()
			for x in range(len(fetch)):
				columns.append(fetch[x][0])
			cur.close()
			return columns

	def get_rowcount(self, table_name):
		# returns the rowcount of table_name as an integer
		self.connect()
		with self.conn.cursor() as cur:
			cur.execute(sql.SQL("SELECT count(*) FROM {table_}").format(table_=sql.Identifier(table_name)))
			count = cur.fetchone()[0]
			return  count

	def get_single_data(self, table_name, column_name, row_id):
		# returns a list with data as a string from the field in the table with table_name, column_name and row_id
		self.connect()
		with self.conn.cursor() as cur:
			cur.execute(sql.SQL("SELECT {column_} FROM {table_} WHERE id = %s;")
				.format(column_=sql.Identifier(column_name),
					table_=sql.Identifier(table_name)),
				[row_id])
			data = [str(x) for x in cur.fetchone()]
			cur.close()
			return data

	def get_multiple_data(self, table_name):
		# returns a list of lists with the rows and their content from a table with table_name
		self.connect()
		with self.conn.cursor() as cur:
			cur.execute(sql.SQL("SELECT * FROM {table_}").format(table_=sql.Identifier(table_name)))
			data = [list(x) for x in cur.fetchall()]
			cur.close()
			return data

	def create_table(self, table_name, from_lang, to_lang):
		# creates a new table with a name and languages as names of columns 2 and 3
		self.connect()
		with self.conn.cursor() as cur:
			cur.execute(sql.SQL("""CREATE TABLE {table_} (
								id BIGSERIAL NOT NULL PRIMARY KEY,
								{from_} VARCHAR(20),
								{to_} VARCHAR(20));
								""").format(table_=sql.Identifier(table_name),
									from_=sql.Identifier(from_lang),
									to_=sql.Identifier(to_lang)))
			self.conn.commit()
			cur.close()

	def insert_data(self, table_name, column_name, data):
		# inserts data into a field in a new row using the table name and column name and returns the new rows id 
		self.connect()
		with self.conn.cursor() as cur:
			cur.execute(sql.SQL("INSERT INTO {table_} ({column_}) VALUES (%s);")
				.format(table_=sql.Identifier(table_name),
					column_=sql.Identifier(column_name)),
				[data])
			self.conn.commit()
			cur.execute(sql.SQL("SELECT id FROM {table_} ORDER BY id DESC LIMIT 1")
				.format(table_=sql.Identifier(table_name)))
			id = [str(x) for x in cur.fetchone()]
			cur.close()
			return id

	def update_existing(self, table_name, column_name, row_id, data):
		# inserts data into a field of an existing row of a table with table_name , column_name and row_id
		try:
			self.connect()
			with self.conn.cursor() as cur:
				cur.execute(sql.SQL("UPDATE {table_} SET {column_} = %s WHERE id = %s")
					.format(table_=sql.Identifier(table_name),
						column_=sql.Identifier(column_name)),
					[data, row_id])
				self.conn.commit()
				cur.close()
			return True
		except:
			return False

	def remove_data(self, table_name, row_id):
		# removes the row of a table with table_name and row_id
		self.connect()
		with self.conn.cursor() as cur:
			cur.execute(sql.SQL("DELETE FROM {table_} WHERE id = %s")
				.format(table_=sql.Identifier(table_name)),
				[row_id])
			self.conn.commit()
			cur.close()

	def drop_table(self, table_name):
		# deletes the table with table_name
		self.connect()
		with self.conn.cursor() as cur:
			cur.execute(sql.SQL("DROP TABLE {table_}").format(table_=sql.Identifier(table_name)))
			self.conn.commit()
			cur.close
		

	def close_connection(self):
		# closes database connection
		if(self.conn):
			self.conn.commit()
			self.cur.close()
			self.conn.close()
			print("PostgreSQL connection is closed")