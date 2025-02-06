                                                                                                                                                                  
import psycopg2
import tornado.tcpserver


def check_blacklist(helo_string, recipient_username, sender_email):
    conn = psycopg2.connect(dbname="dbname", user="dbuser", password="dbpassword", host="dbhost, port="dbport")
    cursor = conn.cursor()

    try:

        # region recipient_usernamecheck
        query = f"SELECT content->>'blocked' as sender_username, content->>'recipient_username' as recipient_username FROM dbtable;"
        cursor.execute(query)
        blacklisted_senderusernames = cursor.fetchall()
        for db_sender_senderusername, db_recipient_username in blacklisted_senderusernames:
            if db_sender_senderusername == sender_email and (not db_recipient_username or db_recipient_username == recipient_username):
                return "REJECT"
        # endregion recipient_usernamecheck

        
        # region domaincheck
        query = f"SELECT content->>'blocked' as sender_domain, content->>'recipient_username' as recipient_username FROM dbtable;"
        cursor.execute(query)
        blacklisted_domains = cursor.fetchall()
        for db_sender_domain, db_recipient_username in blacklisted_domains:
            if db_sender_domain in helo_string and (not db_recipient_username or db_recipient_username == recipient_username):
                return "REJECT"

        # endregion domaincheck
        
        # region extensioncheck

        query = f"SELECT content->>'blocked' as extension, content->>'recipient_username' as username FROM dbtable;"
        cursor.execute(query)
        blacklisted_extension = cursor.fetchall()
        for extension, username in blacklisted_extension:
            if extension in helo_string and (not username or username == recipient_username):
                return "REJECT"

        # endregion extensioncheck

        return "OK"


    finally:
        cursor.close()
        conn.close()


class PolicyServer(tornado.tcpserver.TCPServer):
    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        try:

            policy_data = {}
            while True:
                line = yield stream.read_until(b'\n')
                line = line.strip()


                if not line:
                    break

                key, value = line.decode().split('=', 1)
                policy_data[key] = value



            recipient_username = policy_data.get("recipient")
            helo_name = policy_data.get("helo_name")
            sender_email = policy_data.get("sender")
            server_address = policy_data.get("server_address", None)  ## ip adresi engellenmek istenirse
            action = check_blacklist(helo_name, recipient_username, sender_email)

            response = f"action={action}\n\n"

            yield stream.write(response.encode())

        except Exception as e:
            print(f"Error: {e}")
        finally:
            stream.close()


if __name__ == "__main__":
    server = PolicyServer()
    server.listen(35355, address="127.0.0.1")
    print("Policy service dinleniyor: 127.0.0.1:35355")
    tornado.ioloop.IOLoop.current().start()





