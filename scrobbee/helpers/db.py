#!/usr/bin/env python

import os
import sqlite3
import threading

import scrobbee
from scrobbee.helpers import logger

db_lock = threading.Lock()

class DBConnection():
    def __init__(self, filename='scrobbee.db'):
        self.filename = filename
        self.connection = sqlite3.connect(os.path.join(scrobbee.DATA_DIR, filename), 20)
        self.connection.row_factory = sqlite3.Row
    
    def action(self, query, args=None):
        with db_lock:
            if query == None:
                return
    
            sqlResult = None
            attempt = 0
    
            while attempt < 5:
                try:
                    if args == None:
                        logger.debug("Executing: " + query, 'Database ' + self.filename)
                        sqlResult = self.connection.execute(query)
                    else:
                        logger.debug("Executing: " + query+" with args " + str(args), 'Database' + self.filename)
                        sqlResult = self.connection.execute(query, args)
                    self.connection.commit()
                    # get out of the connection attempt loop since we were successful
                    break
                except sqlite3.OperationalError, e:
                    if "unable to open database file" in e.message or "database is locked" in e.message:
                        logger.warning("Database error: " + e.message, 'Database' + self.filename)
                        attempt += 1
                        time.sleep(1)
                    else:
                        logger.error("DataBase error: " + e.message, 'Database' + self.filename)
                        raise
                except sqlite3.DatabaseError, e:
                    logger.error("Fatal error executing query: " + e.message, 'Database' + self.filename)
                    raise
    
            return sqlResult
    
class DBUpgrade():
    def __init__(self):
        return
    
def upgradeDatabase(connection):
    logger.info('Initializing the database')
    
    # All upgrade functions added here in order of running
    upgrades = [initialSchema]
    
    for upgrade in upgrades:
        upgrade(connection)

# All upgrade functions added here in order of running. The function should always check whether it should run first!
def initialSchema(connection):
    table_exists = len(connection.action("SELECT 1 FROM sqlite_master WHERE name = ?;", ('boxee_boxes', )).fetchall())
    if not table_exists:
        query = "CREATE TABLE boxee_boxes (boxee_id INTEGER PRIMARY KEY, boxee_name TEXT, ip TEXT, port NUMERIC);"
        connection.action(query)